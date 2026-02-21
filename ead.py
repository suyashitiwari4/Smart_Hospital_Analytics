import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")
# Load the datasets
patients=pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/patients.csv")
admissions=pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/admissions.csv")
doctors=pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/doctors.csv")
billing=pd.read_csv("C:/Users/asus/OneDrive/Desktop/.vscode/.project/data/billing.csv")

print(patients.head())
print(admissions.head())

print(patients.info())
print(patients.describe())
print(patients.isnull().sum())

admissions['Admission_date'] = pd.to_datetime(admissions['Admission_date'])
admissions['Discharge_date'] = pd.to_datetime(admissions['Discharge_date'])

admissions['Length_of_stay'] = (
    admissions['Discharge_date'] - admissions['Admission_date']
).dt.days
admissions = admissions[admissions['Length_of_stay'] > 0]#filtering out erroneous data where discharge date is before admission date
print(admissions['Length_of_stay'].describe())

# Merge datasets for comprehensive analysis
df= (admissions.merge(patients, on='Patient_ID',how="left")
    .merge(billing, on='Admission_ID',how="left"))
print(df.head())
print(df.info())

#EDA
plt.figure(figsize=(8,4))
sns.histplot(df['Age'], bins=30, kde=True)
plt.title("Patient Age Distribution")
plt.show()

plt.figure(figsize=(8,4))
sns.countplot(data=df, x='Department')
plt.xticks(rotation=45)
plt.title("Admissions by Department")
plt.show()

df['Bed_type'].value_counts(normalize=True) * 100

plt.figure(figsize=(6,4))
sns.boxplot(x='readmitted_30_days', y='Length_of_stay', data=df)
plt.title("Length of Stay vs Readmission")
plt.show()

plt.figure(figsize=(8,4))
sns.histplot(df['Total_charges'], bins=30, kde=True)
plt.title("Hospital Charges Distribution")
plt.show()

df['Claim_status'].value_counts(normalize=True) * 100
