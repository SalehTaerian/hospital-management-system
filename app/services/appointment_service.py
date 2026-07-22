from app.database.queries.followup_queries import *
from datetime import datetime

def get_patient_appointments_with_followup_service(patient_id):
    return get_appointments_with_followup(patient_id)

def get_available_appointments_for_followup_service(patient_id, current_appointment_id=None):
    return get_available_appointments_for_followup(patient_id, current_appointment_id)

def create_appointment_with_followup_service(data):
    if not data.get('patient_id'):
        raise ValueError("Patient is required")
    if not data.get('doctor_id'):
        raise ValueError("Doctor is required")
    if not data.get('date'):
        raise ValueError("Date is required")
    if not data.get('time'):
        raise ValueError("Time is required")
    
    try:
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if appointment_date < datetime.now().date():
            raise ValueError("Cannot book appointment in the past")
    except ValueError:
        raise ValueError("Invalid date format")
    
    mr_query = "SELECT mID FROM medicalRecord WHERE pID = %s"
    mr_result = DatabaseConnection.execute_query(
        mr_query, (data["patient_id"],), fetch_one=True, fetch_dict=True
    )

    if not mr_result:
        raise ValueError("Patient has no medical record")
    
    data['mID'] = mr_result
    
    follow_id = data.get('followID')
    if not follow_id:
        follow_id = create_followup(0)
        if not follow_id:
            raise ValueError("Failed to create followup record")
        data['followID'] = follow_id
    
    return create_appointment_with_followup(data)

def get_appointment_with_followup_service(appointment_id):
    return get_appointment_by_id_with_followup(appointment_id)

def get_followup_chain_service(follow_id):
    return get_followup_chain(follow_id)

def update_followup_progress_service(follow_id, progress):
    if progress < 0 or progress > 100:
        raise ValueError("Progress must be between 0 and 100")
    return update_followup_progress(follow_id, progress)

def get_doctor_appointments_with_followup_service(doctor_id):
    return get_appointments_with_followup(doctor_id)