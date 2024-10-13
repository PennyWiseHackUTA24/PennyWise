import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_echarts import st_echarts

# Title of the app
st.title("PennyWise - Financial Budget Assistant")

# Step 1: Input income and extra earnings
st.header("Income and Extra Earnings")
income = st.number_input("Enter your monthly income", min_value=0.0, step=100.0, value=0.0, format="%.2f")
extra_earnings = st.number_input("Enter any extra earnings (e.g., financial aid)", min_value=0.0, step=100.0, value=0.0, format="%.2f")

# Step 2: Add expenses
st.header("Add Your Expenses")
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
    st.session_state.expense_names = []

col1, col2 = st.columns([2, 1])
with col1:
    expense_name = st.text_input("Expense Name", key="expense_name")
with col2:
    expense_input = st.number_input("Expense Amount", min_value=0.0, step=10.0, value=0.0, format="%.2f", key="expense_amount")

if st.button("Add Expense"):
    if expense_name and expense_input > 0:
        st.session_state.expense_names.append(expense_name)
        st.session_state.expenses.append(expense_input)
        st.success(f"Expense '{expense_name}' of ${expense_input:.2f} added.")
    else:
        st.error("Please enter a valid expense name and amount.")

if st.session_state.expenses:
    st.subheader("Your Added Expenses")
    for name, value in zip(st.session_state.expense_names, st.session_state.expenses):
        st.write(f"{name}: ${value:.2f}")

# Step 3: Input savings goal
st.header("Set Your Savings Goal")
savings_goal = st.number_input("How much would you like to save?", min_value=0.0, step=100.0, value=0.0, format="%.2f")

# Step 4: Calculate and display the remaining budget
if st.button("View Report"):
    total_expenses = sum(st.session_state.expenses)
    total_income = income + extra_earnings
    remaining_budget = total_income - total_expenses - savings_goal

    # Financial Overview
    st.subheader("Financial Overview")
    st.write(f"Total Income: ${total_income:.2f}")
    st.write(f"Total Expenses: ${total_expenses:.2f}")
    st.write(f"Savings Goal: ${savings_goal:.2f}")
    st.write(f"Remaining Budget: ${remaining_budget:.2f}")

    # Pie Chart (st_echarts)
    st.subheader("Income, Expenses, and Savings Breakdown")
    options = {
        "series": [
            {
                "type": "pie",
                "radius": "50%",
                "data": [
                    {"value": total_expenses, "name": "Expenses", "itemStyle": {"color": "#FF6384"}},
                    {"value": savings_goal, "name": "Savings", "itemStyle": {"color": "#4BC0C0"}},
                    {"value": remaining_budget, "name": "Available", "itemStyle": {"color": "#C9CBCE"}},
                ]
            }
        ]
    }
    st_echarts(options=options, height="600px")

    # Step 5: Sankey Diagram
    st.subheader("Sankey Diagram")
    labels = ["Total Income", "Savings", "Available Money"] + st.session_state.expense_names

    # Sankey Sources and Targets
    sources = [0] * len(st.session_state.expenses) + [0, 0]  # Income flows to all expenses, savings, and available
    targets = list(range(3, 3 + len(st.session_state.expense_names))) + [1, 2]  # Map each expense, savings, and available

    # Values for the Sankey diagram
    values = st.session_state.expenses + [savings_goal, remaining_budget]

    # Colors: Savings green, expenses red, available money light gray
    colors = ['rgba(75, 192, 192, 0.6)', 'rgba(201, 203, 207, 0.6)', 'rgba(255, 99, 132, 0.6)']
    node_colors = ['rgba(75, 192, 192, 0.6)', 'rgba(201, 203, 207, 0.6)', 'rgba(255, 99, 132, 0.6)'] + ['rgba(255, 99, 132, 0.4)'] * len(st.session_state.expense_names)

    # Create the Sankey diagram
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=[f'rgba(255, 99, 132, 0.4)' if i >= 3 else colors[i] for i in range(len(values))]  # Match color for expenses
        )
    ))

    # Update layout for transparency and display
    fig.update_layout(title_text="Income to Expenses and Savings Flow", font_size=10)
    st.plotly_chart(fig)
