from flask import Blueprint, request, jsonify

from app.utils import preprocess

sentiment_bp = Blueprint("sentiment", __name__)



def preprocess_bert(text):
    text = text.lower()
    text = preprocess.remove_usernames(text)
    text = preprocess.remove_hashtags(text)
    text = preprocess.remove_emoticons(text)
    text = preprocess.remove_urls(text)
    text = preprocess.remove_accents(text)
    text = preprocess.remove_numbers(text)
    text = preprocess.remove_extra_whitespace(text)
    return text

@sentiment_bp.route("/sentiment", methods=["POST"])
def sentiment():
    """
    Exemplo de endpoint de análise de sentimento.
    Espera JSON: { "text": "mensagem aqui" }
    """
    data = request.get_json()
    text = data.get("text", "")

    # Exemplo fictício de análise
    if not text:
        return jsonify({"error": "Texto não fornecido"}), 400

    # Simulação simples de lógica
    sentiment = "positivo" if "bom" in text.lower() else "negativo"

    return jsonify({
        "sentiment": sentiment
    })
