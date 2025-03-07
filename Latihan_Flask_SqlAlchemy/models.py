# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Todo {self.task}>'