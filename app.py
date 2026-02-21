from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt, cors
from routes.auth import auth_bp
from routes.advisory import advisory_bp
from routes.crops import crops_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(advisory_bp)
    app.register_blueprint(crops_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)