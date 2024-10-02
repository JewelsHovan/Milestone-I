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
    "prescriptions": "../HOSP/prescriptions.csv",

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

# API keys (consider using environment variables for sensitive information)
API_KEYS = {
    'openai': os.environ.get('OPENAI_API_KEY'),
    'perplexity': os.environ.get('PERPLEXITY_API_KEY'),
}

DISEASE_CATEGORY_MAPPING = {
    # ICD-10 mappings
    'Certain infectious and parasitic diseases': 'Infectious & Parasitic',
    'Neoplasms': 'Neoplasms',
    'Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism': 'Blood & Immune System',
    'Endocrine, nutritional and metabolic diseases': 'Endocrine & Metabolic',
    'Mental and behavioural disorders': 'Mental & Behavioral',
    'Diseases of the nervous system': 'Nervous System',
    'Diseases of the eye and adnexa': 'Eye & Adnexa',
    'Diseases of the ear and mastoid process': 'Ear & Mastoid',
    'Diseases of the circulatory system': 'Circulatory System',
    'Diseases of the respiratory system': 'Respiratory System',
    'Diseases of the digestive system': 'Digestive System',
    'Diseases of the skin and subcutaneous tissue': 'Skin & Subcutaneous',
    'Diseases of the musculoskeletal system and connective tissue': 'Musculoskeletal & Connective',
    'Diseases of the genitourinary system': 'Genitourinary System',
    'Pregnancy, childbirth and the puerperium': 'Pregnancy & Childbirth',
    'Certain conditions originating in the perinatal period': 'Perinatal Conditions',
    'Congenital malformations, deformations and chromosomal abnormalities': 'Congenital & Chromosomal',
    'Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified': 'Symptoms & Abnormal Findings',
    'Injury, poisoning and certain other consequences of external causes': 'Injury & Poisoning',
    'External causes of morbidity and mortality': 'External Causes',
    'Factors influencing health status and contact with health services': 'Health Factors & Services',
    'Codes for special purposes': 'Special Purposes',
    
    # ICD-9 mappings
    'Infectious And Parasitic Diseases': 'Infectious & Parasitic',
    'Neoplasms': 'Neoplasms',
    'Endocrine, Nutritional And Metabolic Diseases, And Immunity Disorders': 'Endocrine & Metabolic',
    'Diseases Of Blood And Blood-Forming Organs': 'Blood & Immune System',
    'Mental Disorders': 'Mental & Behavioral',
    'Diseases Of The Nervous System And Sense Organs': 'Nervous System',
    'Diseases Of The Circulatory System': 'Circulatory System',
    'Diseases Of The Respiratory System': 'Respiratory System',
    'Diseases Of The Digestive System': 'Digestive System',
    'Diseases Of The Genitourinary System': 'Genitourinary System',
    'Complications Of Pregnancy, Childbirth, And The Puerperium': 'Pregnancy & Childbirth',
    'Diseases Of The Skin And Subcutaneous Tissue': 'Skin & Subcutaneous',
    'Diseases Of The Musculoskeletal System And Connective Tissue': 'Musculoskeletal & Connective',
    'Congenital Anomalies': 'Congenital & Chromosomal',
    'Certain Conditions Originating In The Perinatal Period': 'Perinatal Conditions',
    'Symptoms, Signs, And Ill-Defined Conditions': 'Symptoms & Abnormal Findings',
    'Injury And Poisoning': 'Injury & Poisoning'
}

# Define a mapping for careunit categories
CAREUNIT_MAPPING = {
    'Emergency Department': 'Emergency Department',
    'Emergency Department Observation': 'Emergency Department',
    'Medical Intensive Care Unit (MICU)': 'Intensive Care Unit (ICU)',
    'Surgical Intensive Care Unit (SICU)': 'Intensive Care Unit (ICU)',
    'Cardiac Vascular Intensive Care Unit (CVICU)': 'Intensive Care Unit (ICU)',
    'Coronary Care Unit (CCU)': 'Intensive Care Unit (ICU)',
    'Neuro Surgical Intensive Care Unit (Neuro SICU)': 'Intensive Care Unit (ICU)',
    'Intensive Care Unit (ICU)': 'Intensive Care Unit (ICU)',
    'Trauma SICU (TSICU)': 'Intensive Care Unit (ICU)',
    'Cardiology Surgery Intermediate': 'Intermediate Care',
    'Medical/Surgical Intensive Care Unit (MICU/SICU)': 'Intermediate Care',
    'Hematology/Oncology Intermediate': 'Intermediate Care',
    'Medicine/Cardiology Intermediate': 'Intermediate Care',
    'Neuro Intermediate': 'Intermediate Care',
    'Surgical Intermediate': 'Intermediate Care',
    'Medicine': 'General Medicine/Surgery',
    'Med/Surg': 'General Medicine/Surgery',
    'Surgery/Trauma': 'General Medicine/Surgery',
    'Med/Surg/GYN': 'General Medicine/Surgery',
    'Med/Surg/Trauma': 'General Medicine/Surgery',
    'Surgery': 'General Medicine/Surgery',
    'Surgery/Pancreatic/Biliary/Bariatric': 'General Medicine/Surgery',
    'Surgery/Vascular/Intermediate': 'General Medicine/Surgery',
    'Transplant': 'Specialty Units',
    'Thoracic Surgery': 'Specialty Units',
    'Vascular': 'Specialty Units',
    'Labor & Delivery': 'Specialty Units',
    'Obstetrics (Postpartum & Antepartum)': 'Specialty Units',
    'Neurology': 'Specialty Units',
    'Psychiatry': 'Specialty Units',
    'Hematology/Oncology': 'Specialty Units',
    'Oncology': 'Specialty Units',
    'Cardiology': 'Specialty Units',
    'Discharge Lounge': 'Observation/Other',
    'PACU': 'Observation/Other',
    'Observation': 'Observation/Other',
    'Obstetrics Postpartum': 'Observation/Other',
    'Obstetrics Antepartum': 'Observation/Other',
    'Neuro Stepdown': 'Observation/Other',
    'Nursery': 'Observation/Other',
    'Special Care Nursery (SCN)': 'Observation/Other',
    'Unknown': 'Observation/Other',
    'UNKNOWN': 'Observation/Other'
}
