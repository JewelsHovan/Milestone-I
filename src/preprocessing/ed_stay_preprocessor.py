"""Preprocessor for ED Stay data."""

from utils.utils import Utils

class EDStayPreprocessor:
    """Preprocesses the ED Stay dataset."""

    def preprocess(self, df):
        """Preprocesses the edstays DataFrame."""
        Utils.convert_to_datetime(df, ['intime', 'outtime'])
        Utils.compute_length_of_stay(df, 'intime', 'outtime', 'ed')

        # perform map on race
        df['race'] = df['race'].map(Utils.race_mapping)

        # Convert gender, race, arrival transport and disposition into category variables
        category_columns = ['gender', 'race', 'arrival_transport', 'disposition']
        for column in category_columns:
            df[column] = df[column].astype('category')

        return df
