# **Milestone I: Hospital Efficiency and Patient Flow Analysis**

## **Project Overview**
This project focuses on visualizing hospital inefficiencies by analyzing patient stays in the Emergency Department (ED) and Intensive Care Unit (ICU). Our goal is to identify correlations between the severity of medical emergencies and patient length of stay. By understanding these relationships, we aim to discover patterns of resource overuse or potential bottlenecks in hospital operations, particularly those leading to unnecessary extended stays. Minimizing these inefficiencies could help hospitals better allocate resources, improve patient care, and reduce healthcare costs.

The project involves merging data from multiple sources, cleaning it, and performing in-depth analysis to extract insights that would not be possible using any one dataset in isolation.

## **Team Members**
- **Jewels Hovan** (jhovan)
- **Liu Liu** (luvul)

## **Datasets**
We are working with publicly available datasets from the **MIMIC-IV** database, which contains real hospital stay data for patients. Specifically, we are using the following datasets:

### **Primary Dataset: Hospital Admissions (MIMIC-IV)**
- **Description**: Contains records of hospital admissions, including admit/discharge times, admission types, and ED registration/discharge times.
- **Size**: ~550,000 records
- **Access Method**: CSV file from the MIMIC-IV database
- **Source**: [MIMIC-IV Admissions Table](https://mimic.mit.edu/docs/iv/modules/hosp/admissions/)

### **Secondary Dataset: Triage & Diagnosis (MIMIC-IV ED Module)**
- **Description**: Includes triage vital signs and ICD-10 diagnosis codes, detailing patient severity and medical conditions upon arrival at the ED.
- **Size**: 
  - Triage: ~425,000 records
  - Diagnosis: ~90,000 records
- **Access Method**: CSV files from the MIMIC-IV ED module
- **Source**: 
  - [Triage Table](https://mimic.mit.edu/docs/iv/modules/ed/triage/)
  - [Diagnosis Table](https://mimic.mit.edu/docs/iv/modules/ed/diagnosis/)

## **Project Objectives**
- **Visualize patient flow**: We will create detailed flow diagrams (e.g., Sankey diagrams) to illustrate patient pathways from ED admission through ICU stays and discharge.
- **Resource utilization analysis**: We aim to analyze resource usage, focusing on identifying bottlenecks and inefficiencies in patient management. This includes time-series analysis to highlight peak periods of bed occupancy.
- **Explore correlations**: Investigate whether injury severity (via the ESI triage system) directly correlates with hospital stay length. We hypothesize that more severe injuries lead to longer hospital stays.

## **Data Cleaning and Manipulation**
- **Outlier Removal**: The data contains extreme outliers, such as unrealistically high heart rates and temperatures. We will clean these by either removing or imputing values based on valid medical ranges.
- **Handling Missing Data**: Missing values will be addressed through data imputation techniques, possibly employing machine learning models to estimate the missing values.
- **Feature Engineering**: We will derive new features, such as time intervals between key hospital events (e.g., ED arrival to ICU transfer) and patient risk scores based on vital signs and initial diagnoses.
- **Text Data Processing**: Self-reported features like "pain" and "chief complaint" will be grouped using natural language processing (NLP) techniques to reduce dimensionality and improve interpretability.

## **Analysis Plan**
We will use a variety of data analysis techniques:
- **Descriptive Statistics**: Summarize key variables (e.g., patient age, injury severity, length of stay) and provide sanity checks using mean, median, and distribution visualizations.
- **Correlation and Hypothesis Testing**: Investigate potential correlations between patient severity, length of stay, and resource allocation.
- **Survival Analysis**: Evaluate factors that influence patient length of stay, accounting for censored data (i.e., patients not yet discharged).
  
## **Visualizations**
1. **Sankey Diagram**: To visualize patient movement through the hospital system from admission to discharge, highlighting transitions between departments (ED, ICU, surgery).
2. **Heatmap**: To display bed occupancy rates over time, identifying peak usage periods and visualizing patient flow against staffing levels.

## **Ethical Considerations**
- **Patient Privacy**: The MIMIC-IV data is de-identified in accordance with HIPAA standards. We will ensure that no sensitive information is included in our analysis.
- **Bias Mitigation**: We will check for demographic biases in patient admissions and treatments and ensure that analyses and models do not perpetuate bias.

## **Contributions**
- **Jewels Hovan**: Data cleaning, triage data analysis, and Sankey diagram creation.
- **Liu Liu**: ICU data analysis, resource utilization analysis, and visualizations.

## **Changelog**
- **2022.07.27.1.CT**: Initial project proposal for SIADS 593.
- **2021.07.24.1.AW**: Adjusted title, added number sections, simplified section headings, and edited text.
