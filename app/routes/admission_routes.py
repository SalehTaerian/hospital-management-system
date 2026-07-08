from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.admission_service import *
from app.services.auth_service import is_logged_in

admission_bp = Blueprint('admission', __name__, url_prefix='/admissions')

def office_staff_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'officeStaff'

@admission_bp.route('/')
def index():
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('admission/index.html')

@admission_bp.route('/create')
def create():
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('admission/create.html')

@admission_bp.route('/<int:admID>')
def detail(admID):
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('admission/detail.html', admID=admID)

@admission_bp.route('/api/admissions', methods=['GET'])
def api_get_admissions():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    admissions = get_all_admissions_service()
    return jsonify({'success': True, 'data': admissions})

@admission_bp.route('/api/admissions/<int:admID>', methods=['GET'])
def api_get_admission(admID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        admission = get_admission_by_id_service(admID)
        transfers = get_transfer_history_service(admID)
        return jsonify({
            'success': True,
            'data': admission,
            'transfers': transfers
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@admission_bp.route('/api/admissions', methods=['POST'])
def api_create_admission():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        admID = create_admission_service(data, session.get('user_id'))
        return jsonify({
            'success': True,
            'message': 'Admission created successfully',
            'id': admID
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@admission_bp.route('/api/admissions/<int:admID>', methods=['PUT'])
def api_update_admission(admID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = update_admission_cost_service(admID, data.get('cost', 0))
        return jsonify({
            'success': True,
            'message': 'Admission updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@admission_bp.route('/api/admissions/<int:admID>', methods=['DELETE'])
def api_delete_admission(admID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = delete_admission_service(admID)
        return jsonify({
            'success': True,
            'message': 'Admission deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@admission_bp.route('/api/admissions/<int:admID>/discharge', methods=['POST'])
def api_discharge_patient(admID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = discharge_patient_service(admID)
        return jsonify({
            'success': True,
            'message': 'Patient discharged successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@admission_bp.route('/api/beds/available', methods=['GET'])
def api_get_available_beds():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    beds = get_available_beds_service()
    return jsonify({'success': True, 'data': beds})

@admission_bp.route('/api/doctors', methods=['GET'])
def api_get_doctors():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    doctors = get_all_doctors_service()
    return jsonify({'success': True, 'data': doctors})

@admission_bp.route('/api/rooms', methods=['GET'])
def api_get_rooms():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    rooms = get_all_rooms_service()
    return jsonify({'success': True, 'data': rooms})

@admission_bp.route('/api/rooms/<int:roomID>/beds', methods=['GET'])
def api_get_beds_by_room(roomID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    beds = get_beds_by_room_service(roomID)
    return jsonify({'success': True, 'data': beds})

@admission_bp.route('/api/admissions/<int:admID>/transfer', methods=['POST'])
def api_transfer_patient(admID):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = transfer_patient_service(
            admID,
            data.get('bed_id'),
            data.get('room_id'),
            data.get('cost', 0)
        )
        return jsonify({
            'success': True,
            'message': 'Patient transferred successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400