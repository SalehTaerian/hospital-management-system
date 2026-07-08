from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.shift_service import *
from app.services.auth_service import is_logged_in
from app.routes.staff_management_routes import chief_office_staff_required

shift_bp = Blueprint('shift', __name__, url_prefix='/shifts')

@shift_bp.route('/')
def index():
    """Shift management page"""
    if not chief_office_staff_required():
        return redirect('/auth/staff-login')
    
    return render_template('shift_management/index.html')

@shift_bp.route('/calendar')
def calendar():
    """Shift calendar view"""
    if not chief_office_staff_required():
        return redirect('/auth/staff-login')
    
    return render_template('shift_management/calendar.html')

# ==================== API ROUTES ====================

@shift_bp.route('/api/shifts', methods=['GET'])
def api_get_shifts():
    """Get all shifts"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    shifts = get_all_shifts_service(start_date, end_date)
    return jsonify({'success': True, 'data': shifts})

@shift_bp.route('/api/shifts/<int:shift_id>', methods=['GET'])
def api_get_shift(shift_id):
    """Get a specific shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        shift = get_shift_by_id_service(shift_id)
        employees = get_employees_on_shift_service(shift_id)
        available_employees = get_available_employees_for_shift_service(shift_id)
        
        return jsonify({
            'success': True,
            'data': {
                'shift': shift,
                'employees': employees,
                'available_employees': available_employees
            }
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@shift_bp.route('/api/shifts', methods=['POST'])
def api_create_shift():
    """Create a new shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        shift_id = create_shift_service(data)
        return jsonify({
            'success': True,
            'message': 'Shift created successfully',
            'id': shift_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@shift_bp.route('/api/shifts/<int:shift_id>', methods=['PUT'])
def api_update_shift(shift_id):
    """Update a shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = update_shift_service(shift_id, data)
        return jsonify({
            'success': True,
            'message': 'Shift updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@shift_bp.route('/api/shifts/<int:shift_id>', methods=['DELETE'])
def api_delete_shift(shift_id):
    """Delete a shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = delete_shift_service(shift_id)
        return jsonify({
            'success': True,
            'message': 'Shift deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@shift_bp.route('/api/shifts/<int:shift_id>/assign', methods=['POST'])
def api_assign_employee(shift_id):
    """Assign an employee to a shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        
        if not employee_id:
            return jsonify({'success': False, 'error': 'Employee ID is required'}), 400
        
        result = assign_employee_to_shift_service(employee_id, shift_id)
        if not result:
            return jsonify({'success': False, 'error': 'Employee already assigned to this shift'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Employee assigned to shift successfully'
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@shift_bp.route('/api/shifts/<int:shift_id>/remove', methods=['POST'])
def api_remove_employee(shift_id):
    """Remove an employee from a shift"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        employee_id = data.get('employee_id')
        
        if not employee_id:
            return jsonify({'success': False, 'error': 'Employee ID is required'}), 400
        
        result = remove_employee_from_shift_service(employee_id, shift_id)
        if not result:
            return jsonify({'success': False, 'error': 'Employee not assigned to this shift'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Employee removed from shift successfully'
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@shift_bp.route('/api/employees', methods=['GET'])
def api_get_employees():
    """Get all employees for assignment"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    employees = get_all_employees_service()
    return jsonify({'success': True, 'data': employees})

@shift_bp.route('/api/stats', methods=['GET'])
def api_get_stats():
    """Get shift statistics"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    stats = get_shift_statistics_service()
    return jsonify({'success': True, 'data': stats})

@shift_bp.route('/api/range', methods=['GET'])
def api_get_shifts_by_range():
    """Get shifts within a date range"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400
    
    shifts = get_shifts_by_date_range_service(start_date, end_date)
    return jsonify({'success': True, 'data': shifts})

@shift_bp.route('/api/employee/<int:employee_id>/shifts', methods=['GET'])
def api_get_employee_shifts(employee_id):
    """Get shifts for a specific employee"""
    if not chief_office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    shifts = get_employee_shifts_service(employee_id, start_date, end_date)
    return jsonify({'success': True, 'data': shifts})