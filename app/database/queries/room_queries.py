from app.database.connection import DatabaseConnection

def get_all_rooms():
    query = """
        SELECT 
            r.roomID,
            r.name,
            r.description,
            r.departID,
            d.name as department_name
        FROM room r
        LEFT JOIN department d ON r.departID = d.departID
        ORDER BY r.name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_room_by_id(room_id):
    query = """
        SELECT 
            r.roomID,
            r.name,
            r.description,
            r.departID,
            d.name as department_name
        FROM room r
        LEFT JOIN department d ON r.departID = d.departID
        WHERE r.roomID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (room_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_room(data):
    query = """
        INSERT INTO room (name, description, departID)
        VALUES (%s, %s, %s)
        RETURNING roomID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('description'),
            data.get('departID')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_room(room_id, data):
    query = """
        UPDATE room
        SET name = %s, description = %s, departID = %s
        WHERE roomID = %s
        RETURNING roomID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('description'),
            data.get('departID'),
            room_id
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_room(room_id):
    query = "DELETE FROM room WHERE roomID = %s RETURNING roomID"
    result = DatabaseConnection.execute_query(
        query,
        (room_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_rooms_by_department(departID):
    query = """
        SELECT 
            roomID,
            name,
            description
        FROM room
        WHERE departID = %s
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query,
        (departID,),
        fetch_all=True,
        fetch_dict=True
    )