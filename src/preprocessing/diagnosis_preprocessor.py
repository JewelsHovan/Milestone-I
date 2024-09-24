"""Preprocessor for Diagnosis data."""

import pandas as pd
from utils.utils import Utils

class DiagnosisPreprocessor:
    """Preprocesses the Diagnosis dataset."""

    def preprocess(self, df, disease_categories_path):
        """Processes the diagnosis DataFrame."""
        # Filter for ICD-10 codes
        df = df[df['icd_version'] == 10]

        # Extract category code and letter code
        df['category_code'] = df['icd_code'].str[:3]
        df['letter_code'] = df['category_code'].str[0]

        # Convert category_code and letter_code to category dtypes
        df['category_code'] = df['category_code'].astype('category')
        df['icd_code'] = df['icd_code'].astype('category')
        df['letter_code'] = df['letter_code'].astype('category')

        # Load disease categories mapping
        disease_categories_df = pd.read_csv(disease_categories_path)
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
        
        df['category'] = df['category'].map(category_mapping).fillna('Other')
        df['category'] = df['category'].astype('category')

        # Drop specified columns
        df = df.drop(columns=['icd_title', 'icd_version', 'seq_num'])
        
        return df