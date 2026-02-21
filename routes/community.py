from flask import Blueprint, request, jsonify
from extensions import db
from models.community import Post, Answer, Vote

community_bp = Blueprint('community', __name__)

# Get all posts
@community_bp.route('/api/community/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200

# Create new post
@community_bp.route('/api/community/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post = Post(
        title=data['title'],
        content=data['content'],
        author=data['author'],
        is_expert=data.get('is_expert', False)
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

# Get single post with answers
@community_bp.route('/api/community/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = Post.query.get_or_404(id)
    data = post.to_dict()
    data['answers'] = [a.to_dict() for a in post.answers]
    return jsonify(data), 200

# Add answer to post
@community_bp.route('/api/community/posts/<int:id>/answer', methods=['POST'])
def add_answer(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    answer = Answer(
        content=data['content'],
        author=data['author'],
        is_expert=data.get('is_expert', False),
        post_id=post.id
    )
    db.session.add(answer)
    db.session.commit()
    return jsonify(answer.to_dict()), 201

# Upvote or downvote post
@community_bp.route('/api/community/posts/<int:id>/vote', methods=['POST'])
def vote_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()
    voter = data['voter']
    vote_type = data['vote_type']  # "up" or "down"

    # Check if already voted
    existing = Vote.query.filter_by(post_id=post.id, voter=voter).first()
    if existing:
        existing.vote_type = vote_type
    else:
        vote = Vote(post_id=post.id, voter=voter, vote_type=vote_type)
        db.session.add(vote)

    db.session.commit()
    return jsonify({
        "upvotes": Vote.query.filter_by(post_id=post.id, vote_type="up").count(),
        "downvotes": Vote.query.filter_by(post_id=post.id, vote_type="down").count()
    }), 200

# Search posts
@community_bp.route('/api/community/search', methods=['GET'])
def search_posts():
    q = request.args.get('q', '')
    posts = Post.query.filter(
        Post.title.contains(q) | Post.content.contains(q)
    ).order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200