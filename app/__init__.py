from flask import Flask
from app.config import Config
from app.database.connection import DatabaseConnection
from app.routes.auth_routes import auth_bp
from app.routes.auth_routes import mainPage_bp
from app.routes.patient_routes import patient_bp
from app.routes.staff_routes import staff_bp
from app.routes.icd_routes import icd_bp
from app.routes.staff_management_routes import staff_mgmt_bp
from app.routes.shift_routes import shift_bp
from app.routes.room_routes import room_bp
from app.routes.request_routes import request_bp
from app.routes.admission_routes import admission_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    DatabaseConnection.initialize_pool()
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(mainPage_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(icd_bp)
    app.register_blueprint(staff_mgmt_bp)
    app.register_blueprint(shift_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(admission_bp)
    
    
    logging.basicConfig(level=logging.INFO)
    
    return app