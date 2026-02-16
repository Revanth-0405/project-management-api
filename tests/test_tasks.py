import os
os.environ["TESTING"] = "1"

import unittest
from app import app
from database import db


class TaskTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

        res = self.client.post("/api/projects", json={"name": "TaskProj"})
        self.project_id = res.get_json()["id"]

    # ---------------- CREATE ----------------

    def test_create_task(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task1", "priority": "high"}
        )
        self.assertEqual(res.status_code, 201)

    def test_invalid_priority(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task1", "priority": "invalid"}
        )
        self.assertEqual(res.status_code, 400)

    def test_missing_fields(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task1"}
        )
        self.assertEqual(res.status_code, 400)

    # ---------------- READ ----------------

    def test_list_tasks(self):
        res = self.client.get(f"/api/projects/{self.project_id}/tasks")
        self.assertEqual(res.status_code, 200)

    def test_get_task(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task", "priority": "low"}
        )
        task_id = res.get_json()["task_id"]

        res = self.client.get(f"/api/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)

    def test_get_invalid_task(self):
        res = self.client.get("/api/tasks/invalid")
        self.assertEqual(res.status_code, 404)

    # ---------------- UPDATE ----------------

    def test_update_task(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task", "priority": "medium"}
        )
        task_id = res.get_json()["task_id"]

        res = self.client.put(
            f"/api/tasks/{task_id}",
            json={"status": "done"}
        )
        self.assertEqual(res.status_code, 200)

    def test_update_invalid_task(self):
        res = self.client.put("/api/tasks/invalid", json={"status": "done"})
        self.assertEqual(res.status_code, 404)

    # ---------------- DELETE ----------------

    def test_delete_task(self):
        res = self.client.post(
            f"/api/projects/{self.project_id}/tasks",
            json={"title": "Task", "priority": "low"}
        )
        task_id = res.get_json()["task_id"]

        res = self.client.delete(f"/api/tasks/{task_id}")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
