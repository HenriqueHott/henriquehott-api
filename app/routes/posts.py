import datetime
import uuid
from flask import Blueprint, request, jsonify
from mongoengine import ValidationError

from app.middlewares.auth import require_api_key
from app.models import Post

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/posts", methods=["POST"])
@require_api_key
def create_post():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags", [])

    if not (title and content):
        return jsonify({"error": "Campos obrigatórios: title and content"}), 400

    if not isinstance(tags, list):
        return jsonify({"error": "O campo 'tags' deve ser uma lista de strings"}), 400
    
    
    post = Post(**data)
    try:
        post.save()
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify(post.to_dict()), 201

@posts_bp.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    try:
        uuid.UUID(post_id)
    except ValueError:
        return jsonify({"error": "ID inválido"}), 400

    post = Post.objects(id=post_id).first()
    if not post:
        return jsonify({"error": "Post não encontrado"}), 404

    return jsonify(post.to_dict()), 200

@posts_bp.route("/posts", methods=["GET"])
def get_posts():
    tag = request.args.get("tag")
    tags_param = request.args.get("tags")
    exclude_param = request.args.get("exclude_tags")

    # base query
    query = Post.objects

    # filtro por uma única tag
    if tag:
        query = query.filter(tags=tag)

    # filtro por múltiplas tags (qualquer uma)
    elif tags_param:
        tags_list = [t.strip() for t in tags_param.split(",") if t.strip()]
        query = query.filter(tags__in=tags_list)
    
    if exclude_param:
        exclude_list = [t.strip() for t in exclude_param.split(",") if t.strip()]
        query = query.filter(tags__nin=exclude_list)

    # ordena pelos mais recentes
    query = query.order_by("-last_update")

    posts = [p.to_dict() for p in query]
    return jsonify(posts), 200


@posts_bp.route("/posts/<post_id>", methods=["PUT"])
@require_api_key
def update_post(post_id):
    try:
        # Valida o formato do UUID
        uuid.UUID(post_id)
    except ValueError:
        return jsonify({"error": "ID inválido"}), 400

    post = Post.objects(id=post_id).first()
    if not post:
        return jsonify({"error": "Post não encontrado"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    # Atualiza apenas campos presentes
    if "title" in data:
        post.title = str(data["title"]).strip()
    if "excerpt" in data:
        post.excerpt = str(data["excerpt"]).strip()
    if "content" in data:
        post.content = str(data["content"]).strip()
    if "tags" in data:
        tags = data["tags"]
        if not isinstance(tags, list):
            return jsonify({"error": "O campo 'tags' deve ser uma lista de strings"}), 400
        post.tags = [str(t).strip() for t in tags]

    post.updated_at = datetime.datetime.now(datetime.timezone.utc)

    try:
        post.save()
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(post.to_dict()), 200

@posts_bp.route("/posts/<post_id>", methods=["DELETE"])
@require_api_key
def delete_post(post_id):
    try:
        uuid.UUID(post_id)
    except ValueError:
        return '', 200

    post = Post.objects(id=post_id).first()
    if not post:
        return '', 200

    post.delete()
    return  '', 200