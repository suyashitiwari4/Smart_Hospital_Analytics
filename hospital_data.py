import pandas as pd
import numpy as np 
from datetime import timedelta
import random #for generating random values
import os
os.makedirs("data", exist_ok=True)


np.random.seed(42) #for reproducibility

NUM_PATIENTS=500
NUM_ADMISSIONS=1000
NUM_DOCTORS=65
departments=['Cardiology','Neurology','General Medicine','Orthopedics','Emergency','Gynecology','Dermatology','Psychiatry','Radiology']
bed_types=['General','ICU']
admission_types=['Emergency','OPD']
genders=['Male','Female','Other']
claim_statuses=['Approved','Elected']
patients = pd.DataFrame({
    'Patient_ID':range(1,NUM_PATIENTS +1),
    'Age':np.random.randint(0,90,NUM_PATIENTS),
    'Gender':np.random.choice(genders,NUM_PATIENTS),
    'Chronic_conditions':np.random.randint(0,4,NUM_PATIENTS),
    'Admission_type':np.random.choice(admission_types,NUM_PATIENTS)
})
patients.to_csv("data/patients.csv", index=False)

admissions_ids = range(1,NUM_ADMISSIONS +1)
patient_ids=np.random.choice(patients['Patient_ID'],NUM_ADMISSIONS)
admission_dates=pd.to_datetime('2025-01-01')+ pd.to_timedelta(np.random.randint(0,365,NUM_ADMISSIONS),unit='D')#random dates in 2025
discharge_dates= admission_dates + pd.to_timedelta(np.random.randint(1,15,NUM_ADMISSIONS),unit='D')
admissions = pd.DataFrame({
    'Admission_ID':admissions_ids,
    'Patient_ID':patient_ids,
    'Admission_date':admission_dates,
    'Discharge_date':discharge_dates,
    'Department':np.random.choice(departments,NUM_ADMISSIONS),
    'Bed_type':np.random.choice(bed_types,NUM_ADMISSIONS,p=[0.3 ,0.7]),#70% General, 30% ICU
    'readmitted_30_days': np.random.choice([0, 1], NUM_ADMISSIONS, p=[0.75, 0.25]) # 25% readmitted within 30 days
})
admissions.to_csv("data/admissions.csv", index=False)

doctors = pd.DataFrame({
    'Doctor_ID':range(1,NUM_DOCTORS +1),
    'Department':np.random.choice(departments,NUM_DOCTORS),
    'Patients_handled':np.random.randint(50,300,NUM_DOCTORS),
    'Avg_consult_time':np.random.randint(5,30,NUM_DOCTORS) #in minutes
})
doctors.to_csv("data/doctors.csv", index=False)

billing = pd.DataFrame({
    'Admission_ID':admissions['Admission_ID'],
    'Total_charges':np.random.randint(500,20000,NUM_ADMISSIONS),
    'Insurance_covered':np.random.choice(['Yes','No'],NUM_ADMISSIONS,p=[0.6,0.4]),
    'Claim_status':np.random.choice(claim_statuses,NUM_ADMISSIONS,p=[0.8,0.2])
})
billing.to_csv("data/billing.csv", index=False)
print("Hospital data generated and saved to CSV files.")