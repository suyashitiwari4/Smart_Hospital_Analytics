import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier #randomforestclassifier is used for classification tasks
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,# for detailed classification metrics
    roc_auc_score,# to compute the Area Under the Receiver Operating Characteristic Curve 
    confusion_matrix # to evaluate the performance of classification models
)
# Load the datasets
patients = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\.vscode\\.project\\data\\patients.csv")
admissions = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\.vscode\\.project\\data\\admissions.csv")
billing = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\.vscode\\.project\\data\\billing.csv")

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
# Feature Engineering
X= df[
    ['Age',
     'Gender',
     'Chronic_conditions',
     'Admission_type',
     'Department',
     'Bed_type',
     'Length_of_stay',
     'Insurance_covered'
    ]
]
y= df['readmitted_30_days']
X= pd.get_dummies(X, drop_first=True)
X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42, stratify=y)
# Model Training and Evaluation
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
#evaluate logistic regression
lr_preds=lr_model.predict(X_test)
lr_probs= lr_model.predict_proba(X_test)[:,1] #probabilities for the positive class

print("Logistic Regression Results")
print(classification_report(y_test,lr_preds))
print("ROC-AUC:", roc_auc_score(y_test, lr_probs))
#interpret logistic regression
coefficients = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': lr_model.coef_[0]
})
print(coefficients.sort_values(by='Coefficient',  ascending=False))

# Random Forest Classifier
rf_model= RandomForestClassifier(
    n_estimators=2000,#number of trees in the forest
    max_depth=8,#ddepth of each tree
    random_state=42#for reproducibility
)
rf_model.fit(X_train,y_train)
#evaluate random forest
rf_preds = rf_model.predict(X_test)
rf_probs = rf_model.predict_proba(X_test)[:, 1]

print("Random Forest Results")
print(classification_report(y_test, rf_preds))
print("ROC-AUC:", roc_auc_score(y_test, rf_probs))
#interpret random forest
feature_importance = pd.DataFrame({
    'feature':X.columns,
    'Importance':rf_model.feature_importances_

})
print(feature_importance.sort_values(by='Importance', ascending=False))
#model comparison
model_comparision = pd.DataFrame({
    'Model':['Logistic Regression','Random Forest'],
    'ROC_AUC':[
        roc_auc_score(y_test,lr_probs),
        roc_auc_score(y_test,rf_probs)
    ]
})
print(model_comparision)