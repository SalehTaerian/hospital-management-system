from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.room_service import *
from app.services.auth_service import get_departments_service, is_logged_in

room_bp = Blueprint('room', __name__, url_prefix='/rooms')

def office_staff_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'officeStaff'

@room_bp.route('/')
def index():
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('room_management/index.html')

@room_bp.route('/api/rooms', methods=['GET'])
def api_get_rooms():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    rooms = get_all_rooms_service()
    return jsonify({'success': True, 'data': rooms})

@room_bp.route('/api/rooms/<int:room_id>', methods=['GET'])
def api_get_room(room_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        room = get_room_by_id_service(room_id)
        return jsonify({'success': True, 'data': room})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@room_bp.route('/api/rooms', methods=['POST'])
def api_create_room():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        room_id = create_room_service(data)
        return jsonify({
            'success': True,
            'message': 'Room created successfully',
            'id': room_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@room_bp.route('/api/rooms/<int:room_id>', methods=['PUT'])
def api_update_room(room_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        result = update_room_service(room_id, data)
        return jsonify({
            'success': True,
            'message': 'Room updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@room_bp.route('/api/rooms/<int:room_id>', methods=['DELETE'])
def api_delete_room(room_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = delete_room_service(room_id)
        return jsonify({
            'success': True,
            'message': 'Room deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@room_bp.route('/api/departments', methods=['GET'])
def api_get_departments():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    departments = get_departments_service()
    return jsonify({'success': True, 'data': departments})