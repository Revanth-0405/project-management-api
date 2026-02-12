import boto3
import uuid
from datetime import datetime

VALID_PRIORITY = ["low", "medium", "high"]
VALID_STATUS = ["todo", "in_progress", "done"]

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

table = dynamodb.Table("Tasks")


def create_task(project_id, data):

    if data["priority"] not in VALID_PRIORITY:
        return None, "Invalid priority"

    task = {
        "task_id": str(uuid.uuid4()),
        "project_id": project_id,
        "title": data["title"],
        "description": data.get("description"),
        "priority": data["priority"],
        "status": data.get("status", "todo"),
        "assigned_to": data.get("assigned_to"),
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=task)
    return task, None


def get_tasks_by_project(project_id):
    response = table.scan()
    return [t for t in response["Items"] if t["project_id"] == project_id]


def get_task(task_id):
    response = table.get_item(Key={"task_id": task_id})
    return response.get("Item")


def update_task(task_id, data):

    task = get_task(task_id)
    if not task:
        return None

    if "priority" in data and data["priority"] not in VALID_PRIORITY:
        return None

    if "status" in data and data["status"] not in VALID_STATUS:
        return None

    task.update(data)
    table.put_item(Item=task)
    return task


def delete_task(task_id):
    table.delete_item(Key={"task_id": task_id})
