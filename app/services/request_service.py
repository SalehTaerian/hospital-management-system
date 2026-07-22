from app.database.queries.request_queries import *

def get_patient_requests_service(patient_id):
    return get_patient_requests(patient_id)

def get_patient_pending_requests_service(patient_id):
    return get_patient_pending_requests(patient_id)

def get_doctor_requests_service(doctor_id):
    return get_doctor_requests(doctor_id)

def get_request_by_id_service(req_id):
    request = get_request_by_id(req_id)
    if not request:
        raise ValueError("Request not found")
    
    # Get parameters if it's a test request
    if request['testid']:
        parameters = get_request_parameters(req_id)
        request['parameters'] = parameters
    
    return request

def create_medicine_request_service(data):
    if not data.get('mID'):
        raise ValueError("Patient medical record is required")
    if not data.get('doctorID'):
        raise ValueError("Doctor ID is required")
    if not data.get('medID'):
        raise ValueError("Medicine is required")
    if not data.get('name'):
        raise ValueError("Request name is required")
    if not data.get('departID'):
        raise ValueError("Department is required")
    
    return create_medicine_request(data)

def create_test_request_service(data):
    if not data.get('mID'):
        raise ValueError("Patient medical record is required")
    if not data.get('doctorID'):
        raise ValueError("Doctor ID is required")
    if not data.get('testID'):
        raise ValueError("Test is required")
    if not data.get('name'):
        raise ValueError("Request name is required")
    if not data.get('departID'):
        raise ValueError("Department is required")
    
    return create_test_request(data)

def confirm_request_service(req_id, patient_id):
    request = get_request_by_id(req_id)
    if not request:
        raise ValueError("Request not found")
    
    from app.database.queries.request_queries import get_patient_medical_record_id
    mr_id = get_patient_medical_record_id(patient_id)
    if request['mid'] != mr_id:
        raise ValueError("You are not authorized to confirm this request")
    
    return confirm_request(req_id)

def cancel_request_service(req_id, doctor_id):
    request = get_request_by_id(req_id)
    if not request:
        raise ValueError("Request not found")
    
    if request['doctorid'] != doctor_id:
        raise ValueError("You are not authorized to cancel this request")
    
    return cancel_request(req_id)

def add_parameter_result_service(data):
    if not data.get('reqID'):
        raise ValueError("Request ID is required")
    if not data.get('parameterID'):
        raise ValueError("Parameter is required")
    if data.get('parameterValue') is None:
        raise ValueError("Parameter value is required")
    
    result = add_parameter_result(data)
    
    # Update request status to Completed if all parameters are added
    # This is optional - you can implement logic to check if all expected parameters are added
    
    return result

def update_request_status_service(req_id, status):
    return update_request_status(req_id, status)

def get_medicines_list_service():
    return get_medicines_list()

def get_tests_list_service():
    return get_tests_list()

def get_departments_list_service():
    return get_departments_list()