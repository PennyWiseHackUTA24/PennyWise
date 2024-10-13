
from flask import Blueprint, request, jsonify
from backend.services.chatgpt_service import get_chatgpt_response, generate_financial_advice, get_user_financial_advice

chat_bp = Blueprint('chat', __name__)
chat_api = Blueprint('chat_api', __name__)

chat_usrData = Blueprint('chat_usrData', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = get_chatgpt_response(user_input)
    return jsonify({"response": response})


@chat_api.route('/get-advice', methods=['GET'])
def get_advice():
    student_id = request.args.get('student_id')
    user_prompt = request.args.get('prompt')

    if not student_id:
        return jsonify({'error': 'student_id is required'}), 400

    if not user_prompt:
        return jsonify({'error': 'prompt is required'}), 400

    advice = generate_financial_advice(student_id, user_prompt)
    return jsonify({'advice': advice})


@chat_usrData.route('/userDataFrontend', methods=['POST'])
def user_data_frontend():
    try:
        data = request.json
        user_input = data['user_input']
        user_data = data['user_data']

        # Construct the prompt for ChatGPT
        prompt = (
            f"User question: {user_input}\n"
            f"User data: {user_data}\n"
            "Please provide financial advice based on the information above."
        )

        # Send the prompt to ChatGPT and retrieve the response
        advice = get_chatgpt_response(prompt)  # Now this returns a string
        if advice is None:
            return jsonify({"error": "Failed to get advice from ChatGPT."}), 500

        return jsonify({"advice": advice}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
