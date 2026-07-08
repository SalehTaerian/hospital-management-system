from app.database.queries.shift_queries import *
from datetime import datetime

def get_all_shifts_service(start_date=None, end_date=None):
    return get_all_shifts(start_date, end_date)

def get_shift_by_id_service(shift_id):
    shift = get_shift_by_id(shift_id)
    if not shift:
        raise ValueError(f"Shift with ID {shift_id} not found")
    return shift

def get_employees_on_shift_service(shift_id):
    return get_employees_on_shift(shift_id)

def create_shift_service(data):
    if not data.get('shiftDate'):
        raise ValueError("Shift date is required")
    if not data.get('startTime'):
        raise ValueError("Start time is required")
    if not data.get('endTime'):
        raise ValueError("End time is required")
    
    # Validate times
    if data['startTime'] >= data['endTime']:
        raise ValueError("Start time must be before end time")
    
    try:
        shift_date = datetime.strptime(data['shiftDate'], '%Y-%m-%d').date()
        if shift_date < datetime.now().date():
            raise ValueError("Cannot create shifts in the past")
    except ValueError:
        raise ValueError("Invalid date format")
    
    return create_shift(data['shiftDate'], data['startTime'], data['endTime'])

def update_shift_service(shift_id, data):
    existing = get_shift_by_id(shift_id)
    if not existing:
        raise ValueError(f"Shift with ID {shift_id} not found")
    
    if not data.get('shiftDate'):
        raise ValueError("Shift date is required")
    if not data.get('startTime'):
        raise ValueError("Start time is required")
    if not data.get('endTime'):
        raise ValueError("End time is required")
    
    if data['startTime'] >= data['endTime']:
        raise ValueError("Start time must be before end time")
    
    return update_shift(shift_id, data['shiftDate'], data['startTime'], data['endTime'])

def delete_shift_service(shift_id):
    existing = get_shift_by_id(shift_id)
    if not existing:
        raise ValueError(f"Shift with ID {shift_id} not found")
    
    return delete_shift(shift_id)

def assign_employee_to_shift_service(employee_id, shift_id):
    if not employee_id:
        raise ValueError("Employee ID is required")
    if not shift_id:
        raise ValueError("Shift ID is required")
    
    shift = get_shift_by_id(shift_id)
    if not shift:
        raise ValueError(f"Shift with ID {shift_id} not found")
    
    return assign_employee_to_shift(employee_id, shift_id)

def remove_employee_from_shift_service(employee_id, shift_id):
    return remove_employee_from_shift(employee_id, shift_id)

def get_all_employees_service():
    return get_all_employees()

def get_available_employees_for_shift_service(shift_id):
    return get_available_employees_for_shift(shift_id)

def get_shift_statistics_service():
    return get_shift_statistics()

def get_shifts_by_date_range_service(start_date, end_date):
    return get_shifts_by_date_range(start_date, end_date)

def get_employee_shifts_service(employee_id, start_date=None, end_date=None):
    return get_employee_shifts(employee_id, start_date, end_date)