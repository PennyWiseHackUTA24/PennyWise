import plotly.graph_objects as go
import streamlit as st
from streamlit_echarts import st_echarts
import requests

BACKEND_URL = "http://127.0.0.1:5000"  # Fixed typo in URL

# Title of the app
st.title("PennyWise - Financial Budget Assistant")

# Step 1: Input income and extra earnings (like financial aid)
st.header("Income and Extra Earnings")

income = st.number_input("Enter your monthly income", min_value=0.0, step=100.0, value=0.0, format="%.2f")
extra_earnings = st.number_input("Enter any extra earnings (e.g., financial aid)", min_value=0.0, step=100.0, value=0.0,
                                 format="%.2f")

# Step 2: Add expenses with names and amounts
st.header("Add Your Expenses")

# Initialize session state if not already done
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
    st.session_state.expense_names = []

# Display inputs for expense name and amount side by side
col1, col2 = st.columns([2, 1])  # Wider for name, narrower for amount
with col1:
    expense_name = st.text_input("Expense Name", key="expense_name")
with col2:
    expense_input = st.number_input("Expense Amount", min_value=0.0, step=10.0, value=0.0, format="%.2f",
                                    key="expense_amount")

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
savings_goal = st.number_input("How much would you like to save?", min_value=0.0, step=100.0, value=0.0, format="%.2f")

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
    st.write(f"Remaining Budget (Available Money): ${remaining_budget:.2f}")

    # Step 5: Pie chart visualization using st_echarts
    st.subheader("Income, Expenses, and Savings Breakdown")

    # Data for the pie chart
    pie_options = {
        "series": [
            {
                "type": 'pie',
                "radius": '50%',
                "data": [
                    {"value": savings_goal, "name": 'Savings', "itemStyle": {"color": "green"}},
                    {"value": total_expenses, "name": 'Expenses', "itemStyle": {"color": "red"}},
                    {"value": remaining_budget, "name": 'Available Money', "itemStyle": {"color": "lightgrey"}},
                ]
            }
        ],
        "tooltip": {
            "trigger": 'item',
            "formatter": '{a} <br/>{b} : {c} ({d}%)'
        },
        "legend": {
            "top": '5%',
            "left": 'center'
        }
    }

    st_echarts(options=pie_options, height="600px")

    # Step 6: Sankey Diagram Visualization
    st.subheader("Sankey Diagram - Financial Flow")

    # Define nodes for the Sankey diagram
    nodes = ['Income', 'Savings', 'Expenses', 'Available Money'] + st.session_state.expense_names

    # Define the source and target relationships
    sources = [0, 0, 0] + [2] * len(
        st.session_state.expense_names)  # Income -> Savings, Expenses, and Available Money, then to expense categories
    targets = [1, 2, 3] + list(range(4, len(nodes)))

    # Define the value for each flow
    values = [savings_goal, total_expenses, remaining_budget] + st.session_state.expenses

    # Create the Sankey diagram
    sankey_fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=["blue", "green", "red", "lightgrey"] + ["lightblue"] * len(st.session_state.expense_names)
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=["green", "red", "lightgrey"] + ["lightblue"] * len(st.session_state.expense_names)
        )
    ))

    # Update layout and display
    sankey_fig.update_layout(title_text="Financial Flow Diagram", font_size=10)
    st.plotly_chart(sankey_fig)


# Step 7: Request advice from ChatGPT
st.header("Get Financial Advice")
user_input = st.text_area("Enter your financial question here:")

# Prepare the user data string from all input fields
user_data = f"Income: ${income:.2f}, Extra Earnings: ${extra_earnings:.2f}, Expenses: {', '.join([f'{name}: ${value:.2f}' for name, value in zip(st.session_state.expense_names, st.session_state.expenses)])}, Savings Goal: ${savings_goal:.2f}"

if st.button("Get Advice"):
    if user_input:
        # Prepare the data to send to the backend
        request_data = {
            "user_input": user_input,
            "user_data": user_data
        }

        # Send user data to the backend for analysis
        try:
            response = requests.post(f"{BACKEND_URL}/api/userDataFrontend", json=request_data)
            if response.status_code == 200:
                advice = response.json().get("advice")
                st.subheader("PennyWise's Advice")
                st.write(advice)
            else:
                st.error("Error: " + response.json().get("error", "Something went wrong."))
        except Exception as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.error("Please enter your financial question.")

