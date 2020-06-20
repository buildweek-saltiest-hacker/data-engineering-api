"""
API for the Salty Hacker Build Week Project

Model Developer:
Iuliia Stanina
"""
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
        return f'<Comment {self.id} {self.author} {self.comment} {self.saltiness} {self.score}'


def parse_records(database_records):
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records