import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager

# Initialize Google Cloud Secret Manager client
def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = 'regal-cursor-395010'
    secret_version = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=secret_version)
    return response.payload.data.decode('UTF-8')

# Retrieve the Firebase credentials from Secret Manager
firebase_credentials_json = get_secret("firebase-credentials")

# Initialize Firebase if it hasn't been initialized yet
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials_json)  # Use the credentials from Secret Manager
    firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

# Streamlit App Layout
st.title("Assets")

# Input Fields
st.subheader("Enter your asset values")

# Equity Input
st.markdown("## Equity")
equity = st.number_input("Equity", label_visibility="hidden", min_value=0.0, step=1.0, key="equity_input")

# Real Estate Inputs with Dynamic Row Addition
st.subheader("Real Estate Assets")
real_estate_values = []
add_real_estate = st.button("Add Real Estate Row")

if "real_estate_values" not in st.session_state:
    st.session_state["real_estate_values"] = []

if add_real_estate:
    st.session_state["real_estate_values"].append(0.0)

# Display each Real Estate row input
for i in range(len(st.session_state["real_estate_values"])):
    st.session_state["real_estate_values"][i] = st.number_input(f"Real Estate Value {i+1}", key=f"real_estate_{i}")

# Passive Income Assets
st.markdown("## Passive Income Assets")
passive_income = st.number_input("Passive", label_visibility="hidden", min_value=0.0, step=1.0, key="passive_income_inputs")

# Debt
st.markdown("## Debt")
debt = st.number_input("Debt", label_visibility="hidden", min_value=0.0, step=1.0, key="debt")

# Alternative Investments
st.markdown("## Alternative Investments")
alternative_investments = st.number_input("Alt investments", label_visibility="hidden", min_value=0.0, step=1.0, key="alternative_investments")

# Submit Button
if st.button("Submit"):
    # Gather all data for submission
    finance_data = {
        "equity": equity,
        "real_estate": st.session_state["real_estate_values"],
        "passive_income": passive_income,
        "debt": debt,
        "alternative_investments": alternative_investments
    }

    # Store the data in Firebase Firestore
    try:
        db.collection("finance_data").add(finance_data)
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"An error occurred while saving data: {e}")
