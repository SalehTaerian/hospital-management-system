from app.database.queries.room_queries import *

def get_all_rooms_service():
    return get_all_rooms()

def get_room_by_id_service(room_id):
    room = get_room_by_id(room_id)
    if not room:
        raise ValueError(f"Room with ID {room_id} not found")
    return room

def create_room_service(data):
    if not data.get('name'):
        raise ValueError("Room name is required")
    if not data.get('departID'):
        raise ValueError("Department is required")
    
    return create_room(data)

def update_room_service(room_id, data):
    existing = get_room_by_id(room_id)
    if not existing:
        raise ValueError(f"Room with ID {room_id} not found")
    
    if not data.get('name'):
        raise ValueError("Room name is required")
    if not data.get('departID'):
        raise ValueError("Department is required")
    
    return update_room(room_id, data)

def delete_room_service(room_id):
    existing = get_room_by_id(room_id)
    if not existing:
        raise ValueError(f"Room with ID {room_id} not found")
    
    return delete_room(room_id)

def get_rooms_by_department_service(departID):
    return get_rooms_by_department(departID)