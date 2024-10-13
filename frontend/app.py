import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("PennyWise - Financial Budget Assistant")

# Step 1: Input income and extra earnings (like financial aid)
st.header("Income and Extra Earnings")

income = st.number_input("Enter your monthly income", min_value=0.0, step=100.0, format="%.2f")
extra_earnings = st.number_input("Enter any extra earnings (e.g., financial aid)", min_value=0.0, step=100.0, format="%.2f")

# Step 2: Add expenses incrementally
st.header("Add Your Expenses")

expenses = []

# Input for adding each expense
expense_input = st.number_input("Enter an expense", min_value=0.0, step=10.0, format="%.2f")
if st.button("Add Expense"):
    expenses.append(expense_input)
    st.success(f"Expense of ${expense_input:.2f} added.")

# Display the added expenses
if expenses:
    st.subheader("Your Added Expenses")
    st.write(expenses)

# Step 3: Input savings goal
st.header("Set Your Savings Goal")
savings_goal = st.number_input("How much would you like to save?", min_value=0.0, step=100.0, format="%.2f")

# Step 4: Calculate and display the remaining budget
if st.button("View Report"):
    # Total expenses
    total_expenses = sum(expenses)
    
    # Total budget
    total_income = income + extra_earnings
    remaining_budget = total_income - total_expenses - savings_goal

    # Display financial analysis
    st.subheader("Financial Overview")
    st.write(f"Total Income: ${total_income:.2f}")
    st.write(f"Total Expenses: ${total_expenses:.2f}")
    st.write(f"Savings Goal: ${savings_goal:.2f}")
    st.write(f"Remaining Budget: ${remaining_budget:.2f}")

    # Step 5: Bar chart visualization
    st.subheader("Income vs Expenses Analysis")

    # Data for the bar chart
    data = {
        "Income": total_income,
        "Expenses": total_expenses,
        "Savings Goal": savings_goal
    }
    df = pd.DataFrame(data.items(), columns=["Category", "Amount"])

    # Plotting the bar chart
    fig, ax = plt.subplots()
    ax.bar(df["Category"], df["Amount"], color=["blue", "orange", "green"])
    ax.set_ylabel("Amount ($)")
    ax.set_title("Income vs Expenses vs Savings")
    
    # Show the chart
    st.pyplot(fig)
