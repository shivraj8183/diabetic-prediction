import streamlit as st
import pandas as pd
import pickle as pkl

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🩺 Diabetes Predictor",
    page_icon="🧬",
    layout="centered"
)

# ---------------- LOAD MODEL ----------------
scaler = pkl.load(open('scaler.pkl', 'rb'))
model = pkl.load(open('model.pkl', 'rb'))

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.main {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 15px;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #4A00E0;
}
.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 25px;
}
.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #00c6ff, #0072ff);
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<div class="title">🩺 Diabetes Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Health Risk Analysis</div>', unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("👤 Gender", ['Female', 'Male', 'Other'])
    age = st.number_input("🎂 Age", min_value=0, max_value=100, value=50)
    hypertension = st.selectbox("💓 Hypertension", ["Yes", "No"])
    heart_disease = st.selectbox("❤️ Heart Disease", ["Yes", "No"])

with col2:
    smoking_history = st.selectbox("🚬 Smoking History", ['never', 'No Info', 'former', 'not current', 'ever', 'current'])
    bmi = st.number_input("⚖️ BMI", min_value=20, max_value=50, value=28)
    HbA1c_level = st.number_input("🧪 HbA1c Level", min_value=5.0, max_value=10.0, value=6.6, step=0.1)
    blood_glucose_level = st.number_input("🩸 Blood Glucose", min_value=25, max_value=500, value=200)

# ---------------- ENCODING ----------------
if gender == 'Female':
    gender = 0
elif gender == 'Male':
    gender = 1
else:
    gender = 2

if smoking_history == 'never':
    smoking_history = 0
elif smoking_history == 'No Info':
    smoking_history = 1
elif smoking_history in ['former', 'not current']:
    smoking_history = 2
elif smoking_history == 'ever':
    smoking_history = 3
else:
    smoking_history = 4

hypertension = 1 if hypertension == "Yes" else 0
heart_disease = 1 if heart_disease == "Yes" else 0

# ---------------- PREDICTION ----------------
if st.button("🔍 Predict Now"):
    myinput = [[gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level]]
    columns = ['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    
    data = pd.DataFrame(data=myinput, columns=columns)
    data_scaled = scaler.transform(data)
    result = model.predict(data_scaled)

    st.markdown("---")

    if result[0] == 1:
        st.error("⚠️ High Risk: Person is Diabetic")
    else:
        st.success("✅ Low Risk: Person is Not Diabetic")
