from extensions import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_expert = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('Answer', backref='post', lazy=True)
    votes = db.relationship('Vote', backref='post', lazy=True)

    def to_dict(self):
        badge = "[Expert]" if self.is_expert else "[Farmer]"
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author": f"{self.author} {badge}",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "upvotes": Vote.query.filter_by(post_id=self.id, vote_type="up").count(),
            "downvotes": Vote.query.filter_by(post_id=self.id, vote_type="down").count(),
            "answer_count": len(self.answers)
        }

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    is_expert = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def to_dict(self):
        badge = "[Expert]" if self.is_expert else "[Farmer]"
        return {
            "id": self.id,
            "content": self.content,
            "author": f"{self.author} {badge}",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
        }

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(10), nullable=False)  # "up" or "down"
    voter = db.Column(db.String(100), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)