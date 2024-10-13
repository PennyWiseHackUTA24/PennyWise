from requests import post

from backend.config.config import CHATGPT_API_KEY, CHATGPT_API_URL


def get_chatgpt_response(user_input):
    headers = {
        "Authorization": f"Bearer {CHATGPT_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": user_input}
        ]
    }

    response = post(CHATGPT_API_URL, headers=headers, json=data)

    print(f"CHATGPT_API_KEY: {CHATGPT_API_KEY}")  # Should show the actual key
    print(f"CHATGPT_API_URL: {CHATGPT_API_URL}")  # Should show the API URL

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print(f"OpenAI API Response: {response.status_code} - {response.text}")  # Log the response for debugging
        return f"Error: {response.status_code}, {response.text}"
