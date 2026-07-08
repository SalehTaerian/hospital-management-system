from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.auth_service import get_doctors_service, is_logged_in
from app.services.patient_service import *

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

def patient_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'patient'

@patient_bp.route('/home')
def home():
    if not patient_login_required():
        return redirect('/auth/patient-login')
    
    search_term = request.args.get('q', '').strip()
    doctors = get_doctors_service(search_term)
    
    return render_template('patient/home.html', 
                         doctors=doctors, 
                         user=session.get('user_name'))

@patient_bp.route('/medical-records')
def medical_records():
    """Patient medical records page"""
    if not patient_login_required():
        return redirect('/patient-login')
    
    from app.services.auth_service import get_patient_medical_info_service
    medical_data = get_patient_medical_info_service(session.get('user_id'))
    
    return render_template(
        'patient/medical_records.html',
        info=medical_data.get('info'),
        diseases=medical_data.get('diseases'),
        drugs=medical_data.get('drugs'),
        medicines=medical_data.get('medicines')
    )

@patient_bp.route('/appointments')
def appointments():
    """Patient appointments page"""
    if not patient_login_required():
        return redirect('/patient-login')
    
    return render_template('patient/appointments.html')

# ==================== API ROUTES ====================

@patient_bp.route('/api/appointments/upcoming', methods=['GET'])
def api_get_upcoming_appointments():
    """Get upcoming appointments for the logged-in patient"""
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    appointments = get_patient_upcoming_appointments_service(patient_id)
    return jsonify({'success': True, 'data': appointments})

@patient_bp.route('/api/appointments/past', methods=['GET'])
def api_get_past_appointments():
    """Get past appointments for the logged-in patient"""
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    appointments = get_patient_past_appointments_service(patient_id)
    return jsonify({'success': True, 'data': appointments})

@patient_bp.route('/api/appointments/<int:appointment_id>/cancel', methods=['POST'])
def api_cancel_appointment(appointment_id):
    """Cancel an appointment"""
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        patient_id = session.get('user_id')
        result = cancel_appointment_service(appointment_id, patient_id)
        return jsonify({
            'success': True,
            'message': 'Appointment cancelled successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@patient_bp.route('/api/billing', methods=['GET'])
def api_get_billing():
    """Get billing information for the logged-in patient"""
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    billing = get_patient_billing_service(patient_id)
    return jsonify({'success': True, 'data': billing})