from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    COLUMNS = ["title"]

    def to_dict(self):
        return {
            "goal_id": self.goal_id,
            "title" : self.title
        }
    
    @classmethod
    def from_dict(cls, values):
        return cls(**values)
    
    # # use for PATCH requests
    # def update_from_dict(self, values):
    #     for column in self.COLUMNS:
    #         if column in values:
    #             setattr(self, column, values[column])

    # #use for PUT requests
    # def replace_with_dict(self, values):
    #     for column in self.COLUMNS:
    #         if column in values:
    #             setattr(self, column, values[column])
    #         else:
    #             raise ValueError(f"required column {column} missing")
            