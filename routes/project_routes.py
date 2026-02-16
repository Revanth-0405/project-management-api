from flask import Blueprint, request, jsonify
from database import db
from models import Project
from services import get_tasks_by_project, delete_tasks_by_project
from utils import error
import logging

logger = logging.getLogger(__name__)
project_bp = Blueprint("projects", __name__)


# CREATE PROJECT
@project_bp.route("/api/projects", methods=["POST"])
def create_project():
    data = request.get_json()

    if not data or not data.get("name"):
        return error("Project name required", 400)

    if Project.query.filter_by(name=data["name"]).first():
        return error("Project already exists", 409)

    project = Project(
        name=data["name"],
        description=data.get("description"),
        status=data.get("status", "active")
    )

    db.session.add(project)
    db.session.commit()
    logger.info("Project created")

    return jsonify(project.to_dict()), 201


# LIST PROJECTS
@project_bp.route("/api/projects", methods=["GET"])
def list_projects():
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 5))
        if page < 1 or per_page < 1:
            raise ValueError
    except:
        return error("Invalid pagination params", 400)

    status = request.args.get("status")

    query = Project.query
    if status:
        query = query.filter_by(status=status)

    projects = query.paginate(page=page, per_page=per_page)

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": projects.total,
        "pages": projects.pages,
        "data": [p.to_dict() for p in projects.items]
    })


# GET PROJECT
@project_bp.route("/api/projects/<int:id>", methods=["GET"])
def get_project(id):
    project = db.session.get(Project, id)
    if not project:
        return error("Project not found", 404)

    data = project.to_dict()
    data["tasks"] = get_tasks_by_project(id)

    return jsonify(data)


# UPDATE PROJECT
@project_bp.route("/api/projects/<int:id>", methods=["PUT"])
def update_project(id):
    project = db.session.get(Project, id)
    if not project:
        return error("Project not found", 404)

    data = request.get_json()

    for field in ["name", "description", "status"]:
        if field in data:
            setattr(project, field, data[field])

    db.session.commit()
    return jsonify(project.to_dict())


# DELETE PROJECT
@project_bp.route("/api/projects/<int:id>", methods=["DELETE"])
def delete_project(id):
    project = db.session.get(Project, id)
    if not project:
        return error("Project not found", 404)

    delete_tasks_by_project(id)

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted"})


# SUMMARY
@project_bp.route("/api/projects/<int:id>/summary", methods=["GET"])
def summary(id):
    project = db.session.get(Project, id)
    if not project:
        return error("Project not found", 404)

    tasks = get_tasks_by_project(id)

    result = {
        "project_id": id,
        "project_name": project.name,
        "total_tasks": len(tasks),
        "by_status": {},
        "by_priority": {}
    }

    for t in tasks:
        result["by_status"][t["status"]] = result["by_status"].get(t["status"], 0) + 1
        result["by_priority"][t["priority"]] = result["by_priority"].get(t["priority"], 0) + 1

    return jsonify(result)
