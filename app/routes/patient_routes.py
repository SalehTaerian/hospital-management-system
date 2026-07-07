from flask import Blueprint, render_template, request, session, redirect, url_for
from app.services.auth_service import get_doctors_service, get_patient_medical_info_service, is_logged_in

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

def patient_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'patient'

@patient_bp.route('/home')
def home():
    if not patient_login_required():
        return redirect('/patient-login')
    
    search_term = request.args.get('q', '').strip()
    doctors = get_doctors_service(search_term)
    
    return render_template('patient/home.html', doctors=doctors, user=session.get('user_name'))

@patient_bp.route('/medical-records')
def medical_records():
    if not patient_login_required():
        return redirect('/patient-login')
    
    medical_data = get_patient_medical_info_service(session.get('user_id'))
    
    return render_template(
        'patient/medical_records.html',
        info=medical_data.get('info'),
        diseases=medical_data.get('diseases'),
        drugs=medical_data.get('drugs'),
        medicines=medical_data.get('medicines')
    )