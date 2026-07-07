from app.database.queries.auth_queries import *
from flask import session

def is_logged_in():
    return 'user_id' in session

def get_current_user():
    if not is_logged_in():
        return None
    
    return {
        'id': session.get('user_id'),
        'national_code': session.get('user_national_code'),
        'role': session.get('user_role'),
        'name': session.get('user_name')
    }

def login_required():
    return is_logged_in()

def role_required(allowed_roles):
    if not is_logged_in():
        return False
    return session.get('user_role') in allowed_roles

def authenticate_patient(national_code, password):
    patient = get_patient_by_national_code(national_code)
    if not patient:
        return None
    
    if patient['password'] != password:
        return None
    
    return {
        'id': patient['pid'],
        'firstName': patient['firstname'],
        'lastName': patient['lastname'],
        'nationalCode': patient['nationalcode']
    }

def login_patient(user):
    session['user_id'] = user['id']
    session['user_national_code'] = user['nationalCode']
    session['user_role'] = 'patient'
    session['user_name'] = f"{user['firstName']} {user['lastName']}"

def register_patient(data):
    if check_patient_exists(data['nationalCode']):
        raise ValueError("A patient with this national code already exists")
    
    patient_id = create_patient(data)
    if not patient_id:
        raise ValueError("Failed to create patient")
    
    create_medical_record(patient_id)
    
    return patient_id

def logout_patient():
    session.clear()

def authenticate_employee(national_code, password):
    employee = get_employee_by_national_code(national_code)
    if not employee:
        return None
    
    if employee['password'] != password:
        return None
    
    role_data = get_employee_role(employee['employeeid'])
    role = role_data['role'] if role_data else 'employee'
    
    return {
        'id': employee['employeeid'],
        'firstName': employee['firstname'],
        'lastName': employee['lastname'],
        'nationalCode': employee['nationalcode'],
        'role': role,
        'accessLevel': employee['accesslevel']
    }

def login_employee(user):
    session['user_id'] = user['id']
    session['user_national_code'] = user['nationalCode']
    session['user_role'] = user['role']
    session['user_name'] = f"{user['firstName']} {user['lastName']}"
    session['access_level'] = user['accessLevel']

def logout_employee():
    session.clear()

def get_departments_service():
    return get_all_departments()

def create_employee_service(data):
    if not data.get('firstName'):
        raise ValueError("First name is required")
    if not data.get('lastName'):
        raise ValueError("Last name is required")
    if not data.get('nationalCode'):
        raise ValueError("National code is required")
    if not data.get('accessLevel'):
        raise ValueError("Access level/role is required")
    
    if check_employee_exists(data['nationalCode']):
        raise ValueError("An employee with this national code already exists")
    
    employee_id = create_employee(data)
    if not employee_id:
        raise ValueError("Failed to create employee")
    
    assign_employee_role(employee_id, data['accessLevel'])
    
    return employee_id

def get_doctors_service(search_term=None):
    return get_doctors_with_specialization(search_term)

def get_patient_medical_info_service(patient_id):
    return get_patient_medical_info(patient_id)