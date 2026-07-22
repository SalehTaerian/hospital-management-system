from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.appointment_service import *
from app.services.auth_service import is_logged_in

appointment_bp = Blueprint('appointment', __name__, url_prefix='/appointments')

def patient_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'patient'

def staff_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') in ['doctor', 'surgeon', 'nurse', 'officeStaff']

@appointment_bp.route('/')
def index():
    if not patient_login_required():
        return redirect('/patient-login')
    return render_template('patient/appointments_with_followup.html')

@appointment_bp.route('/staff')
def staff_index():
    if not staff_login_required():
        return redirect('/staff-login')
    return render_template('staff/appointments_with_followup.html')

@appointment_bp.route('/api/patient/appointments', methods=['GET'])
def api_get_patient_appointments():
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    appointments = get_patient_appointments_with_followup_service(patient_id)
    return jsonify({'success': True, 'data': appointments})

@appointment_bp.route('/api/patient/appointments/available', methods=['GET'])
def api_get_available_appointments():
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    current_id = request.args.get('current_id', type=int)
    appointments = get_available_appointments_for_followup_service(patient_id, current_id)
    return jsonify({'success': True, 'data': appointments})

@appointment_bp.route('/api/followup/<int:follow_id>', methods=['GET'])
def api_get_followup_chain(follow_id):
    if not is_logged_in():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    chain = get_followup_chain_service(follow_id)
    return jsonify({'success': True, 'data': chain})

@appointment_bp.route('/api/followup/<int:follow_id>/progress', methods=['PUT'])
def api_update_followup_progress(follow_id):
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        progress = data.get('progress')
        if progress is None:
            return jsonify({'success': False, 'error': 'Progress is required'}), 400
        
        result = update_followup_progress_service(follow_id, progress)
        return jsonify({
            'success': True,
            'message': 'Progress updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400