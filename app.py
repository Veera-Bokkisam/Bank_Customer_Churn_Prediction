import streamlit as st
import joblib
import numpy as np

# Load model & preprocessor
model = joblib.load("../models/xgb_model.pkl")
preprocessor = joblib.load("../models/preprocessor.pkl")

st.set_page_config(page_title="Bank Customer Churn Prediction", layout="centered")

st.title("🏦 Bank Customer Churn Prediction")
st.write("Fill the customer details below to predict if they are likely to churn.")

# Input fields
credit_score = st.number_input("Credit Score", 300, 900, 650)
age = st.number_input("Age", 18, 100, 35)
tenure = st.number_input("Tenure (Years with Bank)", 0, 10, 5)
balance = st.number_input("Balance", 0.0, 300000.0, 50000.0)
num_products = st.selectbox("Number of Products", [1,2,3,4])
has_cr_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
is_active = st.selectbox("Is Active Member?", ["Yes", "No"])
estimated_salary = st.number_input("Estimated Salary", 0.0, 200000.0, 50000.0)

geography = st.selectbox("Geography", ["France", "Spain", "Germany"])
gender = st.selectbox("Gender", ["Male", "Female"])

# Convert Yes/No to 1/0
has_cr_card = 1 if has_cr_card == "Yes" else 0
is_active = 1 if is_active == "Yes" else 0

# Prepare DataFrame
import pandas as pd
data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Geography': [geography],
    'Gender': [gender],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active],
    'EstimatedSalary': [estimated_salary]
})

if st.button("Predict Churn"):
    processed_data = preprocessor.transform(data)
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0][1]

    if prediction == 1:
        st.error(f"⚠️ Customer is LIKELY to CHURN. (Probability: {probability:.2f})")
    else:
        st.success(f"✅ Customer is NOT likely to churn. (Probability: {probability:.2f})")