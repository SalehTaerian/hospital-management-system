from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.request_service import *
from app.services.auth_service import is_logged_in
from app.database.queries.request_queries import get_patient_medical_record_id

request_bp = Blueprint('request', __name__, url_prefix='/requests')

def patient_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'patient'

def doctor_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'doctor'

@request_bp.route('/patient')
def patient_requests():
    if not patient_login_required():
        return redirect('/patient-login')
    
    return render_template('patient/requests.html')

@request_bp.route('/doctor')
def doctor_requests():
    if not doctor_login_required():
        return redirect('/staff-login')
    
    return render_template('staff/requests.html')

@request_bp.route('/doctor/create')
def create_request():
    if not doctor_login_required():
        return redirect('/staff-login')
    
    departments = get_departments_list_service()
    return render_template('staff/create_request.html', departments=departments)

@request_bp.route('/api/patient', methods=['GET'])
def api_get_patient_requests():
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    requests = get_patient_requests_service(patient_id)
    return jsonify({'success': True, 'data': requests})

@request_bp.route('/api/patient/pending', methods=['GET'])
def api_get_patient_pending_requests():
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    requests = get_patient_pending_requests_service(patient_id)
    return jsonify({'success': True, 'data': requests})

@request_bp.route('/api/doctor', methods=['GET'])
def api_get_doctor_requests():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    doctor_id = session.get('user_id')
    requests = get_doctor_requests_service(doctor_id)
    return jsonify({'success': True, 'data': requests})

@request_bp.route('/api/medicine', methods=['POST'])
def api_create_medicine_request():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['doctorID'] = session.get('user_id')
        req_id = create_medicine_request_service(data)
        return jsonify({
            'success': True,
            'message': 'Medicine request created successfully',
            'id': req_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@request_bp.route('/api/test', methods=['POST'])
def api_create_test_request():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        data['doctorID'] = session.get('user_id')
        req_id = create_test_request_service(data)
        return jsonify({
            'success': True,
            'message': 'Test request created successfully',
            'id': req_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@request_bp.route('/api/<int:req_id>/confirm', methods=['POST'])
def api_confirm_request(req_id):
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        patient_id = session.get('user_id')
        result = confirm_request_service(req_id, patient_id)
        return jsonify({
            'success': True,
            'message': 'Request confirmed successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@request_bp.route('/api/<int:req_id>/cancel', methods=['POST'])
def api_cancel_request(req_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        doctor_id = session.get('user_id')
        result = cancel_request_service(req_id, doctor_id)
        return jsonify({
            'success': True,
            'message': 'Request cancelled successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@request_bp.route('/api/medicines', methods=['GET'])
def api_get_medicines():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    medicines = get_medicines_list_service()
    return jsonify({'success': True, 'data': medicines})

@request_bp.route('/api/tests', methods=['GET'])
def api_get_tests():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    tests = get_tests_list_service()
    return jsonify({'success': True, 'data': tests})

@request_bp.route('/api/departments', methods=['GET'])
def api_get_departments():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    departments = get_departments_list_service()
    return jsonify({'success': True, 'data': departments})

@request_bp.route('/api/patient/mid', methods=['GET'])
def api_get_patient_mid():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({'success': False, 'error': 'Patient ID is required'}), 400
    
    mid = get_patient_medical_record_id(patient_id)
    if not mid:
        return jsonify({'success': False, 'error': 'Patient has no medical record'}), 404
    
    return jsonify({'success': True, 'data': {'mID': mid}})