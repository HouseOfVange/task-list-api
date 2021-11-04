from flask import current_app
from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    COLUMNS = ["title", "description", "completed_at"]

    def to_dict(self):
        return {
            "id": self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : False if self.completed_at == None else True
        }
    
    @classmethod
    def from_dict(cls, values):
        return cls(**values)
    
    # use for PATCH requests
    def update_from_dict(self, values):
        for column in self.COLUMNS:
            if column in values:
                setattr(self, column, values[column])

    #use for PUT requests
    def replace_with_dict(self, values):
        for column in self.COLUMNS:
            if column in values:
                setattr(self, column, values[column])
            else:
                raise ValueError(f"required column {column} missing")
            