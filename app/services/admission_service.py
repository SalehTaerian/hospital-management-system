from app.database.queries.admission_queries import *
from app.services.auth_service import is_logged_in

def get_all_admissions_service():
    return get_all_admissions()

def get_admission_by_id_service(admID):
    admission = get_admission_by_id(admID)
    if not admission:
        raise ValueError(f"Admission with ID {admID} not found")
    return admission

def create_admission_service(data, officeStaffID):
    if not data.get('patient_id'):
        raise ValueError("Patient is required")
    if not data.get('doctor_id'):
        raise ValueError("Doctor is required")
    if not data.get('bed_id'):
        raise ValueError("Bed is required")
    if not data.get('room_id'):
        raise ValueError("Room is required")
    
    mID = get_medical_record_by_patient(data['patient_id'])
    if not mID:
        raise ValueError("Patient has no medical record")
    
    admission_data = {
        'mID': mID,
        'doctorID': data['doctor_id'],
        'officeStaffID': officeStaffID,
        'cost': data.get('cost', 0)
    }
    
    admID = create_admission(admission_data)
    if not admID:
        raise ValueError("Failed to create admission")
    
    assign_bed_to_admission(admID, data['bed_id'], data['room_id'])
    
    return admID

def update_admission_cost_service(admID, cost):
    existing = get_admission_by_id(admID)
    if not existing:
        raise ValueError(f"Admission with ID {admID} not found")
    
    return update_admission_cost(admID, cost)

def delete_admission_service(admID):
    existing = get_admission_by_id(admID)
    if not existing:
        raise ValueError(f"Admission with ID {admID} not found")
    
    discharge_patient(admID)
    return delete_admission(admID)

def discharge_patient_service(admID):
    existing = get_admission_by_id(admID)
    if not existing:
        raise ValueError(f"Admission with ID {admID} not found")
    
    return discharge_patient(admID)

def get_available_beds_service():
    return get_available_beds()

def get_all_doctors_service():
    return get_all_doctors()

def get_all_rooms_service():
    return get_all_rooms()

def get_beds_by_room_service(roomID):
    return get_beds_by_room(roomID)

def transfer_patient_service(admID, new_bedID, new_roomID, cost):
    existing = get_admission_by_id(admID)
    if not existing:
        raise ValueError(f"Admission with ID {admID} not found")
    
    if existing['bed_status'] != 'Occupied':
        raise ValueError("Patient is not currently admitted")
    
    return transfer_patient(admID, new_bedID, new_roomID, cost)

def get_transfer_history_service(admID):
    return get_transfer_history(admID)