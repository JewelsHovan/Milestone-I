"""Preprocessor for Admissions data."""

from utils.utils import Utils

class AdmissionsPreprocessor:
    """Preprocesses the Admissions dataset."""

    def preprocess(self, df):
        """Preprocesses the admissions DataFrame."""
        Utils.convert_to_datetime(df, ['admittime', 'dischtime', 'edregtime', 'edouttime', 'deathtime'])
        Utils.compute_length_of_stay(df, 'admittime', 'dischtime', 'admission')
        # perform map on race
        df['race'] = df['race'].map(Utils.race_mapping)
        # Convert specified columns to category
        category_columns = [
            'admission_type',
            'admission_location',
            'discharge_location',
            'insurance',
            'language',
            'race',
            'marital_status'
        ]
        for column in category_columns:
            df[column] = df[column].astype('category')
        # remove admission_provider_id columnn
        df = df.drop(columns=['admit_provider_id'])
        # add is_dead column
        df['is_dead'] = df['deathtime'].notna()
        return df
