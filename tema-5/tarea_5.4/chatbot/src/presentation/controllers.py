from flask import Blueprint, jsonify, render_template_string, request

from ..application.chat_service import ChatService
from ..domain.entities import ChatMessage
from .templates import INDEX_HTML


def build_blueprint(service: ChatService) -> Blueprint:
    bp = Blueprint("chat", __name__)

    @bp.get("/")
    def index() -> str:
        return render_template_string(INDEX_HTML)

    @bp.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        text = (payload.get("message") or "").strip()
        if not text:
            return jsonify(error="message is required"), 400

        return jsonify(response=service.reply(ChatMessage(text=text)))

    return bp