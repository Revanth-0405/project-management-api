from flask import Blueprint, request, jsonify
from database import db
from models.project_model import Project
from services.task_service import get_tasks_by_project
import logging

project_bp = Blueprint("projects", __name__)

def error_response(msg, code):
    return jsonify({"error": msg}), code


@project_bp.route("/api/projects", methods=["POST"])
def create_project():

    data = request.get_json()

    if not data or not data.get("name"):
        return error_response("Project name required", 400)

    if Project.query.filter_by(name=data["name"]).first():
        return error_response("Project already exists", 409)

    project = Project(
        name=data["name"],
        description=data.get("description"),
        status=data.get("status", "active")
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at
    }), 201


@project_bp.route("/api/projects", methods=["GET"])
def list_projects():

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    projects = Project.query.paginate(page=page, per_page=per_page)

    return jsonify([{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "status": p.status,
        "created_at": p.created_at,
        "updated_at": p.updated_at
    } for p in projects.items])


@project_bp.route("/api/projects/<int:id>", methods=["GET"])
def get_project(id):

    project = Project.query.get(id)
    if not project:
        return error_response("Project not found", 404)

    tasks = get_tasks_by_project(id)

    return jsonify({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "status": project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "tasks": tasks
    })
