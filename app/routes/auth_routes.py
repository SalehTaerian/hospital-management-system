from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for
from app.services.auth_service import *

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/auth/patient-login')

@auth_bp.route('/')
@auth_bp.route('/patient-login', methods=['GET', 'POST'])
def patient_login():
    if is_logged_in() and session.get('user_role') == 'patient':
        return redirect('/patient/home')
    
    if request.method == 'POST':
        national_code = request.form.get('nationalCode')
        password = request.form.get('password')
        
        if not national_code or not password:
            return render_template('auth/login.html', error="Please enter national code and password")
        
        user = authenticate_patient(national_code, password)
        if not user:
            return render_template('auth/login.html', error="Invalid national code or password")
        
        login_patient(user)
        return redirect('/patient/home')
    
    return render_template('auth/login.html')

@auth_bp.route('/patient-register', methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        try:
            data = {
                'firstName': request.form.get('firstName'),
                'lastName': request.form.get('lastName'),
                'gender': request.form.get('gender'),
                'dateOfBirth': request.form.get('dateOfBirth'),
                'homeNumber': request.form.get('homeNumber'),
                'phoneNumber': request.form.get('phoneNumber'),
                'province': request.form.get('province'),
                'city': request.form.get('city'),
                'street': request.form.get('street'),
                'alley': request.form.get('alley'),
                'houseCode': request.form.get('houseCode'),
                'nationalCode': request.form.get('nationalCode'),
                'password': request.form.get('password')
            }
            
            register_patient(data)
            return render_template('auth/login.html', message="Registration successful! Please login.")
            
        except ValueError as e:
            return render_template('auth/register.html', error=str(e))
    
    return render_template('auth/register.html')

@auth_bp.route('/patient-logout')
def patient_logout():
    logout_patient()
    return redirect('/patient-login')

@auth_bp.route('/staff-login', methods=['GET', 'POST'])
def staff_login():
    if is_logged_in() and session.get('user_role') in ['doctor', 'surgeon', 'nurse', 'officeStaff']:
        if(session.get('user_role') == 'officeStaff' and session.get('accessLevel') == 'HospitalChief'):
            return redirect('/staff-management')
        return redirect('/staff/dashboard')
    
    if request.method == 'POST':
        national_code = request.form.get('nationalCode')
        password = request.form.get('password')
        
        if not national_code or not password:
            return render_template('auth/staff_login.html', error="Please enter national code and password")
        
        user = authenticate_employee(national_code, password)
        if not user:
            return render_template('auth/staff_login.html', error="Invalid national code or password")
        
        login_employee(user)
        if user['role'] == 'officeStaff' and user['accessLevel'] == 'HospitalChief':
            return redirect('/staff-management')
        elif user['role'] == 'officeStaff':
            return redirect('/staff/dashboard')
        else:
            return redirect('/staff/dashboard')
    
    return render_template('auth/staff_login.html')

@auth_bp.route('/staff-logout')
def staff_logout():
    logout_employee()
    return redirect('/auth/staff-login')

@auth_bp.route('/add-staff', methods=['GET', 'POST'])
def add_staff():
    if not is_logged_in():
        return redirect('/staff-login')
    if session.get('user_role') != 'officeStaff':
        return render_template('auth/unauthorized.html'), 403
    
    departments = get_departments_service()
    
    if request.method == 'POST':
        try:
            data = {
                'firstName': request.form.get('firstName'),
                'lastName': request.form.get('lastName'),
                'nationalCode': request.form.get('nationalCode'),
                'password': request.form.get('password'),
                'departID': request.form.get('department'),
                'contractType': request.form.get('contractType'),
                'hireDate': request.form.get('hireDate'),
                'accessLevel': request.form.get('accessLevel'),
                'salary': request.form.get('salary')
            }
            
            create_employee_service(data)
            return render_template('staff/add_staff.html', message="Staff member added successfully!", deps=departments)
            
        except ValueError as e:
            return render_template('staff/add_staff.html', error=str(e), deps=departments)
    
    return render_template('staff_management/add_staff.html', deps=departments)

@auth_bp.route('/check-session')
def check_session():
    return {
        'session': dict(session)
    }