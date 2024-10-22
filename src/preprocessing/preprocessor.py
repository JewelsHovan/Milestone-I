import pandas as pd
from .preprocessing_functions import (
    preprocess_diagnosis,
    preprocess_admissions,
    preprocess_triage,
    preprocess_vitalsigns,
    preprocess_ed_stay,
    preprocess_patients,
    preprocess_transfers,
    preprocess_icu_stays,
    preprocess_prescriptions
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

        if table_name == 'prescriptions':
            df = pd.read_csv(
                self.file_paths[table_name],
                usecols=['subject_id', 'hadm_id', 'drug_type', 'drug', 'gsn', 'ndc', 'prod_strength']
            )
        else:
            df = pd.read_csv(self.file_paths[table_name])
        # set the name of the dataframe
        df.name = table_name

        if table_name == 'diagnosis':
            return preprocess_diagnosis(df, self.file_paths['icd9_codes'], self.file_paths['icd10_codes'])
        elif table_name == 'hosp_diagnosis':
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
        elif table_name == 'icu_stays':
            return preprocess_icu_stays(df)
        elif table_name == 'prescriptions':
            return preprocess_prescriptions(df)
        else:
            print(f"Warning: No preprocessing function for {table_name}")
            return df

    def preprocess_and_save_all(self, save_dir="../Processed_Data"):
        import os

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        preprocessed_data = self.preprocess_all()
        for table_name, df in preprocessed_data.items():
            df.to_pickle(f"{save_dir}/{table_name}.pkl")

    def preprocess_and_save_sample(self, save_dir="../Processed_Data_Sample"):
        """
        Preprocesses all tables and saves only the first 100 rows of each to the specified directory.

        Parameters:
        - save_dir (str): The directory where the sample data will be saved. Defaults to "../Processed_Data_Sample".
        """
        import os

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        preprocessed_data = self.preprocess_all()
        for table_name, df in preprocessed_data.items():
            sample_df = df.head(100)
            sample_df.to_pickle(f"{save_dir}/{table_name}.pkl")
            print(f"Saved sample of {table_name} with {len(sample_df)} rows to {save_dir}/{table_name}.pkl")
