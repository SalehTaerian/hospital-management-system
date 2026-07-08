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