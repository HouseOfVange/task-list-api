from flask import Blueprint, jsonify, request
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods = ["GET"])
def get_goals():
    goals = Goal.query.all()
        
    if goals == None:
        return [], 200

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@goals_bp.route("", methods = ["POST"])
def post_goal():
    request_body = request.get_json()

    if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)
        
    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal":new_goal.to_dict()}

    return jsonify(response_body), 201

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    elif request.method == "GET":
        goal_response = {"goal" : goal.to_dict()}
        return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods = ["PUT"])
def put_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    elif request.method == "PUT":
        form_data = request.get_json()
        goal.title = form_data["title"]
        db.session.commit()

        response_body = {"goal":goal.to_dict()}
        return jsonify(response_body), 200

@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if goal is None:
        return jsonify(None), 404

    else:
        response_body = {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}

        db.session.delete(goal)
        db.session.commit()

        return jsonify(response_body), 200