import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Fraud Detection", page_icon=":shield:", layout="centered")

st.title("🛡️ Fraud Detection Predictor")
st.write("Upload a CSV file with your transaction data to predict fraud using the trained model.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    if st.button("Predict Fraud"):
        with st.spinner("Predicting..."):
            uploaded_file.seek(0)
            files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
            try:
                response = requests.post("http://localhost:5000/predict", files=files)
                if response.status_code == 200:
                    try:
                        preds = response.json().get('predictions', [])
                        # If preds is a list of dicts, extract predictions and anomaly_scores
                        if preds and isinstance(preds[0], dict):
                            preds_list = [p['prediction'] for p in preds]
                            scores_list = [p['anomaly_score'] for p in preds]
                            # Only keep as many rows as predictions
                            result_df = df.iloc[:len(preds_list)].copy()
                            result_df['Prediction'] = preds_list
                            result_df['Anomaly Score'] = scores_list
                        else:
                            # fallback for old API
                            result_df = df.copy()
                            result_df['Prediction'] = preds
                        st.subheader("Prediction Results")
                        st.dataframe(result_df)
                        st.success("Prediction completed!")
                    except Exception as e:
                        st.error(f"Error parsing prediction response: {e}")
                else:
                    try:
                        error_msg = response.json().get('error', 'Unknown error')
                    except Exception:
                        error_msg = response.text
                    st.error(f"Error: {error_msg}")
            except Exception as e:
                st.error(f"Failed to connect to prediction server: {e}")
else:
    st.info("Please upload a CSV file to get started.")

st.markdown("""
<style>
    .stButton>button {
        color: white;
        background: #4F8BF9;
    }
    .stDataFrame { background: #f9f9f9; }
</style>
""", unsafe_allow_html=True)
