
from requests import post
import requests


from backend.config.config import CHATGPT_API_KEY, CHATGPT_API_URL


def get_chatgpt_response(user_input):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 150,
        "temperature": 0.5,
    }

    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        response_data = response.json()
        advice = response_data["choices"][0]["message"]["content"].strip()
        return advice  # Return only the advice string
    except requests.exceptions.RequestException as e:
        return None  # Handle errors appropriately


def generate_financial_advice(student_id, user_prompt):
    student_data = fetch_student_data(student_id)
    if not student_data:
        return None, "Student data not found."

    # Extract relevant financial details from student data
    weekly_spending = student_data.get('weekly_spending')
    monthly_income = student_data.get('monthly_income')
    savings_goal = student_data.get('savings_goal')
    current_savings = student_data.get('current_savings')

    # Create a combined prompt for ChatGPT
    combined_prompt = (
        f"Given the following financial data for the student:\n"
        f"Weekly Spending: {weekly_spending}\n"
        f"Monthly Income: {monthly_income}\n"
        f"Savings Goal: {savings_goal}\n"
        f"Current Savings: {current_savings}\n\n"
        f"{user_prompt}\n"
        f"Based on this data, provide tailored financial advice on how the student can better manage their finances."
    )

    chatgpt_response, error = get_chatgpt_response(combined_prompt)
    return chatgpt_response, error



def get_user_financial_advice(user_data):
    # Create a prompt for ChatGPT using the user-provided data
    prompt = (
        f"Your name is PennyWise tell them your name when they ask, You are a no-nonsense financial advisor who gives straightforward and blunt advice. "
        f"Based on the user's financial situation, provide unapologetic feedback. "
        f"If the user shares that they are considering a $700 car payment while making only $800, say: "
        f'Look, you CANNOT afford a $700 car payment when you’re only making $800. '
        f"This is financial suicide. You need to get your priorities straight and live within your means. "
        f"Provide specific numbers and advice based on their spending habits. "
        f"If they are spending too much, tell them bluntly that they are spending too much. "
        f"Offer concrete advice on where they can stop spending and where to start saving. "
        f"If they want to buy a car but their finances are tight, tell them they need to increase their income first. "
        f"You do not care about hurting feelings; your goal is to be blunt and give them the truth they need. "
        f"User data: {user_data}\n\n"
    )

    # Get response from ChatGPT
    chatgpt_response, error = get_chatgpt_response(prompt)
    return chatgpt_response, error

