from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(128))
    comment = db.Column(db.String())
    saltiness = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def __repr__(self):
        return f"<Comment {self.id} {self.text}>"