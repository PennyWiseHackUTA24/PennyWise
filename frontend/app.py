import streamlit as st
import pandas as pd

# Load the CSV data (this assumes the CSV is in the same folder)
df = pd.read_csv('student_spending.csv')

# Simulated user storage (For simplicity, we'll skip actual authentication logic)
users = {}
next_user_number = 0  # Keep track of the next available user number

# Function to register a new user
def register_user(username, password):
    global next_user_number
    if next_user_number >= 1000:
        st.error("All user numbers are assigned.")
        return None

    # Assign the next available number from the CSV
    user_number = next_user_number
    users[user_number] = {"username": username, "password": password}
    next_user_number += 1  # Increment for the next user
    return user_number

# Function to authenticate the user
def authenticate(user_number, password):
    user = users.get(user_number)
    if user and user['password'] == password:
        return True
    return False

# Function to calculate the remaining budget
def calculate_budget(user_number, save_amount):
    user_data = df.iloc[user_number]  # Get the user-specific data from the CSV
    income = float(user_data['monthly_income'])
    financial_aid = float(user_data['financial_aid'])
    total_budget = income + financial_aid

    # Calculate total expenses
    total_expenses = (
        float(user_data['housing']) +
        float(user_data['food']) +
        float(user_data['transportation']) +
        float(user_data['books_supplies']) +
        float(user_data['entertainment']) +
        float(user_data['personal_care']) +
        float(user_data['technology']) +
        float(user_data['health_wellness']) +
        float(user_data['miscellaneous'])
    )

    # Calculate remaining budget after setting savings goal
    remaining_budget = total_budget - total_expenses - save_amount

    return total_budget, total_expenses, remaining_budget

# Streamlit app layout
st.title("PennyWise - Financial AI Assistant")

# Registration Section
st.header("Register a New User")
username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:", type="password")

if st.button("Register"):
    user_number = register_user(username, password)
    if user_number is not None:
        st.success(f"User registered successfully! Your user number is {user_number}.")

# Login Section
st.header("User Login")
user_number = st.number_input("Enter your user number", min_value=0, max_value=999, step=1)
login_password = st.text_input("Enter your password:", type="password")

if st.button("Login"):
    if authenticate(user_number, login_password):
        st.success(f"Login successful! Welcome, User {user_number}.")
        st.session_state.logged_in_user = user_number
    else:
        st.error("Invalid credentials. Please try again.")

# Dashboard Section (after login)
if "logged_in_user" in st.session_state:
    st.header(f"Welcome, User {st.session_state.logged_in_user}")

    # Savings Goal Input
    save_amount = st.number_input("How much do you want to save?", min_value=0.0, step=100.0)

    if st.button("Set Budget and Calculate Remaining Budget"):
        total_budget, total_expenses, remaining_budget = calculate_budget(st.session_state.logged_in_user, save_amount)
        
        # Display the budget results
        st.subheader("Budget Overview")
        st.write(f"Total Budget: ${total_budget:.2f}")
        st.write(f"Total Expenses: ${total_expenses:.2f}")
        st.write(f"Remaining Budget: ${remaining_budget:.2f}")
