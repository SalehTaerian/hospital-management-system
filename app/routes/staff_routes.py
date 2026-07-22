from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.auth_service import is_logged_in
from app.services.staff_service import *
import matplotlib.pyplot as plt
import io
import base64
staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

def staff_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') in ['doctor', 'surgeon', 'nurse', 'officeStaff']

def office_staff_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'officeStaff'

@staff_bp.route('/dashboard')
def dashboard():
    if not staff_login_required():
        return redirect('/staff-login')
    # occupiedBeds = get_occupied_beds_by_department()
    # names = [item["name"] for item in occupiedBeds]
    # values = [item["occupied"] for item in occupiedBeds]
    # plt.figure()
    # plt.bar(names , values)
    # plt.title("Occupied Beds by Department")
    # plt.xlabel("Department")
    # plt.ylabel("Occupied Beds")
    # img = io.BytesIO()
    # plt.savefig(img, format="png")
    # img.seek(0)
    # plt.close()
    # imgBase64 = base64.b64encode(img.getvalue()).decode('utf-8')
    # return render_template('staff/dashboard.html' , chart = imgBase64)
    return render_template('staff/dashboard.html')

@staff_bp.route('/patients')
def patients():
    if not staff_login_required():
        return redirect('/staff-login')
    
    return render_template('staff/patients.html')

@staff_bp.route('/appointments')
def appointments():
    if not staff_login_required():
        return redirect('/staff-login')
    
    return render_template('staff/appointments.html')

@staff_bp.route('/surgeries')
def surgeries():
    if not staff_login_required():
        return redirect('/staff-login')
    
    return render_template('staff/surgeries.html')

@staff_bp.route('/patient/<int:patient_id>')
def patient_detail(patient_id):
    if not staff_login_required():
        return redirect('/staff-login')
    
    return render_template('staff/patient_detail.html', patient_id=patient_id)

@staff_bp.route('/api/patients/search', methods=['GET'])
def api_search_patients():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    search_term = request.args.get('q', '')
    results = search_patients_service(search_term)
    return jsonify({'success': True, 'data': results})

@staff_bp.route('/api/patients/<int:patient_id>', methods=['GET'])
def api_get_patient(patient_id):
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        patient = get_patient_basic_info_service(patient_id)
        return jsonify({'success': True, 'data': patient})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@staff_bp.route('/api/doctors', methods=['GET'])
def api_get_doctors():
    if not staff_login_required():
        return jsonify({'success ': False, 'error': 'Unauthorized'}), 401
    
    doctors = get_doctors_service()
    return jsonify({'success': True, 'data': doctors})

@staff_bp.route('/api/doctors/available', methods=['GET'])
def api_get_available_doctors():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    date = request.args.get('date')
    if not date:
        return jsonify({'success': False, 'error': 'Date is required'}), 400
    
    doctors = get_doctors_with_availability_service(date)
    return jsonify({'success': True, 'data': doctors})

@staff_bp.route('/api/doctors/<int:doctor_id>/slots', methods=['GET'])
def api_get_doctor_slots(doctor_id):
    # if not staff_login_required():
    #     print("Unauthorized access attempt to get doctor slots")
    #     return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    date = request.args.get('date')
    if not date:
        return jsonify({'success': False, 'error': 'Date is required'}), 400
    
    slots = get_available_slots_service(doctor_id, date)
    return jsonify({'success': True, 'data': slots})

@staff_bp.route('/api/appointments', methods=['POST'])
def api_create_appointment():
    # if not staff_login_required():
    #     return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        
        appointment_id = create_appointment_service(data)
        return jsonify({
            'success': True,
            'message': 'Appointment created successfully',
            'id': appointment_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_bp.route('/api/appointments/<int:appointment_id>/status', methods=['PUT'])
def api_update_appointment_status(appointment_id):
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        result = update_appointment_status_service(appointment_id, status)
        if not result:
            return jsonify({'success': False, 'error': 'Appointment not found'}), 404
        
        return jsonify({
            'success': True,
            'message': f'Appointment status updated to {status}',
            'id': appointment_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_bp.route('/api/appointments/today', methods=['GET'])
def api_get_today_appointments():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    appointments = get_today_appointments_service()
    return jsonify({'success': True, 'data': appointments})

@staff_bp.route('/api/surgeons', methods=['GET'])
def api_get_surgeons():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    surgeons = get_surgeons_service()
    return jsonify({'success': True, 'data': surgeons})

@staff_bp.route('/api/surgery-codes', methods=['GET'])
def api_get_surgery_codes():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    codes = get_surgery_codes_service()
    return jsonify({'success': True, 'data': codes})

@staff_bp.route('/api/rooms', methods=['GET'])
def api_get_rooms():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    rooms = get_rooms_service()
    return jsonify({'success': True, 'data': rooms})

@staff_bp.route('/api/surgeries', methods=['POST'])
def api_create_surgery():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        surgery_id = create_surgery_service(data)
        return jsonify({
            'success': True,
            'message': 'Surgery scheduled successfully',
            'id': surgery_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_bp.route('/api/surgeries/today', methods=['GET'])
def api_get_today_surgeries():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    surgeries = get_today_surgeries_service()
    return jsonify({'success': True, 'data': surgeries})

@staff_bp.route('/api/dashboard/stats', methods=['GET'])
def api_get_dashboard_stats():
    if not staff_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    stats = get_dashboard_stats_service()
    return jsonify({'success': True, 'data': stats})

@staff_bp.route('/api/patients-admission/<int:patient_id>', methods=['GET'])
def api_get_patient_with_admission_info_service(patient_id):
    try:
        patient = get_patient_with_admission_info_service(patient_id)
        return jsonify({'success': True, 'data': patient})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404