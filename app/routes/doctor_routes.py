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

@doctor_bp.route('/appointments')
def appointments():
    if not doctor_login_required():
        return redirect('/staff-login')
    
    return render_template('doctor/appointments.html')

@doctor_bp.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    if not doctor_login_required():
        return redirect('/staff-login')
    
    return render_template('doctor/patient_detail.html', patient_id=patient_id)

@doctor_bp.route('/appointment/<int:appointment_id>')
def appointment_detail(appointment_id):
    if not doctor_login_required():
        return redirect('/staff-login')
    medicineAllergy = get_medicine_allergy_service(appointment_id)
    return render_template('doctor/appointment_detail.html', appointment_id=appointment_id, medicineAllergy = medicineAllergy)


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


@doctor_bp.route('/api/appointments', methods=['GET'])
def api_get_appointments():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    doctor_id = session.get('user_id')
    appointments = get_doctor_appointments_service(doctor_id)
    return jsonify({'success': True, 'data': appointments})

@doctor_bp.route('/api/appointment/<int:appointment_id>', methods=['GET'])
def api_get_appointment(appointment_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        appointment = get_appointment_by_id_service(appointment_id)
        return jsonify({'success': True, 'data': appointment})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@doctor_bp.route('/api/disease/diagnosis', methods=['POST'])
def api_add_disease_diagnosis():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_disease_diagnosis_service(data)
        return jsonify({
            'success': True,
            'message': 'Disease diagnosis added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@doctor_bp.route('/api/disease/history', methods=['POST'])
def api_add_disease_history():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_disease_history_service(data)
        return jsonify({
            'success': True,
            'message': 'Disease history added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@doctor_bp.route('/api/disease/codes', methods=['GET'])
def api_get_disease_codes():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    codes = get_icd_codes_service()
    return jsonify({'success': True, 'data': codes})


@doctor_bp.route('/api/medicine/diagnosis', methods=['POST'])
def api_add_medicine_diagnosis():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_medicine_diagnosis_service(data)
        return jsonify({
            'success': True,
            'message': 'Medicine diagnosis added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@doctor_bp.route('/api/medicine/history', methods=['POST'])
def api_add_medicine_history():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_medicine_history_service(data)
        return jsonify({
            'success': True,
            'message': 'Medicine history added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@doctor_bp.route('/api/medicine/codes', methods=['GET'])
def api_get_medicine_codes():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    codes = get_icdm_codes_service()
    return jsonify({'success': True, 'data': codes})


@doctor_bp.route('/api/drug/history', methods=['POST'])
def api_add_drug_history():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_drug_history_service(data)
        return jsonify({
            'success': True,
            'message': 'Drug history added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@doctor_bp.route('/api/vital/sign', methods=['POST'])
def api_add_vital_sign():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = add_vital_sign_service(data)
        return jsonify({
            'success': True,
            'message': 'Vital sign added successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@doctor_bp.route('/api/vital/parameters', methods=['GET'])
def api_get_vital_parameters():
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    parameters = get_parameter_list_service()
    return jsonify({'success': True, 'data': parameters})


@doctor_bp.route('/api/patient/<int:patient_id>/history/diseases', methods=['GET'])
def api_get_patient_disease_history(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    history = get_patient_disease_history_service(patient_id)
    return jsonify({'success': True, 'data': history})

@doctor_bp.route('/api/patient/<int:patient_id>/history/medicines', methods=['GET'])
def api_get_patient_medicine_history(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    history = get_patient_medicine_history_service(patient_id)
    return jsonify({'success': True, 'data': history})

@doctor_bp.route('/api/patient/<int:patient_id>/history/drugs', methods=['GET'])
def api_get_patient_drug_history(patient_id):
    if not doctor_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    history = get_patient_drug_history_service(patient_id)
    return jsonify({'success': True, 'data': history})