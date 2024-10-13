# backend/api/chat.py

from flask import Blueprint, request, jsonify
from backend.services.chatgpt_service import get_chatgpt_response

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = get_chatgpt_response(user_input)
    return jsonify({"response": response})
