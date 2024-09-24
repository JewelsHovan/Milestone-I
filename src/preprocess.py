"""Module for preprocessing MIMIC dataset."""
import pandas as pd
from utils.utils import nunique_per_cat
import numpy as np
from IPython.display import display



# a utility preprocessor class to preprocess different datasets
class PreprocessMIMIC:
    """
    A class to preprocess MIMIC-IV data tables.
    """
    def __init__(self):
        pass

    def print_info(self, df):
        """
        Prints basic information about the DataFrame.
        """
        print("DataFrame Information:")
        display(df.info())
        print("\nMissing Values:")
        display(df.isna().sum())
        print("\nDataFrame Head:")
        display(df.head())
        print("\nDataFrame Description:")
        display(df.describe(include='all'))

    def convert_to_datetime(self, df, columns):
        """
        Converts specified columns of a DataFrame to datetime objects.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the columns.
        columns (list): List of column names to convert.
        """
        for col in columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    def compute_length_of_stay(self, df, intime_col, outtime_col, stay_type='ed'):
        """
        Computes the length of stay in hours and adds it as a new column.

        Parameters:
        df (pd.DataFrame): The DataFrame containing intime and outtime columns.
        intime_col (str): The name of the admission time column.
        outtime_col (str): The name of the discharge time column.
        stay_type (str): Type of stay ('ed' for emergency department, 'admission' for hospital).
        """
        df[f'{stay_type}_los_hours'] = (df[outtime_col] - df[intime_col]).dt.total_seconds() / 3600.0

    def map_to_group(self, df, column, mapping_dict, fill_na='Other'):
        """
        Maps the values of a column to specified groups.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the column.
        column (str): The name of the column to map.
        mapping_dict (dict): A dictionary mapping original values to group names.
        fill_na (str): Value to fill in for missing or unmatched entries.
        """
        df[f'{column}_grouped'] = df[column].map(mapping_dict)
        df[f'{column}_grouped'] = df[f'{column}_grouped'].fillna(fill_na)

    def filter_outliers(self, df, column, method='IQR'):
        """
        Filters outliers from a specified column in the DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame containing the column.
        column (str): The name of the column to filter.
        method (str): The method to use for outlier detection ('IQR' or 'Z-score').

        Returns:
        pd.DataFrame: The DataFrame with outliers removed.
        """
        if method == 'IQR':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
        elif method == 'Z-score':
            from scipy import stats
            z_scores = stats.zscore(df[column].dropna())
            abs_z_scores = np.abs(z_scores)
            df_filtered = df[abs_z_scores < 3]
        else:
            raise ValueError("Method must be 'IQR' or 'Z-score'")
        return df_filtered

    def clean_vitalsigns(self, df):
        """
        Cleans vital signs data by removing unrealistic values based on medical reference ranges.

        Parameters:
        df (pd.DataFrame): The DataFrame containing vital signs.

        Returns:
        pd.DataFrame: The cleaned DataFrame.
        """
        # Define valid ranges
        valid_ranges = {
            'temperature': (95.0, 107.6),
            'heartrate': (20, 250),
            'resprate': (4, 60),
            'o2sat': (70, 100),
            'sbp': (50, 250),
            'dbp': (20, 150)
        }

        # Clean each vital sign
        for vitalsign, (lower, upper) in valid_ranges.items():
            df[vitalsign] = df[vitalsign].apply(
                lambda x: x if lower <= x <= upper else np.nan
            )
        # Drop rows with NaNs in any of the vital signs
        df_cleaned = df.dropna(subset=valid_ranges.keys())
        return df_cleaned

    def preprocess_diagnosis(self, df):
        """
        Processes the diagnosis DataFrame by extracting category codes and mapping to disease categories.

        Parameters:
        df (pd.DataFrame): The diagnosis DataFrame.

        Returns:
        pd.DataFrame: The DataFrame with added category codes and disease categories.
        """
        # Extract category code
        df['category_code'] = df['icd_code'].str[:3]
        df['letter_code'] = df['category_code'].str[0]

        # Load disease categories mapping
        disease_categories_df = pd.read_csv("../Data/disease_categories.csv")
        disease_categories_df['letter_code'] = disease_categories_df['block_code'].str[0]

        # Map categories
        df = df.merge(
            disease_categories_df[['category', 'letter_code']],
            on='letter_code',
            how='left'
        )

        # Simplify category names
        category_mapping = {
            'Diseases of the nervous system': 'Nervous System',
            'Mental and behavioural disorders': 'Mental & Behavioral',
            'Diseases of the digestive system': 'Digestive System',
            'Endocrine, nutritional and metabolic diseases': 'Endocrine & Metabolic',
            'Diseases of the circulatory system': 'Circulatory System',
            'Diseases of the respiratory system': 'Respiratory System',
            'Diseases of the genitourinary system': 'Genitourinary System',
            'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism': 'Blood & Immune System',
            'Diseases of the eye and adnexa': 'Eye & Adnexa',
            'Diseases of the ear and mastoid process': 'Ear & Mastoid',
            'Pregnancy, childbirth and the puerperium': 'Pregnancy & Childbirth',
            'Certain infectious and parasitic diseases': 'Infectious & Parasitic'
        }
        df['category'] = df['category'].map(category_mapping)
        return df

    def preprocess_triage_text(self, df):
        """
        Processes the chief complaints in the triage DataFrame using NLP techniques.

        Parameters:
        df (pd.DataFrame): The triage DataFrame.

        Returns:
        pd.DataFrame: The DataFrame with processed complaints and assigned topics.
        """
        import nltk
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from nltk.stem import WordNetLemmatizer
        import re

        # Download necessary NLTK data files
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        def preprocess_text(text):
            # Lowercase
            text = str(text).lower()
            # Remove non-alphabetical characters
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            # Tokenize
            tokens = word_tokenize(text)
            # Remove stopwords and lemmatize
            tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
            return tokens

        df['processed_complaints'] = df['chiefcomplaint'].apply(preprocess_text)

        # Build dictionary and corpus for LDA
        from gensim.corpora import Dictionary
        dictionary = Dictionary(df['processed_complaints'])
        dictionary.filter_extremes(no_below=10, no_above=0.5)
        corpus = [dictionary.doc2bow(doc) for doc in df['processed_complaints']]

        # LDA Model
        from gensim.models import LdaModel
        num_topics = 5
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=10)

        # Assign topics
        def assign_topic(complaint):
            bow = dictionary.doc2bow(complaint)
            topic_distribution = lda_model.get_document_topics(bow)
            return max(topic_distribution, key=lambda x: x[1])[0]

        df['topic'] = df['processed_complaints'].apply(assign_topic)

        # Map topics to labels
        topic_labels = {
            0: "General Pain & Weakness",
            1: "Respiratory & Trauma Symptoms",
            2: "Injury & Alcohol-Related Issues",
            3: "Abdominal & Chest Pain",
            4: "Limb & Head Pain"
        }
        df['topic_label'] = df['topic'].map(topic_labels)
        return df

    def impute_missing_values(self, df, strategy='mean', columns=None):
        """
        Imputes missing values in the DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame to impute.
        strategy (str): The imputation strategy ('mean', 'median', 'most_frequent').
        columns (list): List of columns to impute. If None, all columns are imputed.

        Returns:
        pd.DataFrame: The DataFrame with imputed values.
        """
        from sklearn.impute import SimpleImputer
        if columns is None:
            columns = df.columns
        imputer = SimpleImputer(strategy=strategy)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    def encode_categorical(self, df, columns):
        """
        Encodes categorical features using One-Hot Encoding.

        Parameters:
        df (pd.DataFrame): The DataFrame containing categorical features.
        columns (list): List of columns to encode.

        Returns:
        pd.DataFrame: The DataFrame with encoded features.
        """
        df_encoded = pd.get_dummies(df, columns=columns, drop_first=True)
        return df_encoded

    def standardize_features(self, df, columns):
        """
        Standardizes numerical features in the DataFrame.

        Parameters:
        df (pd.DataFrame): The DataFrame containing numerical features.
        columns (list): List of columns to standardize.

        Returns:
        pd.DataFrame: The DataFrame with standardized features.
        """
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    def preprocess_vitalsigns(self, df):
        """
        Cleans the vitalsigns DataFrame and handles missing values.

        Parameters:
        df (pd.DataFrame): The vitalsigns DataFrame.

        Returns:
        pd.DataFrame: The cleaned vitalsigns DataFrame.
        """
        # Clean unrealistic values
        df_cleaned = self.clean_vitalsigns(df)
        # Impute missing 'pain' values using forward fill
        df_cleaned['pain'] = df_cleaned['pain'].fillna(method='ffill')
        return df_cleaned

    def merge_tables(self, df_list, on_columns, how='inner'):
        """
        Merges a list of DataFrames on specified columns.

        Parameters:
        df_list (list): List of DataFrames to merge.
        on_columns (list): List of column names to merge on.
        how (str): Type of merge ('inner', 'outer', 'left', 'right').

        Returns:
        pd.DataFrame: The merged DataFrame.
        """
        from functools import reduce
        df_merged = reduce(lambda left, right: pd.merge(left, right, on=on_columns, how=how), df_list)
        return df_merged

    def process_all_tables(self, file_paths):
        """
        Processes all tables and returns the final merged DataFrame ready for analysis.

        Parameters:
        file_paths (dict): Dictionary containing file paths for each table.

        Returns:
        pd.DataFrame: The final preprocessed DataFrame.
        """
        # Load data
        ed_stays = pd.read_csv(file_paths['edstays'])
        admissions = pd.read_csv(file_paths['admissions'])
        diagnosis = pd.read_csv(file_paths['diagnosis'])
        triage = pd.read_csv(file_paths['triage'])
        vitalsigns = pd.read_csv(file_paths['vitalsigns'])
        # More tables can be added as needed

        # Preprocess ed_stays
        self.convert_to_datetime(ed_stays, ['intime', 'outtime'])
        self.compute_length_of_stay(ed_stays, 'intime', 'outtime', 'ed')
        # Map race to groups if race_mapping is provided
        # self.map_to_group(ed_stays, 'race', race_mapping, fill_na='Other')

        # Preprocess admissions
        self.convert_to_datetime(admissions, ['admittime', 'dischtime', 'edregtime', 'edouttime'])
        self.compute_length_of_stay(admissions, 'admittime', 'dischtime', 'admission')
        # Map race to groups if race_mapping is provided
        # self.map_to_group(admissions, 'race', race_mapping, fill_na='Other')

        # Preprocess triage
        triage = self.preprocess_triage_text(triage)
        triage_cleaned = self.clean_vitalsigns(triage)

        # Preprocess vitalsigns
        vitalsigns_cleaned = self.preprocess_vitalsigns(vitalsigns)

        # Preprocess diagnosis
        diagnosis_processed = self.preprocess_diagnosis(diagnosis)

        # Merge tables
        df_list = [ed_stays, admissions, triage_cleaned, vitalsigns_cleaned, diagnosis_processed]
        merge_columns = ['subject_id']
        final_df = self.merge_tables(df_list, on_columns=merge_columns, how='inner')
        return final_df
