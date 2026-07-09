from app.database.queries.patient_queries import *

def get_patient_upcoming_appointments_service(patient_id):
    return get_patient_upcoming_appointments(patient_id)

def get_patient_past_appointments_service(patient_id):
    return get_patient_past_appointments(patient_id)

def cancel_appointment_service(appointment_id, patient_id):
    result = cancel_appointment(appointment_id, patient_id)
    if not result:
        raise ValueError("Appointment not found or cannot be cancelled")
    return result

def get_patient_billing_service(patient_id):
    return get_patient_billing(patient_id)

def get_patient_admissions_service(patient_id):
    return get_patient_admissions(patient_id)

def get_patient_admission_by_id_service(admID, patient_id):
    admission = get_patient_admission_by_id(admID, patient_id)
    if not admission:
        raise ValueError("Admission not found or you don't have permission to view it")
    return admission

def get_patient_insurance_service(patient_id):
    return get_patient_insurance(patient_id)

def get_insurance_by_id_service(insurance_id, patient_id):
    insurance = get_insurance_by_id(insurance_id, patient_id)
    if not insurance:
        raise ValueError("Insurance record not found")
    return insurance

def create_insurance_service(data):
    if not data.get('name'):
        raise ValueError("Insurance name is required")
    if not data.get('policyNumber'):
        raise ValueError("Policy number is required")
    if not data.get('startDate'):
        raise ValueError("Start date is required")
    if not data.get('endDate'):
        raise ValueError("End date is required")
    
    patient_id = data.get('pID')
    if check_insurance_exists(patient_id):
        raise ValueError("You already have an insurance policy. Please edit the existing one.")
    
    return create_insurance(data)

def update_insurance_service(insurance_id, data):
    existing = get_insurance_by_id(insurance_id, data.get('pID'))
    if not existing:
        raise ValueError("Insurance record not found")
    if not data.get('name'):
        raise ValueError("Insurance name is required")
    if not data.get('policyNumber'):
        raise ValueError("Policy number is required")
    return update_insurance(insurance_id, data)

def delete_insurance_service(insurance_id, patient_id):
    existing = get_insurance_by_id(insurance_id, patient_id)
    if not existing:
        raise ValueError("Insurance record not found")
    return delete_insurance(insurance_id, patient_id)