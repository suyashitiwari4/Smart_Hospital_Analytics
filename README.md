# Hospital Analytics Dashboard

A full-stack data analytics and machine learning project built with Python and Streamlit that provides actionable healthcare insights through interactive visualizations, KPI tracking, and predictive modeling.

# Project Overview

This project simulates a real hospital environment with synthetic data and delivers end-to-end analytics — from raw data generation to ML-based readmission prediction — all visualized through an interactive web dashboard.

# Project Structure

hospital-analytics/
│
├── data/                          # Auto-generated CSV datasets
│   ├── patients.csv
│   ├── admissions.csv
│   ├── billing.csv
│   └── doctors.csv
│
├── hospital_data.py               #  Data generation script
├── ead.py                         #  Exploratory Data Analysis (EDA)
├── hospital_operation_kpi.py      #  KPI computation script
├── readmission_prediction.py      #  ML prediction models
├── app.py                         #  Streamlit dashboard (main app)
└── README.md

# Features

<img width="766" height="698" alt="image" src="https://github.com/user-attachments/assets/c720f35f-cf05-4a5e-97bd-db3e163cda0f" />

# Machine Learning

Logistic Regression and Random Forest Classifier for 30-day readmission prediction

Feature engineering from patient demographics, clinical, and billing data

Model comparison using ROC-AUC score

Feature importance analysis

# Dataset Overview
Synthetic data generated with numpy seed 42 for reproducibility:

<img width="766" height="405" alt="image" src="https://github.com/user-attachments/assets/05dcdde6-dc6e-4147-a50e-e9b109a5d94e" />

# ML Model Results

Target: readmitted_30_days (binary classification)

Features used: Age, Gender, Chronic Conditions, Admission Type, Department, Bed Type, Length of Stay, Insurance

<img width="769" height="278" alt="image" src="https://github.com/user-attachments/assets/a2b08f48-2de7-4c21-b632-6c7a16246d7b" />

# Key KPIs Tracked

Total Admissions & Unique Patients

Average Length of Stay (LOS)

30-Day Readmission Rate

ICU Bed Utilization %

Revenue by Department

Insurance Coverage & Claim Approval Rate

Doctor Workload (avg patients per doctor)

 # Conclusion
 
This project demonstrates a complete data science pipeline applied to the healthcare domain — from synthetic data generation and EDA to interactive dashboarding and machine learning. It reflects practical skills in data engineering, visualization, and predictive analytics, simulating real-world hospital operations monitoring.




