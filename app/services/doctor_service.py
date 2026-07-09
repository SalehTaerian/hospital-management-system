from app.database.queries.doctor_queries import *

def get_doctor_patients_service(doctor_id):
    return get_doctor_patients(doctor_id)

def get_patient_logs_service(patient_id):
    return get_patient_logs(patient_id)

def get_patient_warnings_service(patient_id):
    return get_patient_warnings(patient_id)

def get_latest_logs_for_patients_service(patient_ids):
    return get_latest_logs_for_patients(patient_ids)

def get_all_active_warnings_service():
    return get_all_active_warnings()

def mark_warning_checked_service(warning_id):
    return mark_warning_checked(warning_id)

def mark_warnings_checked_for_patient_service(patient_id):
    return mark_warnings_checked_for_patient(patient_id)