from flask import Blueprint, request, jsonify
from models import Project
from database import db
from services import *
from utils import error

task_bp = Blueprint("tasks", __name__)


# CREATE TASK
@task_bp.route("/api/projects/<int:id>/tasks", methods=["POST"])
def create_task_route(id):

    if not db.session.get(Project, id):
        return error("Project not found", 404)

    data = request.get_json()

    if not data or not data.get("title") or not data.get("priority"):
        return error("Title and priority required", 400)

    task, err = create_task(id, data)

    if err:
        return error(err, 400)

    return jsonify(task), 201


# LIST TASKS
@task_bp.route("/api/projects/<int:id>/tasks")
def list_tasks(id):
    tasks = get_tasks_by_project(id)

    status = request.args.get("status")
    priority = request.args.get("priority")

    if status:
        tasks = [t for t in tasks if t["status"] == status]

    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]

    return jsonify(tasks)


# GET TASK
@task_bp.route("/api/tasks/<task_id>")
def get_task_route(task_id):
    task = get_task(task_id)

    if not task:
        return error("Task not found", 404)

    return jsonify(task)


# UPDATE TASK
@task_bp.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task_route(task_id):
    data = request.get_json()

    task, err = update_task(task_id, data)

    if err == "not_found":
        return error("Task not found", 404)

    if err:
        return error(err, 400)

    return jsonify(task)


# DELETE TASK
@task_bp.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    delete_task(task_id)
    return jsonify({"message": "Task deleted"})
