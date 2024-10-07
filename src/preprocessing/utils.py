"""Utility functions and classes for data preprocessing."""

import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import nltk
import ipywidgets as widgets
from IPython.display import display

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

    # Data Information Methods
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
        display(df.head())
        
        print("\n" + "="*50 + "\n")

    # Data Conversion Methods
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

    # Data Cleaning Methods
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

    # Data Transformation Methods
    @staticmethod
    def encode_categorical(df, columns):
        df_encoded = pd.get_dummies(df, columns=columns, drop_first=True)
        return df_encoded

    @staticmethod
    def standardize_features(df, columns):
        scaler = StandardScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    # NLTK Data Download Method
    @staticmethod
    def download_nltk_data():
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

    # Custom Methods for Disease Incidence Analysis
    @staticmethod
    def categorize_age(age):
        if pd.isna(age):
            return 'All ages'
        elif age < 5:
            return '<5 years'
        elif 5 <= age <= 14:
            return '5-14 years'
        elif 15 <= age <= 49:
            return '15-49 years'
        elif 50 <= age <= 69:
            return '50-69 years'
        else:
            return '70+ years'

    @staticmethod
    def get_first_element(x):
        if isinstance(x, list) and len(x) > 0:
            return x[0]
        elif isinstance(x, str):
            try:
                lst = eval(x)
                if isinstance(lst, list) and len(lst) > 0:
                    return lst[0]
            except:
                pass
        return None

    @staticmethod
    def extract_icd_ranges(df, cause_name_col, *icd_cols):
        icd_dict = {}
        for idx, row in df.iterrows():
            cause_name = row[cause_name_col]
            icd_ranges = []
            for icd_col in icd_cols:
                if pd.notna(row[icd_col]):
                    ranges = row[icd_col].split(", ")
                    for r in ranges:
                        icd_ranges.append(r)
            icd_dict[cause_name] = icd_ranges
        return icd_dict
    
    @staticmethod
    def get_n_element(x, n):
        if isinstance(x, list) and len(x) >= n:
            return x[n-1]
        elif isinstance(x, list) and len(x) == n-1:
            return None
        elif isinstance(x, str):
            return None
        return None

    @staticmethod
    def code_map_from_icd_list(row, icd9_ranges, icd10_ranges):
        icd_list = row["icd_code"]
        for i in range(1, len(icd_list)+1):
            code = Utils.get_n_element(icd_list, i)
            if code:
                if len(code) > 3:
                    code = code[:3] + "." + code[3:]
                if row['primary_ICD_version'] == 9:
                    result = Utils.get_disease_for_icd(code, icd9_ranges)
                else:
                    result = Utils.get_disease_for_icd(code, icd10_ranges)
                if result != "Unknown":
                    return result
        return "Unknown"

    @staticmethod
    def get_disease_for_icd(icd_code, icd_ranges):
        for disease, ranges in icd_ranges.items():
            for range_str in ranges:
                start, end = Utils.parse_icd_range(range_str)
                if Utils.is_in_range(icd_code, start, end):
                    return disease
        return "Unknown"

    @staticmethod
    def parse_icd_range(range_str):
        parts = range_str.split('-')
        if len(parts) == 1:
            return parts[0].strip(), parts[0].strip()
        start, end = parts
        return start.strip(), end.strip()

    @staticmethod
    def is_in_range(code, start, end):
        if start == end:
            return code == start
        if '.' not in code:
            code += '.0'
        if '.' not in start:
            start += '.0'
        if '.' not in end:
            end += '.9'
        return start <= code <= end

    @staticmethod
    def display_dataframes(dataframes, titles):
        outputs = [widgets.Output() for _ in dataframes]

        for output, dataframe in zip(outputs, dataframes):
            with output:
                display(dataframe.head())

        tab = widgets.Tab(outputs)
        for i, title in enumerate(titles):
            tab.set_title(i, title)

        display(tab)
