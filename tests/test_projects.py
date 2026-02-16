import os
os.environ["TESTING"] = "1"

import unittest
from app import app
from database import db


class ProjectTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    # ---------------- CREATE ----------------

    def test_create_project(self):
        res = self.client.post("/api/projects", json={"name": "Alpha"})
        self.assertEqual(res.status_code, 201)

    def test_duplicate_project(self):
        self.client.post("/api/projects", json={"name": "Dup"})
        res = self.client.post("/api/projects", json={"name": "Dup"})
        self.assertEqual(res.status_code, 409)

    def test_missing_name(self):
        res = self.client.post("/api/projects", json={})
        self.assertEqual(res.status_code, 400)

    # ---------------- READ ----------------

    def test_list_projects(self):
        res = self.client.get("/api/projects")
        self.assertEqual(res.status_code, 200)

    def test_get_single_project(self):
        res = self.client.post("/api/projects", json={"name": "Single"})
        pid = res.get_json()["id"]

        res = self.client.get(f"/api/projects/{pid}")
        self.assertEqual(res.status_code, 200)

    def test_get_invalid_project(self):
        res = self.client.get("/api/projects/999")
        self.assertEqual(res.status_code, 404)

    # ---------------- UPDATE ----------------

    def test_update_project(self):
        res = self.client.post("/api/projects", json={"name": "UpdateMe"})
        pid = res.get_json()["id"]

        res = self.client.put(f"/api/projects/{pid}", json={"status": "archived"})
        self.assertEqual(res.status_code, 200)

    # ---------------- DELETE ----------------

    def test_delete_project(self):
        res = self.client.post("/api/projects", json={"name": "DeleteMe"})
        pid = res.get_json()["id"]

        res = self.client.delete(f"/api/projects/{pid}")
        self.assertEqual(res.status_code, 200)

    # ---------------- SUMMARY ----------------

    def test_summary(self):
        res = self.client.post("/api/projects", json={"name": "Summary"})
        pid = res.get_json()["id"]

        res = self.client.get(f"/api/projects/{pid}/summary")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
