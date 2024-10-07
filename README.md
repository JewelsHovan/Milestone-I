# **COVID-19 Impact Analysis on Hospital Dynamics and Patient Care**

## **Project Overview**

This project focuses on analyzing the impact of COVID-19 on hospital dynamics, patient profiles, and outcomes using the MIMIC-IV dataset. By integrating insurance data and Global Burden of Disease (GBD) statistics, we aim to provide insights into how the pandemic affected hospital operations, patient care, and mortality rates. Our analysis specifically examines the effects of COVID-19 within the hospital setting, primarily utilizing the HOSP and ICU modules of the MIMIC-IV dataset. By integrating insurance data and GBD data to map ICD codes to disease labels and categories, we enable comparative analyses at state (Massachusetts) and county levels. This comprehensive approach allows us to assess the pandemic's impact from multiple perspectives, helping to understand the challenges faced during the pandemic and in preparing for future healthcare crises.

## **Team Members**

- **Jewels Hovan** (jhovan)
- **Liu Liu** (luvul)
- **George Mathew** (ggmathew)

## **Datasets**

We are working with publicly available datasets from the **MIMIC-IV** database and external sources to enrich our analysis.

### **Primary Dataset: MIMIC-IV Clinical Database**

- **Description**: Contains detailed clinical data for hospital admissions, including patient demographics, diagnoses, procedures, medications, and vital signs.
- **Size**: Various tables totaling over 550,000 records.
- **Access Method**: Accessible through PhysioNet with appropriate credentials.
- **Source**: [MIMIC-IV Clinical Database](https://mimic.mit.edu/docs/iv/)

### **External Datasets**

#### 1. **Insurance Data (CMS Medicare Enrollment Reports)**

- **Description**: Medicare enrollment and claims data providing state and county-level statistics on insurance coverage and healthcare utilization.
- **Size**: Data from 2013 onwards; varies by report.
- **Access Method**: Available through the Centers for Medicare & Medicaid Services (CMS).
- **Source**: [CMS Medicare Enrollment Reports](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment)

#### 2. **Global Burden of Disease (GBD) Data**

- **Description**: Comprehensive dataset providing global health statistics related to disease prevalence, incidence, mortality, and risk factors.
- **Size**: Extensive coverage of diseases and conditions globally.
- **Access Method**: Accessible through the Institute for Health Metrics and Evaluation (IHME).
- **Source**: [Global Health Data Exchange](https://ghdx.healthdata.org/gbd-results-tool)

#### 3. **ICD-10 and ICD-9 Classification Data**

- **Description**: Datasets mapping ICD codes to disease descriptions and hierarchical categories, enabling grouping of diagnoses for analysis.
- **Size**: Comprehensive coverage of ICD codes.
- **Access Method**: Generated via web scraping from the World Health Organization (WHO) ICD-10 and ICD-9 websites.
- **Source**:
  - [WHO ICD-10 Classification](https://icd.who.int/browse10/2010/en)
  - [CDC ICD-9 CM Browser](https://www.cdc.gov/nchs/icd/icd9cm.htm)

## **Project Objectives**

- **Analyze Hospital Dynamics**: Examine ICU admissions, bed occupancy rates, and resource utilization before and during the COVID-19 pandemic.
- **Profile COVID-19 Patients**: Explore demographics, comorbidities, and outcomes of patients diagnosed with COVID-19.
- **Assess Mortality Rates**: Investigate mortality trends among COVID-19 patients across different age groups and years.
- **Integrate Insurance Data**: Analyze the impact of insurance coverage on patient outcomes and hospital resource utilization.
- **Comparative Analysis**: Compare hospital data with state and county-level statistics to identify unique patterns or deviations.
- **Map Disease Categories**: Utilize ICD codes to group diagnoses, facilitating higher-level analyses of disease patterns.

## **Data Cleaning and Manipulation**

- **Config and Preprocessor Class**: Implemented a `config` module and a `Preprocessor` class to streamline the preprocessing of all utilized MIMIC-IV tables.
- **Outlier Removal**: Identified and addressed extreme outliers in physiological measurements to improve data quality.
- **Handling Missing Data**: Employed imputation techniques and model-based methods to handle missing values.
- **Feature Engineering**:
  - **Time Intervals**: Calculated durations between key events (e.g., admission to ICU transfer).
  - **Disease Mapping**: Mapped ICD codes to disease categories using GBD data.
  - **Age Grouping**: Categorized patients into age groups for demographic analysis.
- **Data Integration**:
  - **Merging Datasets**: Aligned MIMIC-IV data with insurance and GBD data using common keys (e.g., ICD codes, demographics).
  - **Aggregation**: Aggregated data to match granularity levels when merging (e.g., state vs. county data).
- **Text Data Processing**: Applied NLP techniques to process textual fields like clinical notes for additional insights.

## **Codebase Structure**

Our codebase is organized to facilitate efficient data processing and analysis.

### **Configuration**

We use a `config.py` file to manage file paths and other configurations centrally. This allows for easy updates and consistent access across all scripts.

```python:src/config.py
import os

# File paths
FILE_PATHS = {
    # ED files
    'edstays': "../ED/edstays.csv",
    'diagnosis': "../ED/diagnosis.csv",
    'triage': "../ED/triage.csv",
    'vitalsigns': '../ED/vitalsign.csv',

    # HOSP files
    'admissions': "../HOSP/admissions.csv",
    'transfers': "../HOSP/transfers.csv",
    'patients': "../HOSP/patients.csv",
    'hosp_diagnosis': "../HOSP/diagnoses_icd.csv",
    'prescriptions': "../HOSP/prescriptions.csv",

    # ICU files
    'icu_stays': "../ICU/icustays.csv",

    # Data files
    'icd10_codes': "../Data/diagnosis_icd10_codes.csv",
    'icd9_codes': "../Data/diagnosis_icd9_codes.csv"
}

# Other configurations
CONFIG = {
    'random_state': 42,
    'test_size': 0.2,
    'validation_size': 0.2,
}
```

### **Preprocessor Class**

The `Preprocessor` class in `preprocessing/preprocessor.py` is designed to preprocess all necessary MIMIC-IV tables. It handles tasks such as data loading, cleaning, merging, and feature engineering.

```python:src/preprocessing/preprocessor.py
import pandas as pd
from config import FILE_PATHS

class Preprocessor:
    def __init__(self, file_paths=FILE_PATHS):
        self.file_paths = file_paths

    def load_data(self, table_name):
        return pd.read_csv(self.file_paths[table_name])

    def preprocess_table(self, table_name):
        df = self.load_data(table_name)
        # Add preprocessing steps specific to the table
        return df

    def preprocess_all(self):
        self.edstays = self.preprocess_table('edstays')
        self.diagnosis = self.preprocess_table('diagnosis')
        self.triage = self.preprocess_table('triage')
        self.vitalsigns = self.preprocess_table('vitalsigns')
        self.admissions = self.preprocess_table('admissions')
        self.transfers = self.preprocess_table('transfers')
        self.patients = self.preprocess_table('patients')
        self.hosp_diagnosis = self.preprocess_table('hosp_diagnosis')
        self.prescriptions = self.preprocess_table('prescriptions')
        self.icu_stays = self.preprocess_table('icu_stays')
        # Add more tables if needed
```

## **Analysis Plan**

We will employ a variety of analytical techniques:

- **Descriptive Statistics**: Summarize key variables to validate data integrity and understand baseline characteristics.
- **Time Series Analysis**: Examine trends in ICU admissions, mortality rates, and resource utilization over time.
- **Comparative Analysis**: Compare hospital data against state and county-level statistics to identify unique patterns or deviations.
- **Survival Analysis**: Utilize time-to-event models to evaluate factors influencing patient length of stay and mortality.
- **Insurance Impact Analysis**: Investigate how insurance type and coverage levels correlate with patient outcomes and resource utilization.

## **Visualizations**

1. **ICU Admissions Over Time**: Line charts comparing ICU admissions for COVID-19 and non-COVID-19 patients across different years.
2. **Mortality Rates by Age Group**: Bar charts illustrating mortality rates among COVID-19 patients by age group.
3. **Antiviral Prescription Trends**: Visualization of antiviral medication prescriptions over time.
4. **Age Distribution Comparisons**: Histograms comparing age distributions of COVID-19 and non-COVID-19 patients.
5. **Insurance Coverage Impact**: Charts showing correlations between insurance types and patient outcomes.

## **Ethical Considerations**

- **Patient Privacy**: Strictly adhere to HIPAA regulations and data use agreements. Use de-identified data and ensure no re-identification risks.
- **Data Integrity**: Account for date shifts in MIMIC-IV data to maintain temporal accuracy in analyses.
- **Bias Mitigation**: Identify and correct biases related to demographics or socioeconomic status in data collection and analysis.

## **Contributions**

- **Jewels Hovan**:
  - Data cleaning and preprocessing, including handling of outliers and missing values.
  - Development of the `config.py` and `Preprocessor` class for streamlined data processing.
  - Creation of visualizations related to ICU dynamics and patient profiles.
- **Liu Liu**:
  - Research and integration of external datasets, focusing on GBD and insurance data.
  - Comparative analysis between hospital data and state/county statistics.
  - Analysis of mortality rates and demographic patterns.
- **George Mathew**:
  - Exploration and integration of insurance data.
  - Analysis of the impact of insurance coverage on patient outcomes and resource utilization.
  - Developed `InsuranceAnalysis.ipynb` for detailed exploration of Medicare data and its correlation with patient data.
  - Creation of visualizations related to insurance impact.

## **Changelog**

- **2023.10.10**:
  - **Updated**: Shifted project focus to COVID-19 impact analysis.
  - **Added**: New datasets and adjusted objectives to reflect the pandemic focus.
  - **Enhanced**: Included `config.py` and `Preprocessor` class details in the codebase section.
  - **Revised**: Analysis plan and visualizations to align with the new direction.

- **2023.10.05**:
  - **Updated**: Incorporated external datasets into the project scope.
  - **Added**: New objectives related to external data integration and insurance impact analysis.
  - **Revised**: Data cleaning section to include new feature engineering efforts.
  - **Expanded**: Contributions to reflect team members' current roles.
  - **Polished**: Improved document formatting and clarity.

## **Future Work**

- **Advanced Modeling**: Implement machine learning models to predict patient outcomes and resource needs during pandemics.
- **Further Data Collection**: Explore additional datasets, such as vaccination rates or socioeconomic indicators, to enrich analysis.
- **Deep Dive Analyses**: Investigate specific findings in more detail, such as the impact of insurance coverage on COVID-19 patient mortality.

## **References**

- [MIMIC-IV Documentation](https://mimic.mit.edu/docs/iv/)
- [CMS Medicare Enrollment Reports](https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment)
- [Global Health Data Exchange](https://ghdx.healthdata.org/gbd-results-tool)
- [WHO ICD-10 Classification](https://icd.who.int/browse10/2010/en)
- [CDC ICD-9 CM Browser](https://www.cdc.gov/nchs/icd/icd9cm.htm)
