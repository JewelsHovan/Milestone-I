import pandas as pd
import numpy as np
from .utils import Utils
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from config import DISEASE_CATEGORY_MAPPING, CAREUNIT_MAPPING

def preprocess_diagnosis(df, icd9_codes_path, icd10_codes_path):
    """Processes the diagnosis DataFrame for both ICD-9 and ICD-10 codes."""

    # Separate ICD-9 and ICD-10 dataframes
    df_icd9 = df[df['icd_version'] == 9]
    df_icd10 = df[df['icd_version'] == 10]

    # Process ICD-9 codes
    df_icd9['category_code'] = df_icd9['icd_code'].str[:3]
    icd9_codes = pd.read_csv(icd9_codes_path)
    icd9_codes['category_code'] = icd9_codes['icd_code'].astype(str)
    df_icd9 = df_icd9.merge(icd9_codes, on='category_code', how='left', suffixes=('', '_icd9'))
    df_icd9 = df_icd9.rename(columns={'subcategory': 'subcategory_icd9'})

    # Process ICD-10 codes
    df_icd10['category_code'] = df_icd10['icd_code'].str[:3]
    icd10_codes = pd.read_csv(icd10_codes_path)
    icd10_codes['letter_code'] = icd10_codes['block_code'].str[0:2]
    
    df_icd10['letter_code'] = df_icd10['category_code'].str[0:2]
    icd10_codes = icd10_codes.drop_duplicates(subset=['letter_code'])

    df_icd10 = df_icd10.merge(icd10_codes[['category', 'block_title', 'letter_code']], 
                              on='letter_code', 
                              how='left',
                              suffixes=('', '_icd10'))
    df_icd10 = df_icd10.rename(columns={'block_title': 'subcategory_icd10'})

    # Drop the temporary letter_code column
    df_icd10 = df_icd10.drop(columns=['letter_code'])

    # Combine processed dataframes
    df = pd.concat([df_icd9, df_icd10], ignore_index=True)

    # Combine subcategories
    df['subcategory'] = df['subcategory_icd9'].fillna(df['subcategory_icd10'])

    # Updated category mapping for both ICD-9 and ICD-10
    category_mapping = DISEASE_CATEGORY_MAPPING

    # Apply category mapping
    df['category'] = df['category'].astype(str).map(category_mapping).fillna('Other')
    # fill na in subcategory with 'Other'
    df['subcategory'] = df['subcategory'].fillna('Other')

    # Convert columns to category dtype
    category_columns = ['category_code', 'icd_code', 'category', 'subcategory']
    for col in category_columns:
        df[col] = df[col].astype('category')

    # Before dropping columns, print their non-null counts
    columns_to_drop = ['seq_num', 'description', 'subcategory_icd9', 'subcategory_icd10', 'icd_code_icd9']
    # Drop unnecessary columns
    df = df.drop(columns=columns_to_drop)

    return df

def preprocess_admissions(df):
    """Preprocesses the admissions DataFrame."""
    Utils.convert_to_datetime(df, ['admittime', 'dischtime', 'edregtime', 'edouttime', 'deathtime'])
    Utils.compute_length_of_stay(df, 'admittime', 'dischtime', 'admission')
    df['race'] = df['race'].map(Utils.race_mapping)
    df['discharge_location'] = df['discharge_location'].fillna('Unknown')
    category_columns = [
        'admission_type', 'admission_location', 'discharge_location',
        'insurance', 'language', 'race', 'marital_status'
    ]
    for column in category_columns:
        df[column] = df[column].astype('category')
    df = df.drop(columns=['admit_provider_id'])
    df['is_dead'] = df['deathtime'].notna()
    # Start of Selection
    columns_to_impute = ['insurance', 'marital_status', 'language', 'admission_location']
    for column in columns_to_impute:
        df[column] = df[column].fillna(df[column].mode()[0])

    return df

def preprocess_patients(df):
    """Preprocesses the patients DataFrame."""
    # Convert the dob column to datetime
    df['dod'] = pd.to_datetime(df['dod'])

    # Convert anchor_year_group to category
    df['anchor_year_group'] = df['anchor_year_group'].astype('category')

    # Convert gender to category
    df['gender'] = df['gender'].astype('category')

    # Determine if the patient is dead
    df['is_dead'] = df['dod'].notna()

    return df

def preprocess_transfers(df):
    """Preprocesses the transfers DataFrame."""
    # Parse dates
    df['intime'] = pd.to_datetime(df['intime'])
    df['outtime'] = pd.to_datetime(df['outtime'])

    # Compute length of stay
    df['los'] = (df['outtime'] - df['intime']).dt.total_seconds() / 3600

    # Apply the mapping to the careunit column
    df['careunit_grouped'] = df['careunit'].map(CAREUNIT_MAPPING).fillna('Observation/Other')

    # Convert categorical variables to category dtype
    df['careunit'] = df['careunit'].astype('category')
    df['careunit_grouped'] = df['careunit_grouped'].astype('category')
    df['eventtype'] = df['eventtype'].astype('category')

    # Update 'outtime' and 'los' for rows where eventtype is 'discharge'
    df.loc[df['eventtype'] == 'discharge', 'outtime'] = df['intime']
    df.loc[df['eventtype'] == 'discharge', 'los'] = 0

    # Drop rows with missing los
    df = df.dropna(subset=['los'])

    return df

def preprocess_triage(df):
    """Processes the triage DataFrame."""
    Utils.download_nltk_data()
    df['processed_complaints'] = df['chiefcomplaint'].apply(_preprocess_text)
    df = _assign_topics(df)
    df = _convert_to_ordinal(df)
    df = df.drop(columns=['chiefcomplaint', 'processed_complaints'])
    return df

def preprocess_vitalsigns(df):
    """Cleans and preprocesses the vitalsigns DataFrame."""
    df_cleaned = _clean_vitalsigns(df)
    df_cleaned['pain'] = df_cleaned['pain'].fillna(method='ffill')
    return df_cleaned

def preprocess_ed_stay(df):
    """Preprocesses the edstays DataFrame."""
    Utils.convert_to_datetime(df, ['intime', 'outtime'])
    Utils.compute_length_of_stay(df, 'intime', 'outtime', 'ed')
    df['race'] = df['race'].map(Utils.race_mapping)
    category_columns = ['gender', 'race', 'arrival_transport', 'disposition']
    for column in category_columns:
        df[column] = df[column].astype('category')
    df['admitted'] = df['hadm_id'].notna()
    return df

# Helper functions for triage preprocessing
def _preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return tokens

def _assign_topics(df):
    dictionary = corpora.Dictionary(df['processed_complaints'])
    dictionary.filter_extremes(no_below=10, no_above=0.5)
    corpus = [dictionary.doc2bow(doc) for doc in df['processed_complaints']]
    num_topics = 5
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=10)
    df['topic'] = df['processed_complaints'].apply(
        lambda complaint: _get_topic(complaint, lda_model, dictionary)
    )
    topic_labels = {
        0: "General Pain & Weakness",
        1: "Respiratory & Trauma Symptoms",
        2: "Injury & Alcohol-Related Issues",
        3: "Abdominal & Chest Pain",
        4: "Limb & Head Pain"
    }
    df['topic_label'] = df['topic'].map(topic_labels)
    return df

def _convert_to_ordinal(df):
    df['acuity'] = pd.Categorical(df['acuity'], categories=[1, 2, 3, 4, 5], ordered=True)
    df['topic'] = pd.Categorical(df['topic'] + 1, categories=[1, 2, 3, 4, 5], ordered=True)
    return df

def _get_topic(complaint, lda_model, dictionary):
    bow = dictionary.doc2bow(complaint)
    topic_distribution = lda_model.get_document_topics(bow)
    return max(topic_distribution, key=lambda x: x[1])[0]

# Helper function for vitalsigns preprocessing
def _clean_vitalsigns(df):
    valid_ranges = {
        'temperature': (95.0, 107.6),
        'heartrate': (20, 250),
        'resprate': (4, 60),
        'o2sat': (70, 100),
        'sbp': (50, 250),
        'dbp': (20, 150)
    }
    for vitalsign, (lower, upper) in valid_ranges.items():
        df[vitalsign] = df[vitalsign].apply(
            lambda x: x if lower <= x <= upper else np.nan
        )
    df_cleaned = df.dropna(subset=valid_ranges.keys())
    return df_cleaned