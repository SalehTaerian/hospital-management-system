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
    appointments = get_doctor_appointments(doctor_id)
    
    for apt in appointments:
        if 'time' in apt and apt['time']:
            apt['time'] = str(apt['time'])
        if 'date' in apt and apt['date']:
            apt['date'] = str(apt['date'])
        if 'createdat' in apt and apt['createdat']:
            apt['createdat'] = str(apt['createdat'])
    
    return appointments

def get_appointment_by_id_service(appointment_id):
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        raise ValueError("Appointment not found")
    
    if 'time' in appointment and appointment['time']:
        appointment['time'] = str(appointment['time'])
    if 'date' in appointment and appointment['date']:
        appointment['date'] = str(appointment['date'])
    if 'createdat' in appointment and appointment['createdat']:
        appointment['createdat'] = str(appointment['createdat'])
    
    diseases = get_appointment_diseases(appointment_id)
    medicines = get_appointment_medicines(appointment_id)
    vitals = get_appointment_vitals(appointment_id)
    
    appointment['diseases'] = diseases
    appointment['medicines'] = medicines
    appointment['vitals'] = vitals
    
    return appointment
def add_disease_diagnosis_service(data):
    if not data.get('appoID'):
        raise ValueError("Appointment ID is required")
    if not data.get('icdID'):
        raise ValueError("Disease is required")
    return add_disease_diagnosis(data)

def add_disease_history_service(data):
    if not data.get('mID'):
        raise ValueError("Medical record ID is required")
    if not data.get('icdID'):
        raise ValueError("Disease is required")
    return add_disease_history(data)

def add_medicine_diagnosis_service(data):
    if not data.get('appoID'):
        raise ValueError("Appointment ID is required")
    if not data.get('icdmID'):
        raise ValueError("Medicine is required")
    return add_medicine_diagnosis(data)

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

def get_patient_logs_service(patient_id):
    return get_patient_logs(patient_id)