from flask import Flask
from database import db
from routes.project_routes import project_bp
from routes.task_routes import task_bp
import logging_config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projects.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(project_bp)
app.register_blueprint(task_bp)

if __name__ == "__main__":
    app.run(debug=True)
