import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("PennyWise - Financial Budget Assistant")

# Step 1: Input income and extra earnings (like financial aid)
st.header("Income and Extra Earnings")

income = st.number_input("Enter your monthly income", min_value=0.0, step=100.0, format="%.2f")
extra_earnings = st.number_input("Enter any extra earnings (e.g., financial aid)", min_value=0.0, step=100.0, format="%.2f")

# Step 2: Add expenses with names and amounts
st.header("Add Your Expenses")

# Create lists to store expense names and values
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
    st.session_state.expense_names = []

# Input for expense name and amount
expense_name = st.text_input("Enter the name of the expense (e.g., 'Table')")
expense_input = st.number_input("Enter the expense amount", min_value=0.0, step=10.0, format="%.2f")

# Button to add expense to the list
if st.button("Add Expense"):
    if expense_name and expense_input > 0:
        st.session_state.expense_names.append(expense_name)
        st.session_state.expenses.append(expense_input)
        st.success(f"Expense '{expense_name}' of ${expense_input:.2f} added.")
    else:
        st.error("Please enter a valid expense name and amount.")

# Display the added expenses
if st.session_state.expenses:
    st.subheader("Your Added Expenses")
    for name, value in zip(st.session_state.expense_names, st.session_state.expenses):
        st.write(f"{name}: ${value:.2f}")

# Step 3: Input savings goal
st.header("Set Your Savings Goal")
savings_goal = st.number_input("How much would you like to save?", min_value=0.0, step=100.0, format="%.2f")

# Step 4: Calculate and display the remaining budget
if st.button("View Report"):
    # Total expenses
    total_expenses = sum(st.session_state.expenses)
    
    # Total income
    total_income = income + extra_earnings
    remaining_budget = total_income - total_expenses - savings_goal

    # Display financial analysis
    st.subheader("Financial Overview")
    st.write(f"Total Income: ${total_income:.2f}")
    st.write(f"Total Expenses: ${total_expenses:.2f}")
    st.write(f"Savings Goal: ${savings_goal:.2f}")
    st.write(f"Remaining Budget: ${remaining_budget:.2f}")

    # Step 5: Bar chart visualization with all expenses and categories
    st.subheader("Income, Expenses, and Savings Breakdown")

    # Data for the bar chart
    categories = ['Income', 'Savings Goal'] + st.session_state.expense_names
    amounts = [total_income, savings_goal] + st.session_state.expenses

    # Plotting the bar chart
    fig, ax = plt.subplots()
    ax.bar(categories, amounts, color=['blue'] + ['green'] + ['orange'] * len(st.session_state.expenses))
    ax.set_ylabel("Amount ($)")
    ax.set_title("Income vs Expenses vs Savings")
    plt.xticks(rotation=45, ha='right')

    # Show the chart
    st.pyplot(fig)
