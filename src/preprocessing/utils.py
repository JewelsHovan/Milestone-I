

"""Utility functions and classes for data preprocessing."""

import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import nltk

class Utils:
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
        print("\n" + "="*50)
        print(f"DataFrame Information for: {df.name if hasattr(df, 'name') else 'Unnamed DataFrame'}")
        print("="*50)
        
        print("\nShape:")
        print(f"  Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        print("\nColumn Types:")
        for dtype in df.dtypes.value_counts().index:
            print(f"  {dtype}: {df.dtypes.value_counts()[dtype]}")
        
        print("\nMissing Values:")
        missing = df.isnull().sum()
        if missing.sum() > 0:
            for col in missing[missing > 0].index:
                print(f"  {col}: {missing[col]} ({missing[col]/len(df):.2%})")
        else:
            print("  No missing values")
        
        print("\nNumeric Columns Summary:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols].describe().to_string())
        else:
            print("  No numeric columns")
        
        print("\nCategorical Columns Summary:")
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            for col in cat_cols:
                print(f"  {col}:")
                print(f"    Unique values: {df[col].nunique()}")
                print(f"    Top 5 values: {df[col].value_counts().nlargest(5).to_dict()}")
        else:
            print("  No categorical columns")
        
        print("\nSample Data:")
        print(df.head().to_string())
        
        print("\n" + "="*50 + "\n")

    @staticmethod
    def convert_to_datetime(df, columns):
        for col in columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    @staticmethod
    def compute_length_of_stay(df, intime_col, outtime_col, stay_type='ed'):
        df[f'{stay_type}_los_hours'] = (
            df[outtime_col] - df[intime_col]).dt.total_seconds() / 3600.0

    @staticmethod
    def map_to_group(df, column, mapping_dict, fill_na='Other'):
        df[f'{column}_grouped'] = df[column].map(mapping_dict)
        df[f'{column}_grouped'] = df[f'{column}_grouped'].fillna(fill_na)

    @staticmethod
    def filter_outliers(df, column, method='IQR'):
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
        if columns is None:
            columns = df.columns
        imputer = SimpleImputer(strategy=strategy)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    @staticmethod
    def encode_categorical(df, columns):
        df_encoded = pd.get_dummies(df, columns=columns, drop_first=True)
        return df_encoded

    @staticmethod
    def standardize_features(df, columns):
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    @staticmethod
    def download_nltk_data():
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
