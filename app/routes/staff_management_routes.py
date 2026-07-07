from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.routes.auth_routes import staff_logout
from app.services.staff_management_service import *
from app.services.auth_service import get_departments_service, is_logged_in

staff_mgmt_bp = Blueprint('staff_management', __name__, url_prefix='/staff-management')

def office_staff_required():
    if not is_logged_in():
        return False
    if session.get('access_level') != 'HospitalChief':
        redirect('/staff/dashboard')
        return True
    return session.get('user_role') == 'officeStaff'

@staff_mgmt_bp.route('/')
def index():
    if not office_staff_required():
        return redirect('/staff-login')
    
    departments = get_departments_service()
    return render_template('staff_management/index.html', departments=departments)

@staff_mgmt_bp.route('/add')
def add_staff_page():
    if not office_staff_required():
        return redirect('/staff-login')
    
    departments = get_departments_service()
    return render_template('staff_management/add_staff.html', departments=departments)

@staff_mgmt_bp.route('/edit/<int:employee_id>')
def edit_staff_page(employee_id):
    if not office_staff_required():
        return redirect('/staff-login')
    
    try:
        staff = get_staff_by_id_service(employee_id)
        departments = get_departments_service()
        return render_template('staff_management/edit_staff.html', 
                             staff=staff, 
                             departments=departments)
    except ValueError as e:
        return render_template('staff_management/error.html', error=str(e))

@staff_mgmt_bp.route('/api/staff', methods=['GET'])
def api_get_all_staff():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    staff = get_all_staff_service()
    return jsonify({'success': True, 'data': staff})

@staff_mgmt_bp.route('/api/staff/<int:employee_id>', methods=['GET'])
def api_get_staff(employee_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        staff = get_staff_by_id_service(employee_id)
        return jsonify({'success': True, 'data': staff})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@staff_mgmt_bp.route('/api/staff', methods=['POST'])
def api_create_staff():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        employee_id = create_employee_service(data)
        return jsonify({
            'success': True,
            'message': 'Staff member created successfully',
            'id': employee_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_mgmt_bp.route('/api/staff/<int:employee_id>', methods=['PUT'])
def api_update_staff(employee_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = update_employee_service(employee_id, data)
        return jsonify({
            'success': True,
            'message': 'Staff member updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_mgmt_bp.route('/api/staff/<int:employee_id>', methods=['DELETE'])
def api_delete_staff(employee_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        if employee_id == session.get('user_id'):
            return jsonify({'success': False, 'error': 'You cannot delete yourself'}), 400
        
        result = delete_employee_service(employee_id)
        return jsonify({
            'success': True,
            'message': 'Staff member deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_mgmt_bp.route('/api/staff/<int:employee_id>/role', methods=['PUT'])
def api_update_staff_role(employee_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        new_role = data.get('role')
        
        if not new_role:
            return jsonify({'success': False, 'error': 'Role is required'}), 400
        
        result = update_employee_role_service(employee_id, new_role)
        return jsonify({
            'success': True,
            'message': f'Role updated to {new_role} successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@staff_mgmt_bp.route('/api/stats', methods=['GET'])
def api_get_staff_stats():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    total = get_staff_count_service()
    doctors = get_staff_by_role_service('doctor')
    surgeons = get_staff_by_role_service('surgeon')
    nurses = get_staff_by_role_service('nurse')
    office_staff = get_staff_by_role_service('officeStaff')
    
    return jsonify({
        'success': True,
        'data': {
            'total': total,
            'doctors': len(doctors),
            'surgeons': len(surgeons),
            'nurses': len(nurses),
            'officeStaff': len(office_staff)
        }
    })