"""Preprocessor for Triage data."""

from utils.utils import Utils
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import nltk
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import pandas as pd

class TriagePreprocessor:
    """Preprocesses the Triage dataset."""

    def preprocess(self, df):
        """Processes the triage DataFrame."""
        Utils.download_nltk_data()
        df['processed_complaints'] = df['chiefcomplaint'].apply(self._preprocess_text)
        df = self._assign_topics(df)
        df = self._convert_to_ordinal(df)
        df = df.drop(columns=['chiefcomplaint', 'processed_complaints'])
        return df

    def _preprocess_text(self, text):
        """Preprocesses text data."""
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
        # Lowercase
        text = str(text).lower()
        # Remove non-alphabetical characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Tokenize
        tokens = nltk.word_tokenize(text)
        # Remove stopwords and lemmatize
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
        return tokens

    def _assign_topics(self, df):
        """Assigns topics to preprocessed complaints using LDA."""
        # Build dictionary and corpus for LDA
        dictionary = corpora.Dictionary(df['processed_complaints'])
        dictionary.filter_extremes(no_below=10, no_above=0.5)
        corpus = [dictionary.doc2bow(doc) for doc in df['processed_complaints']]

        # LDA Model
        num_topics = 5
        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42, passes=10)

        # Assign topics
        df['topic'] = df['processed_complaints'].apply(
            lambda complaint: self._get_topic(complaint, lda_model, dictionary)
        )

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

    def _convert_to_ordinal(self, df):
        """Converts acuity and topic to ordinal categories."""
        # Convert acuity to ordinal (assuming it's already in the DataFrame)
        df['acuity'] = pd.Categorical(df['acuity'], categories=[1, 2, 3, 4, 5], ordered=True)
        
        # Convert topic to ordinal (adding 1 to make it 1-indexed)
        df['topic'] = pd.Categorical(df['topic'] + 1, categories=[1, 2, 3, 4, 5], ordered=True)
        
        return df

    def _get_topic(self, complaint, lda_model, dictionary):
        """Returns the topic for a given complaint."""
        bow = dictionary.doc2bow(complaint)
        topic_distribution = lda_model.get_document_topics(bow)
        return max(topic_distribution, key=lambda x: x[1])[0]