import re
from flask import Blueprint, jsonify, request
from app.models.task import Task
from app.models.goal import Goal
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET", "POST"])
def get_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        if tasks == None:
            return [], 200
        tasks_response = [task.to_dict() for task in tasks]
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

        new_task = Task.from_dict(request_body)
        
        db.session.add(new_task)
        db.session.commit()

        response_body = {"task":new_task.to_dict()}

        return jsonify(response_body), 201

@tasks_bp.route("/<task_id>", methods = ["GET", "DELETE", "PUT"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify(None), 404

    elif request.method == "GET":
        task_response = {"task" : task.to_dict()}
        return jsonify(task_response), 200

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        db.session.commit()

        return jsonify(task.to_dict()), 200

        # request_body = request.get_json()
        # task.replace_with_dict(request_body)
        # db.session.commit()
        # response_body = {"task" : task.to_dict()}
        # return jsonify(response_body), 200

    elif request.method == "DELETE":
        response_body = {"details": f"Task {task.id} \"{task.title}\" successfully deleted"}

        db.session.delete(task)
        db.session.commit()

        return jsonify(response_body), 200