"""Preprocessor for Vital Signs data."""

from utils.utils import Utils
import numpy as np

class VitalSignsPreprocessor:
    """Preprocesses the Vital Signs dataset."""

    def preprocess(self, df):
        """Cleans and preprocesses the vitalsigns DataFrame."""
        df_cleaned = self._clean_vitalsigns(df)
        # Impute missing 'pain' values using forward fill
        df_cleaned['pain'] = df_cleaned['pain'].fillna(method='ffill')
        return df_cleaned

    def _clean_vitalsigns(self, df):
        """Cleans vital signs data based on valid ranges."""
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