import streamlit as st
import pandas as pd
import requests  # Used if fetching from Databricks API
import plotly as px  # For visualization

# Backend endpoint or file location for analyzed data
DATA_BACKEND_URL = "https://your-databricks-backend.com/financial-data"  # Replace with actual URL

# Function to fetch data from the backend (replace this with actual Databricks integration)
def fetch_data():
    try:
        response = requests.get(DATA_BACKEND_URL)
        if response.status_code == 200:
            # Assuming the backend returns data in CSV format
            data = pd.read_csv(response.content)
            return data
        else:
            st.error("Failed to fetch data from the backend")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

# Simulating data loading for this example
@st.cache
def load_data():
    # You can replace this with `fetch_data()` once connected to the backend
    data = pd.read_csv("financial_data.csv")  # Local data for demo
    return data

# Calculate available money and expenditure
def calculate_financial_metrics(data):
    # Monthly income
    data['total_expenses'] = data[['tuition', 'housing', 'food', 'transportation', 'books_supplies',
                                   'entertainment', 'personal_care', 'technology', 'health_wellness',
                                   'miscellaneous']].sum(axis=1)
    
    data['available_money'] = data['monthly_income'] - data['total_expenses']
    return data

# Create visualizations
def create_visualizations(data):
    # Visualize available money
    st.header("Available Money")
    fig = px.bar(data, x="age", y="available_money", color="year_in_school",
                 labels={'available_money': 'Money Left After Expenses'}, title="Available Money by Age and Year in School")
    st.plotly_chart(fig)
    
    # Visualize expenditure breakdown
    st.header("Breakdown of Expenses")
    expense_columns = ['tuition', 'housing', 'food', 'transportation', 'books_supplies', 
                       'entertainment', 'personal_care', 'technology', 'health_wellness', 'miscellaneous']
    
    total_expenses = data[expense_columns].sum().reset_index()
    total_expenses.columns = ['Expense Category', 'Total Amount']
    fig_expenses = px.pie(total_expenses, names='Expense Category', values='Total Amount',
                          title="Total Breakdown of Expenditures")
    st.plotly_chart(fig_expenses)
    
    # Visualize saving/investing recommendations
    st.header("Potential Savings or Investments")
    st.markdown("""
    Based on your financial data, here are some places you could put your savings:
    
    - **Savings Account**: Low-risk, easy access.
    - **Stocks/ETFs**: Higher returns but comes with risk.
    - **Retirement Funds (e.g., IRA)**: Long-term investments for retirement.
    """)
    
    fig_savings = px.bar(data, x="age", y="how_much_im_wanting_to_save", color="major",
                         title="Desired Savings by Age and Major",
                         labels={'how_much_im_wanting_to_save': 'Desired Savings Amount'})
    st.plotly_chart(fig_savings)

# Main Streamlit app
def main():
    st.title("College Student Financial Management App")
    
    # Load and process the data
    data = load_data()  # This can be replaced with fetch_data() once Databricks integration is ready
    if data is not None:
        data = calculate_financial_metrics(data)
        
        # Display financial metrics
        st.subheader("Financial Metrics Overview")
        st.write(data[['age', 'year_in_school', 'monthly_income', 'total_expenses', 'available_money']])
        
        # Create charts and visualizations
        create_visualizations(data)

if __name__ == "__main__":
    main()
