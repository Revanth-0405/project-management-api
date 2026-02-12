from flask import Blueprint, request, jsonify
from models.project_model import Project
from services.task_service import *

task_bp = Blueprint("tasks", __name__)

def error_response(msg, code):
    return jsonify({"error": msg}), code


@task_bp.route("/api/projects/<int:id>/tasks", methods=["POST"])
def create_task_route(id):

    if not Project.query.get(id):
        return error_response("Project not found", 404)

    data = request.get_json()

    if not data or not data.get("title") or not data.get("priority"):
        return error_response("Title and priority required", 400)

    task, error = create_task(id, data)

    if error:
        return error_response(error, 400)

    return jsonify(task), 201


@task_bp.route("/api/projects/<int:id>/tasks", methods=["GET"])
def list_tasks(id):

    tasks = get_tasks_by_project(id)

    status = request.args.get("status")
    priority = request.args.get("priority")

    if status:
        tasks = [t for t in tasks if t["status"] == status]

    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify(tasks[start:end])
