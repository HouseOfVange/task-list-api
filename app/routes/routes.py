from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime 
import requests
from app.routes.slack_bot_routes import slack_message

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET"])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    if tasks == None:
        return [], 200

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@tasks_bp.route("", methods = ["POST"])
def post_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)
        
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task":new_task.to_dict()}

    return jsonify(response_body), 201

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404

    elif request.method == "GET":
        task_response = {"task" : task.to_dict()}
        return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def put_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        db.session.commit()

        response_body = {"task":task.to_dict()}
        return jsonify(response_body), 200

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404
    else:
        response_body = {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}

        db.session.delete(task)
        db.session.commit()

        return jsonify(response_body), 200

@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def patch_task_mark_complete(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify(None), 404
    else:
        # send notification to task-notifications slack channel
        slack_message(f"Someone just completed the task {task.title}")

        if task.completed_at == None:
            task.completed_at = datetime.utcnow()

        db.session.commit()

        response_body = {"task":task.to_dict()}

    return jsonify(response_body), 200    

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def patch_task_mark_incomplete(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return jsonify(None), 404
    else:
        if task.completed_at:
            task.completed_at = None

        db.session.commit()

        response_body = {"task":task.to_dict()}

    return jsonify(response_body), 200 