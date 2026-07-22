from app.database.queries.doctor_queries import *

def get_doctor_patients_service(doctor_id):
    return get_doctor_patients(doctor_id)

def get_patient_logs_service(patient_id):
    return get_patient_logs(patient_id)

def get_patient_warnings_service(patient_id):
    return get_patient_warnings(patient_id)

def get_all_active_warnings_service():
    return get_all_active_warnings()

def mark_warning_checked_service(warning_id):
    return mark_warning_checked(warning_id)

def mark_warnings_checked_for_patient_service(patient_id):
    return mark_warnings_checked_for_patient(patient_id)

def get_doctor_appointments_service(doctor_id):
    return get_doctor_appointments(doctor_id)

def get_appointment_by_id_service(appointment_id):
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    
    diseases = get_appointment_diseases(appointment_id)
    
    for disease in diseases:
        disease['medicines'] = get_disease_medicines_with_feedback(disease['disdiagid'])
    
    vitals = get_appointment_vitals(appointment_id)
    
    appointment['diseases'] = diseases
    appointment['vitals'] = vitals
    
    return appointment

def get_disease_with_medicines_service(dis_diag_id):
    disease = get_disease_by_id(dis_diag_id)
    if not disease:
        raise ValueError("Disease not found")
    
    disease['medicines'] = get_disease_medicines_with_feedback(dis_diag_id)
    return disease

def add_disease_diagnosis_service(data):
    if not data.get('appoID'):
        raise ValueError("Appointment ID is required")
    if not data.get('icdID'):
        raise ValueError("Disease is required")
    return add_disease_diagnosis(data)

def update_disease_diagnosis_service(dis_diag_id, data):
    if not data.get('icdID'):
        raise ValueError("Disease is required")
    existing = get_disease_by_id(dis_diag_id)
    if not existing:
        raise ValueError("Disease not found")
    return update_disease_diagnosis(dis_diag_id, data)

def delete_disease_diagnosis_service(dis_diag_id):
    existing = get_disease_by_id(dis_diag_id)
    if not existing:
        raise ValueError("Disease not found")
    return delete_disease_diagnosis(dis_diag_id)

def add_medicine_to_disease_service(data):
    if not data.get('disDiagID'):
        raise ValueError("Disease diagnosis ID is required")
    if not data.get('icdmID'):
        raise ValueError("Medicine is required")
    
    disease = get_disease_by_id(data['disDiagID'])
    if not disease:
        raise ValueError("Disease diagnosis not found")
    
    return add_medicine_to_disease(data)

def delete_medicine_from_disease_service(med_diag_id):
    return delete_medicine_from_disease(med_diag_id)

def add_disease_history_service(data):
    if not data.get('mID'):
        raise ValueError("Medical record ID is required")
    if not data.get('icdID'):
        raise ValueError("Disease is required")
    return add_disease_history(data)

def add_medicine_history_service(data):
    if not data.get('mID'):
        raise ValueError("Medical record ID is required")
    if not data.get('icdmID'):
        raise ValueError("Medicine is required")
    return add_medicine_history(data)

def add_drug_history_service(data):
    if not data.get('mID'):
        raise ValueError("Medical record ID is required")
    if not data.get('description'):
        raise ValueError("Drug description is required")
    return add_drug_history(data)

def add_vital_sign_service(data):
    if not data.get('appoID'):
        raise ValueError("Appointment ID is required")
    if not data.get('parameterID'):
        raise ValueError("Parameter is required")
    if data.get('parameterValue') is None:
        raise ValueError("Value is required")
    return add_vital_sign(data)

def get_icd_codes_service():
    return get_icd_codes()

def get_icdm_codes_service():
    return get_icdm_codes()

def get_parameter_list_service():
    return get_parameter_list()

def get_patient_disease_history_service(patient_id):
    return get_patient_disease_history(patient_id)

def get_patient_medicine_history_service(patient_id):
    return get_patient_medicine_history(patient_id)

def get_patient_drug_history_service(patient_id):
    return get_patient_drug_history(patient_id)

def get_medicine_feedback_service(med_diag_id):
    return get_medicine_feedback(med_diag_id)

def add_or_update_feedback_service(data):
    if not data.get('medDiagID'):
        raise ValueError("Medicine diagnosis ID is required")
    if data.get('effectPercentage') is None:
        raise ValueError("Effectiveness percentage is required")
    if data.get('effectPercentage') < 0 or data.get('effectPercentage') > 100:
        raise ValueError("Effectiveness percentage must be between 0 and 100")
    return add_or_update_feedback(data)

def delete_feedback_service(med_diag_id):
    return delete_feedback(med_diag_id)