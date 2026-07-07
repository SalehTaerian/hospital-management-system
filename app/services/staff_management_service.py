from app.database.queries.staff_management_queries import *
from app.database.queries.auth_queries import create_employee, assign_employee_role, check_employee_exists

def get_all_staff_service():
    return get_all_staff()

def get_staff_by_id_service(employee_id):
    staff = get_staff_by_id(employee_id)
    if not staff:
        raise ValueError(f"Staff member with ID {employee_id} not found")
    return staff

def create_employee_service(data):
    if not data.get('firstName'):
        raise ValueError("First name is required")
    if not data.get('lastName'):
        raise ValueError("Last name is required")
    if not data.get('nationalCode'):
        raise ValueError("National code is required")
    if not data.get('accessLevel'):
        raise ValueError("Role is required")
    
    if check_employee_exists(data['nationalCode']):
        raise ValueError("An employee with this national code already exists")
    
    employee_id = create_employee(data)
    if not employee_id:
        raise ValueError("Failed to create employee")
    
    assign_employee_role(employee_id, data['accessLevel'])
    
    return employee_id

def update_employee_service(employee_id, data):
    existing = get_staff_by_id(employee_id)
    if not existing:
        raise ValueError(f"Staff member with ID {employee_id} not found")
    
    return update_employee(employee_id, data)

def delete_employee_service(employee_id):
    existing = get_staff_by_id(employee_id)
    if not existing:
        raise ValueError(f"Staff member with ID {employee_id} not found")
    
    return delete_employee(employee_id)

def update_employee_role_service(employee_id, new_role):
    existing = get_staff_by_id(employee_id)
    if not existing:
        raise ValueError(f"Staff member with ID {employee_id} not found")
    
    valid_roles = ['doctor', 'surgeon', 'nurse', 'officeStaff']
    if new_role not in valid_roles:
        raise ValueError(f"Invalid role. Must be one of: {', '.join(valid_roles)}")
    
    return update_employee_role(employee_id, new_role)

def get_staff_count_service():
    return get_staff_count()

def get_staff_by_role_service(role):
    return get_staff_by_role(role)