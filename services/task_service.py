import boto3
import uuid
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

# VALID VALUES

VALID_PRIORITY = ["low", "medium", "high"]
VALID_STATUS = ["todo", "in_progress", "done"]


# DYNAMODB CONNECTION

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8000",
    region_name="us-east-1",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

table = dynamodb.Table("Tasks")

# CREATE TASK

def create_task(project_id, data):

    if data["priority"] not in VALID_PRIORITY:
        return None, "Invalid priority"

    if "status" in data and data["status"] not in VALID_STATUS:
        return None, "Invalid status"

    task = {
        "project_id": project_id,
        "task_id": str(uuid.uuid4()),
        "title": data["title"],
        "description": data.get("description"),
        "priority": data["priority"],
        "status": data.get("status", "todo"),
        "assigned_to": data.get("assigned_to"),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    table.put_item(Item=task)
    return task, None

# GET TASKS BY PROJECT

def get_tasks_by_project(project_id):
    try:
        response = table.query(
            KeyConditionExpression=Key("project_id").eq(project_id)
        )
        return response.get("Items", [])
    except Exception:
        return []

# DELETE TASKS BY PROJECT

def delete_tasks_by_project(project_id):
    try:
        tasks = get_tasks_by_project(project_id)

        for task in tasks:
            table.delete_item(
                Key={
                    "project_id": project_id,
                    "task_id": task["task_id"]
                }
            )
    except Exception:
        pass

# GET SINGLE TASK

def get_task(task_id):
    try:
        response = table.scan()
        for item in response.get("Items", []):
            if item["task_id"] == task_id:
                return item
        return None
    except Exception:
        return None

# UPDATE TASK

def update_task(task_id, data):

    task = get_task(task_id)

    if not task:
        return None, "not_found"

    if "priority" in data and data["priority"] not in VALID_PRIORITY:
        return None, "Invalid priority"

    if "status" in data and data["status"] not in VALID_STATUS:
        return None, "Invalid status"

    task.update(data)

    table.put_item(Item=task)

    return task, None

# DELETE TASK

def delete_task(task_id):
    try:
        task = get_task(task_id)
        if not task:
            return

        table.delete_item(
            Key={
                "project_id": task["project_id"],
                "task_id": task_id
            }
        )
    except Exception:
        pass
