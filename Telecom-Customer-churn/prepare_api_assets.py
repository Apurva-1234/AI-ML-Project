import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import os


df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df.drop('customerID', axis=1, inplace=True)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'] = df['TotalCharges'].fillna(df['TotalCharges'].median())
df['SeniorCitizen'] = df['SeniorCitizen'].astype('object')
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})


df_encoded = pd.get_dummies(df, drop_first=True)
X = df_encoded.drop('Churn', axis=1)
y = df_encoded['Churn']


feature_columns = X.columns.tolist()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)


scaler = StandardScaler()
num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])


model = GradientBoostingClassifier(
    n_estimators=200, 
    learning_rate=0.1, 
    max_depth=4, 
    subsample=0.8, 
    random_state=42
)
model.fit(X_train, y_train)


if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/best_gradient_boosting_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(feature_columns, 'models/feature_columns.pkl')

print("API assets (model, scaler, feature_columns) saved to models/ directory.")
