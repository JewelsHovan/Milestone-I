

"""Utility functions and classes for data preprocessing."""

import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from functools import reduce


class Utils:
    """Utility functions for data preprocessing."""

    race_mapping = {
        'WHITE': 'White/European Descent',
        'WHITE - RUSSIAN': 'White/European Descent',
        'WHITE - OTHER EUROPEAN': 'White/European Descent',
        'WHITE - BRAZILIAN': 'White/European Descent',
        'WHITE - EASTERN EUROPEAN': 'White/European Descent',
        'PORTUGUESE': 'White/European Descent',

        'BLACK/AFRICAN AMERICAN': 'Black/African Descent',
        'BLACK/CAPE VERDEAN': 'Black/African Descent',
        'BLACK/AFRICAN': 'Black/African Descent',
        'BLACK/CARIBBEAN ISLAND': 'Black/African Descent',

        'HISPANIC OR LATINO': 'Hispanic/Latino',
        'HISPANIC/LATINO - PUERTO RICAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - DOMINICAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - SALVADORAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - GUATEMALAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - MEXICAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - CUBAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - HONDURAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - CENTRAL AMERICAN': 'Hispanic/Latino',
        'HISPANIC/LATINO - COLUMBIAN': 'Hispanic/Latino',
        'SOUTH AMERICAN': 'Hispanic/Latino',

        'ASIAN': 'Asian',
        'ASIAN - CHINESE': 'Asian',
        'ASIAN - SOUTH EAST ASIAN': 'Asian',
        'ASIAN - KOREAN': 'Asian',
        'ASIAN - ASIAN INDIAN': 'Asian',

        'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER': 'Native American/Pacific Islander',
        'AMERICAN INDIAN/ALASKA NATIVE': 'Native American/Pacific Islander',

        'MULTIPLE RACE/ETHNICITY': 'Mixed or Other',
        'OTHER': 'Mixed or Other',
        'UNABLE TO OBTAIN': 'Mixed or Other',
        'UNKNOWN': 'Mixed or Other',
        'PATIENT DECLINED TO ANSWER': 'Mixed or Other'
    }

    @staticmethod
    def print_info(df):
        """Prints basic information about the DataFrame."""
        print("DataFrame Information:")
        display(df.info())
        print("\nMissing Values:")
        display(df.isna().sum())
        print("\nDataFrame Head:")
        display(df.head())
        print("\nDataFrame Description:")
        display(df.describe(include='all'))

    @staticmethod
    def convert_to_datetime(df, columns):
        """Converts specified columns of a DataFrame to datetime objects."""
        for col in columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    @staticmethod
    def compute_length_of_stay(df, intime_col, outtime_col, stay_type='ed'):
        """Computes the length of stay in hours and adds it as a new column."""
        df[f'{stay_type}_los_hours'] = (
            df[outtime_col] - df[intime_col]).dt.total_seconds() / 3600.0

    @staticmethod
    def map_to_group(df, column, mapping_dict, fill_na='Other'):
        """Maps the values of a column to specified groups."""
        df[f'{column}_grouped'] = df[column].map(mapping_dict)
        df[f'{column}_grouped'] = df[f'{column}_grouped'].fillna(fill_na)

    @staticmethod
    def filter_outliers(df, column, method='IQR'):
        """Filters outliers from a specified column in the DataFrame."""
        if method == 'IQR':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_filtered = df[(df[column] >= lower_bound) &
                             (df[column] <= upper_bound)]
        elif method == 'Z-score':
            from scipy import stats
            z_scores = stats.zscore(df[column].dropna())
            abs_z_scores = np.abs(z_scores)
            df_filtered = df[abs_z_scores < 3]
        else:
            raise ValueError("Method must be 'IQR' or 'Z-score'")
        return df_filtered

    @staticmethod
    def impute_missing_values(df, strategy='mean', columns=None):
        """Imputes missing values in the DataFrame."""
        if columns is None:
            columns = df.columns
        imputer = SimpleImputer(strategy=strategy)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    @staticmethod
    def encode_categorical(df, columns):
        """Encodes categorical features using One-Hot Encoding."""
        df_encoded = pd.get_dummies(df, columns=columns, drop_first=True)
        return df_encoded

    @staticmethod
    def standardize_features(df, columns):
        """Standardizes numerical features in the DataFrame."""
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    @staticmethod
    def download_nltk_data():
        """Downloads necessary NLTK data files."""
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
