import streamlit as st
import requests

# Collect user data
budget = st.number_input("Enter your monthly budget")
expenses = st.number_input("Enter your monthly expenses")

if st.button("Analyze my finances"):
    # Send request to Databricks API
    response = requests.post(
        "https://databricks-api-endpoint.com/analyze",
        json={"budget": budget, "expenses": expenses}
    )

    if response.status_code == 200:
        analysis_result = response.json()
        st.write("Analysis Result:", analysis_result)
    else:
        st.write("Error fetching analysis.")
