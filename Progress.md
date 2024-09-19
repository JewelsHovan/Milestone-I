# Progress Tracker

## 1. Project Overview

This project focuses on analyzing electronic health records (EHR) from the MIMIC dataset to explore patient data, predict acuity levels, collect disease statistics, and analyze patient flow within healthcare facilities. The primary objectives include data preprocessing, exploratory data analysis (EDA), building and interpreting classification models, scraping disease categories, and understanding patient transfer patterns.

## 2. Data Collection

### a. Downloading MIMIC Data

- **Datasets Acquired:**
  - `edstays.csv` (Emergency Department Stays)
  - `admissions.csv` (Hospital Admissions)
  - `transfers.csv` (Patient Transfers)
  - `diagnosis.csv` (Diagnosis Information)
  - `triage.csv` (Triage Data)
  - `vitalsign.csv` (Vital Signs)
  - `medrecon.csv` (Medication Reconciliation)
  - `patients.csv` (Patient Demographics)

### b. Web Scraping ICD Codes

- **Objective:** Extract disease categories and their corresponding ICD-10 codes from the [WHO ICD-10 Browser](https://icd.who.int/browse10/2010/en#/XXII).
- **Tools Used:** Selenium for dynamic content loading and BeautifulSoup for parsing HTML.
- **Process:**
  - Navigated through each ICD-10 chapter.
  - Extracted chapter titles, ICD codes (first 3 characters/digits), and block titles.
  - Stored the scraped data in `disease_categories.csv`.

## 3. Data Preprocessing

### a. Preprocessing MIMIC Data (`src/preprocess.py`)

- **Implemented `PreprocessMIMIC` Class:**
  - **Methods:**
    - `print_info(df)`: Displays DataFrame shape, missing values, and unique counts for categorical columns.
    - `convert_to_datetime(df, cols)`: Converts specified columns to datetime objects.
    - `compute_length_of_stay(df, intime_col, outtime_col, prefix)`: Calculates Length of Stay (LOS) in hours.
    - `map_to_group(df, col, mapping, fill_na)`: Maps categorical values to broader groups and handles missing values.
    - `filter_outliers(df, col)`: Filters outliers using the Interquartile Range (IQR) method for specified numerical columns.

### b. Utility Functions (`src/utils.py`)

- **Functions:**
  - `nunique_per_cat(df)`: Returns the number of unique values for each categorical column.
  - `min_max_for_cols(df)`: Prints the minimum and maximum values for numerical columns.

## 4. Exploratory Data Analysis (EDA)

### a. EDA Notebook (`src/EDA.ipynb`)

- **Data Importing:**
  - Loaded all relevant CSV files into Pandas DataFrames.
- **Initial Exploration:**
  - Utilized `missingno` to visualize missing data patterns.
  - Analyzed unique values and distributions for categorical and numerical features.
- **Data Cleaning:**
  - Converted `intime` and `outtime` columns to datetime formats.
  - Calculated ED Length of Stay (`ed_los_hours`).
  - Mapped detailed race categories to broader groups using `race_mapping`.
- **Visualizations:**
  - Plotted distributions of vital signs and other continuous variables.
  - Explored racial disparities in ED length of stay.
- **Regression Analysis:**
  - Prepared data for regression models to interpret feature impacts on LOS.

## 5. Classification and Model Interpretation

### a. Classification Notebook (`src/Classification-Interpretation.ipynb`)

- **Data Preparation:**
  - Selected relevant features and target variable (`acuity`) for classification.
  - Split data into training and testing sets (80-20 split).
- **Preprocessing Pipeline:**
  - **Numerical Features:**
    - Imputed missing values using the mean.
    - Standardized features with `StandardScaler`.
  - **Categorical Features:**
    - Imputed missing values using the most frequent category.
    - Applied `OneHotEncoder` to convert categorical variables into numerical format.
- **Model Training:**
  - Trained a `RandomForestClassifier` with 300 estimators and a maximum depth of 4.
- **Model Evaluation:**
  - Achieved train and test accuracy scores of approximately 0.605 and 0.605 respectively.
  - Generated a classification report highlighting precision, recall, and F1-scores for each class.
- **Feature Importance:**
  - Identified and visualized the top 10 most important features influencing model predictions.

## 6. Disease Statistics Collection

### a. Data Collection Notebook (`src/DataCollection.ipynb`)

- **Objective:** Gather up-to-date statistics on various disease categories, including prevalence, incidence, mortality, and economic impact.
- **Process:**
  - **Web Scraping:**
    - Extracted disease categories and ICD codes from the WHO ICD-10 Browser.
    - Saved the data into `disease_categories.csv`.
  - **API Integration:**
    - Utilized OpenAI's API (via Perplexity) to fetch statistics for each disease category.
    - Structured system and user prompts to ensure responses are in valid JSON format.
    - Extracted and parsed JSON responses to compile a comprehensive DataFrame.
    - Stored the collected statistics in `disease_data.csv`.

## 7. Patient Flow Analysis

### a. Flow Analysis Notebook (`src/FlowAnalysis.ipynb`)

- **Data Loading:**
  - Imported `transfers.csv` and `patients.csv` into DataFrames.
- **Preprocessing:**
  - Converted `intime` and `outtime` columns to datetime formats.
  - Calculated Length of Stay (`los`) for each transfer.
- **Movement Summary:**
  - Grouped data by `subject_id` and `hadm_id` to summarize patient transfers.
  - Computed the number of transfers, total LOS, number of unique care units, and average time per unit.
- **Common Pathways Analysis:**
  - Identified and listed the most frequent patient pathways through various care units.
- **Visualizations:**
  - Plotted the distribution of the number of transfers per patient.
  - Analyzed the relationship between the number of transfers and total LOS using scatter plots.

## 8. Current Status

- **Completed:**
  - Data collection from MIMIC datasets and ICD-10 Browser.
  - Comprehensive data preprocessing and cleaning.
  - Conducted exploratory data analysis with insightful visualizations.
  - Developed and evaluated a Random Forest classification model for predicting patient acuity.
  - Collected detailed disease statistics via API integrations.
  - Analyzed patient transfer patterns and their impact on hospital LOS.

## 9. Next Steps

- **Model Improvement:**
  - Explore hyperparameter tuning and alternative classification algorithms to enhance model performance.
- **Integration:**
  - Combine disease statistics with clinical data for more enriched analyses.
- **Advanced Analytics:**
  - Implement regression models to further interpret factors affecting LOS.
  - Conduct longitudinal studies on patient outcomes based on transfer patterns.
- **Reporting:**
  - Compile findings into comprehensive reports and dashboards for stakeholders.
- **Automation:**
  - Automate data collection and preprocessing pipelines for scalability.

## 10. Challenges Encountered

- **Data Quality:** Handling missing values and outliers in large datasets posed significant challenges.
- **API Limitations:** Ensuring valid JSON responses from API integrations required meticulous prompt engineering.
- **Computational Resources:** Processing and analyzing extensive datasets necessitated efficient coding practices and resource management.

## 11. Lessons Learned

- **Importance of Preprocessing:** Effective data cleaning and feature engineering are crucial for building reliable models.
- **API Utilization:** Leveraging APIs for data enrichment can significantly enhance the scope of analysis.
- **Visualization Skills:** Clear and insightful visualizations aid in uncovering hidden patterns and informing decision-making.
