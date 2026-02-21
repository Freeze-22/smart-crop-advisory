from app import create_app
from extensions import db
from models.user import User
from models.advisory import Advisory
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    db.create_all()
    inspector = inspect(db.engine)
    print('Tables:', inspector.get_table_names())
    print('Users:', User.query.count())
    print('Advisories:', Advisory.query.count())