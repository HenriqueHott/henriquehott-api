from flask import request, jsonify
import os
from functools import wraps

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        expected_key = os.getenv("API_KEY")

        if not api_key:
            return jsonify({"error": "Chave de API não fornecida"}), 401

        # aceita tanto "Authorization: 123" quanto "Authorization: Bearer 123"
        if api_key.startswith("Bearer "):
            api_key = api_key.replace("Bearer ", "").strip()

        if api_key != expected_key:
            return jsonify({"error": "Chave de API inválida"}), 403

        return func(*args, **kwargs)
    return wrapper