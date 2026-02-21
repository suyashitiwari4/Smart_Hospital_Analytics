import pandas as pd
import numpy as np

patients = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/patients.csv")
admissions = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/admissions.csv")
billing = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/billing.csv")
doctors = pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/doctors.csv")

admissions['Admission_date'] = pd.to_datetime(admissions['Admission_date'])
admissions['Discharge_date'] = pd.to_datetime(admissions['Discharge_date'])

admissions['Length_of_stay'] = (
    admissions['Discharge_date'] - admissions['Admission_date']
).dt.days

df = (
    admissions
    .merge(patients, on="Patient_ID", how="left")
    .merge(billing, on="Admission_ID", how="left")
)
daily_admissions = (
    df.groupby(df['Admission_date'].dt.date)
    .size()
    .reset_index(name="Daily_Admissions")
)
daily_discharges=(
    df.groupby(df['Discharge_date'].dt.date).size().reset_index(name="Daily_Discharges")
)
bed_utilization=(df['Bed_type'].value_counts(normalize=True).reset_index())
bed_utilization.columns=['Bed_type',"Utilization_Percentage"]
bed_utilization['Utilization_Percentage']*=100

avg_los= df['Length_of_stay'].mean()#average length of stay

los_by_dept = (df.groupby('Department')['Length_of_stay'].mean().reset_index())
avg_patients_per_doctor = doctors['Patients_handled'].mean()
doctor_workload=(doctors.groupby('Department')['Patients_handled'].mean().reset_index())

revenue_by_dept = (
    df.groupby('Department')['Total_charges']
    .sum()
    .reset_index()
)
insurance_rejection_rate=(df['Claim_status'].value_counts(normalize=True)*100)
