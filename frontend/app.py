import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# API base URL (from Flask/FastAPI)
API_URL = "http://your_backend_api_url_here"

# User Authentication
def user_login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid credentials")
            return False

# Fetch and display budget overview
def budget_overview():
    st.subheader("Budget Overview")
    response = requests.get(f"{API_URL}/budget")
    if response.status_code == 200:
        budget_data = response.json()
        df = pd.DataFrame(budget_data)
        # Create a line chart for visualizing monthly expenses
        fig = px.line(df, x="age", y=["housing", "food", "tuition"], title="Budget Overview by Age")
        st.plotly_chart(fig)

# Fetch and display spending statistics
def spending_statistics():
    st.subheader("Spending Statistics by Category")
    response = requests.get(f"{API_URL}/spending")
    if response.status_code == 200:
        spending_data = response.json()
        df = pd.DataFrame(spending_data)
        fig = px.pie(df, values="total_spending", names="category", title="Spending by Category")
        st.plotly_chart(fig)

# Display individual student spending breakdown
def student_spending():
    st.subheader("Student Spending Breakdown")
    response = requests.get(f"{API_URL}/student_spending")
    if response.status_code == 200:
        spending_data = response.json()
        df = pd.DataFrame(spending_data)
        
        # Create a dropdown to select the student ID and view their expenses
        student_id = st.selectbox("Select Student ID", df.index)
        student_data = df.loc[student_id]

        st.write(f"Major: {student_data['major']}")
        st.write(f"Year in School: {student_data['year_in_school']}")
        st.write(f"Monthly Income: ${student_data['monthly_income']}")

        # Visualize the student's spending across categories
        categories = ["tuition", "housing", "food", "transportation", "books_supplies", "entertainment"]
        fig = px.bar(student_data[categories], x=categories, y=student_data[categories].values, 
                     title=f"Spending Breakdown for Student {student_id}")
        st.plotly_chart(fig)

# Main function to render the app
def main():
    st.title("PennyWise - Financial AI Assistant")
    if user_login():
        st.sidebar.title("Dashboard")
        option = st.sidebar.selectbox("Select Dashboard", ["Budget Overview", "Spending Statistics", "Student Spending Breakdown"])
        
        if option == "Budget Overview":
            budget_overview()
        elif option == "Spending Statistics":
            spending_statistics()
        elif option == "Student Spending Breakdown":
            student_spending()

if __name__ == "__main__":
    main()
