from flask import Flask, jsonify
from database import db
from routes import project_bp, task_bp
import logging_config
import os

app = Flask(__name__)

# ---------------- DATABASE CONFIG ----------------
if os.environ.get("TESTING") == "1":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(project_bp)
app.register_blueprint(task_bp)


# ---------------- GLOBAL ERROR HANDLER ----------------
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
