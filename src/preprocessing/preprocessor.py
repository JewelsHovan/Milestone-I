import pandas as pd
from .preprocessing_functions import (
    preprocess_diagnosis,
    preprocess_admissions,
    preprocess_triage,
    preprocess_vitalsigns,
    preprocess_ed_stay,
    preprocess_patients,
    preprocess_transfers
)

class Preprocessor:
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def preprocess_all(self):
        preprocessed_data = {}

        for table_name, file_path in self.file_paths.items():
            preprocessed_data[table_name] = self.preprocess_table(table_name)

        return preprocessed_data

    def preprocess_table(self, table_name):
        if table_name not in self.file_paths:
            raise ValueError(f"No file path found for table: {table_name}")

        df = pd.read_csv(self.file_paths[table_name])
        # set the name of the dataframe
        df.name = table_name

        if table_name == 'diagnosis':
            return preprocess_diagnosis(df, self.file_paths['icd9_codes'], self.file_paths['icd10_codes'])
        elif table_name == 'admissions':
            return preprocess_admissions(df)
        elif table_name == 'triage':
            return preprocess_triage(df)
        elif table_name == 'vitalsigns':
            return preprocess_vitalsigns(df)
        elif table_name == 'edstays':
            return preprocess_ed_stay(df)
        elif table_name == 'patients':
            return preprocess_patients(df)
        elif table_name == 'transfers':
            return preprocess_transfers(df)
        else:
            print(f"Warning: No preprocessing function for {table_name}")
            return df