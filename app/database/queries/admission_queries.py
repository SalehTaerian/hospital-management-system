from app.database.connection import DatabaseConnection
from datetime import datetime

def get_all_admissions():
    query = """
        SELECT 
            a.admID,
            a.cost,
            p.pID as patient_id,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            e.firstName || ' ' || e.lastName as doctor_name,
            b.bedID,
            b.cost as bed_cost,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.name as room_name,
            dep.name as department_name
        FROM admission a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor doc ON a.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN bedInfo bi ON a.admID = bi.asgAdmID AND bi.status = 'Occupied'
        LEFT JOIN bed b ON bi.bedID = b.bedID
        LEFT JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        ORDER BY b.bedID DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_admission_by_id(admID):
    query = """
        SELECT 
            a.admID,
            a.cost,
            a.mID,
            a.doctorID,
            a.officeStaffID,
            p.pID as patient_id,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            e.firstName || ' ' || e.lastName as doctor_name,
            b.bedID,
            b.cost as bed_cost,
            bi.biID as bed_info_id,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.roomID,
            r.name as room_name,
            dep.departID,
            dep.name as department_name
        FROM admission a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor doc ON a.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN bedInfo bi ON a.admID = bi.asgAdmID AND bi.status = 'Occupied'
        LEFT JOIN bed b ON bi.bedID = b.bedID
        LEFT JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE a.admID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        fetch_dict=True
    )

def get_patient_by_id(patient_id):
    query = """
        SELECT 
            pID,
            firstName,
            lastName,
            nationalCode
        FROM patient
        WHERE pID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )

def get_medical_record_by_patient(patient_id):
    query = "SELECT mID FROM medicalRecord WHERE pID = %s"
    result = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )
    return result['mid'] if result else None

def create_admission(data):
    query = """
        INSERT INTO admission (mID, doctorID, officeStaffID, cost)
        VALUES (%s, %s, %s, %s)
        RETURNING admID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('doctorID'),
            data.get('officeStaffID'),
            data.get('cost', 0)
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def assign_bed_to_admission(admID, bedID, roomID):
    query = """
        INSERT INTO bedInfo (bedID, roomID, asgAdmID, startTimestamp, status)
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP, 'Occupied')
        RETURNING biID
    """
    result = DatabaseConnection.execute_query(
        query,
        (bedID, roomID, admID),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_admission_cost(admID, cost):
    query = """
        UPDATE admission
        SET cost = %s
        WHERE admID = %s
        RETURNING admID
    """
    result = DatabaseConnection.execute_query(
        query,
        (cost, admID),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_admission(admID):
    query = "DELETE FROM admission WHERE admID = %s RETURNING admID"
    result = DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def discharge_patient(admID):
    query = """
        UPDATE bedInfo
        SET status = 'Available'
        WHERE asgAdmID = %s AND status = 'Occupied'
        RETURNING biID
    """
    result = DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_available_beds():
    query = """
        SELECT 
            b.bedID,
            b.cost,
            r.roomID,
            r.name as room_name,
            dep.departID,
            dep.name as department_name
        FROM bed b
        CROSS JOIN room r
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE b.bedID NOT IN (
            SELECT bedID FROM bedInfo WHERE status = 'Occupied'
        )
        AND NOT EXISTS (
            SELECT 1 FROM bedInfo bi2 
            WHERE bi2.bedID = b.bedID AND bi2.status = 'Occupied'
        )
        ORDER BY r.name, b.bedID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_available_beds_by_room(roomID):
    query = """
        SELECT 
            b.bedID,
            b.cost
        FROM bed b
        WHERE b.bedID NOT IN (
            SELECT bedID FROM bedInfo WHERE status = 'Occupied' AND roomID = %s
        )
        AND NOT EXISTS (
            SELECT 1 FROM bedInfo bi2 
            WHERE bi2.bedID = b.bedID AND bi2.status = 'Occupied'
        )
        ORDER BY b.bedID
    """
    return DatabaseConnection.execute_query(
        query,
        (roomID,),
        fetch_all=True,
        fetch_dict=True
    )

def get_all_doctors():
    query = """
        SELECT 
            e.employeeID as id,
            e.firstName || ' ' || e.lastName as name,
            d.specialization
        FROM doctor d
        JOIN employee e ON d.employeeID = e.employeeID
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_all_rooms():
    query = """
        SELECT 
            roomID as id,
            name,
            description,
            departID
        FROM room
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_beds_by_room(roomID):
    query = """
        SELECT 
            b.bedID,
            b.cost
        FROM bed b
        WHERE b.bedID NOT IN (
            SELECT bedID FROM bedInfo WHERE status = 'Occupied' AND roomID = %s
        )
        AND NOT EXISTS (
            SELECT 1 FROM bedInfo bi2 
            WHERE bi2.bedID = b.bedID AND bi2.status = 'Occupied'
        )
        ORDER BY b.bedID
    """
    return DatabaseConnection.execute_query(
        query,
        (roomID,),
        fetch_all=True,
        fetch_dict=True
    )

def transfer_patient(admID, new_bedID, new_roomID, cost):
    query = """
        INSERT INTO transfer (admID, destBedID, cost)
        VALUES (%s, %s, %s)
        RETURNING transferID
    """
    result = DatabaseConnection.execute_query(
        query,
        (admID, new_bedID, cost),
        fetch_one=True,
        commit=True
    )
    
    if result:
        update_bed_info = """
            UPDATE bedInfo
            SET status = 'Available'
            WHERE asgAdmID = %s AND status = 'Occupied'
        """
        DatabaseConnection.execute_query(
            update_bed_info,
            (admID,),
            commit=True
        )
        
        assign_bed = """
            INSERT INTO bedInfo (bedID, roomID, asgAdmID, startTimestamp, status)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, 'Occupied')
        """
        DatabaseConnection.execute_query(
            assign_bed,
            (new_bedID, new_roomID, admID),
            commit=True
        )
        
        return result[0]
    return None

def get_transfer_history(admID):
    query = """
        SELECT 
            t.transferID,
            t.transferedAt,
            t.cost,
            b.bedID as from_bed,
            b2.bedID as to_bed,
            r.name as from_room
        FROM transfer t
        JOIN bedInfo bi ON t.admID = bi.asgAdmID
        JOIN bed b ON bi.bedID = b.bedID
        JOIN room r ON bi.roomID = r.roomID
        JOIN bed b2 ON t.destBedID = b2.bedID
        WHERE t.admID = %s
        ORDER BY t.transferedAt DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_all=True,
        fetch_dict=True
    )