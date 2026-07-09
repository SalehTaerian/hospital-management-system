from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.doctor_service import *
from app.services.auth_service import is_logged_in

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

def doctor_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'doctor'

@doctor_bp.route('/patients')
def patients():
    if not doctor_login_required():
        return redirect('/staff-login')
    
    return render_template('doctor/patients.html')

@doctor_bp.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    if not doctor_login_required():
        return redirect('/staff-login')
    
    return render_template('doctor/patient_detail.html', patient_id=patient_id)

@doctor_bp.route('/api/patients', methods=['GET'])
def api_get_patients():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    doctor_id = session.get('user_id')
    patients = get_doctor_patients_service(doctor_id)
    return jsonify({'success': True, 'data': patients})

@doctor_bp.route('/api/patient/<int:patient_id>/logs', methods=['GET'])
def api_get_patient_logs(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    logs = get_patient_logs_service(patient_id)
    return jsonify({'success': True, 'data': logs})

@doctor_bp.route('/api/patient/<int:patient_id>/warnings', methods=['GET'])
def api_get_patient_warnings(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    warnings = get_patient_warnings_service(patient_id)
    return jsonify({'success': True, 'data': warnings})

@doctor_bp.route('/api/warnings/active', methods=['GET'])
def api_get_active_warnings():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    warnings = get_all_active_warnings_service()
    return jsonify({'success': True, 'data': warnings})

@doctor_bp.route('/api/warning/<int:warning_id>/check', methods=['POST'])
def api_mark_warning_checked(warning_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = mark_warning_checked_service(warning_id)
        if not result:
            return jsonify({'success': False, 'error': 'Warning not found'}), 404
        return jsonify({
            'success': True,
            'message': 'Warning marked as checked'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@doctor_bp.route('/api/patient/<int:patient_id>/warnings/check-all', methods=['POST'])
def api_mark_all_warnings_checked(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        results = mark_warnings_checked_for_patient_service(patient_id)
        return jsonify({
            'success': True,
            'message': f'Marked {len(results)} warnings as checked',
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@doctor_bp.route('/api/patient/<int:patient_id>/warnings/unchecked', methods=['GET'])
def api_get_unchecked_warnings(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    warnings = get_patient_warnings_service(patient_id)
    # Filter only unchecked warnings
    unchecked = [w for w in warnings if w.get('checkedstatus') == 'Unchecked']
    return jsonify({'success': True, 'data': unchecked})