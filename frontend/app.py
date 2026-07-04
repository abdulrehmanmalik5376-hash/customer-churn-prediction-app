import streamlit as st
import pandas as pd
import requests

API_URL = "https://customer-churn-api.onrender.com"
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Customer Churn Prediction System")
st.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Single Prediction",
        "📂 Batch Prediction"
    ]
)

# ===========================
# HOME PAGE
# ===========================

if menu == "🏠 Home":

    st.header("Welcome")

    st.write("""
This project predicts whether a customer is likely to leave the company.

### Features

✅ FastAPI Backend

✅ Random Forest Model

✅ Single Prediction

✅ Batch Prediction

✅ Download Prediction CSV
""")

    st.info("Select an option from the left sidebar.")

# ===========================
# SINGLE PREDICTION
# ===========================

elif menu == "🔍 Single Prediction":

    st.header("Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            [0,1],
            format_func=lambda x: "Female" if x==0 else "Male"
        )

        senior = st.selectbox(
            "Senior Citizen",
            [0,1]
        )

        partner = st.selectbox(
            "Partner",
            [0,1]
        )

        dependents = st.selectbox(
            "Dependents",
            [0,1]
        )

        tenure = st.number_input(
            "Tenure Months",
            0,
            100,
            12
        )

        phone = st.selectbox(
            "Phone Service",
            [0,1]
        )

        multiple = st.selectbox(
            "Multiple Lines",
            [0,1,2]
        )

        internet = st.selectbox(
            "Internet Service",
            [0,1,2]
        )

        security = st.selectbox(
            "Online Security",
            [0,1,2]
        )

        backup = st.selectbox(
            "Online Backup",
            [0,1,2]
        )

    with col2:

        device = st.selectbox(
            "Device Protection",
            [0,1,2]
        )

        support = st.selectbox(
            "Tech Support",
            [0,1,2]
        )

        tv = st.selectbox(
            "Streaming TV",
            [0,1,2]
        )

        movies = st.selectbox(
            "Streaming Movies",
            [0,1,2]
        )

        contract = st.selectbox(
            "Contract",
            [0,1,2]
        )

        paper = st.selectbox(
            "Paperless Billing",
            [0,1]
        )

        payment = st.selectbox(
            "Payment Method",
            [0,1,2,3]
        )

        monthly = st.number_input(
            "Monthly Charges",
            0.0,
            200.0,
            70.0
        )

        total = st.number_input(
            "Total Charges",
            0.0,
            10000.0,
            1000.0
        )
    if st.button("🔍 Predict Customer Churn"):

        customer = {

            "Gender": gender,
            "Senior_Citizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "Tenure_Months": tenure,
            "Phone_Service": phone,
            "Multiple_Lines": multiple,
            "Internet_Service": internet,
            "Online_Security": security,
            "Online_Backup": backup,
            "Device_Protection": device,
            "Tech_Support": support,
            "Streaming_TV": tv,
            "Streaming_Movies": movies,
            "Contract": contract,
            "Paperless_Billing": paper,
            "Payment_Method": payment,
            "Monthly_Charges": monthly,
            "Total_Charges": total

        }

        try:

            response = requests.post(
                API_URL + "/predict",
                json=customer,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.success("Prediction Completed Successfully")

                st.metric(
                    "Prediction",
                    "Churn" if result["Prediction"] == 1 else "No Churn"
                )

                st.metric(
                    "Probability",
                    f'{result["Probability"]*100:.2f}%'
                )

                st.metric(
                    "Risk Level",
                    result["Risk_Level"]
                )

            else:

                st.error(response.text)

        except Exception as e:

            st.error(f"Connection Error : {e}")



# =====================================
# BATCH PREDICTION
# =====================================

elif menu == "📂 Batch Prediction":

    st.header("Batch Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        if st.button("Predict CSV"):

            try:

                files = {

                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )

                }

                response = requests.post(
                    API_URL + "/predict-batch",
                    files=files,
                    timeout=60
                )

                if response.status_code == 200:

                    result = response.json()

                    df = pd.DataFrame(result)

                    st.success("Prediction Completed")

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    csv = df.to_csv(
                        index=False
                    ).encode("utf-8")

                    st.download_button(

                        label="Download Prediction CSV",

                        data=csv,

                        file_name="prediction.csv",

                        mime="text/csv"

                    )

                else:

                    st.error(response.text)

            except Exception as e:

                st.error(e)