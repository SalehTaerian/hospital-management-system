from app.database.connection import DatabaseConnection
from datetime import datetime

def create_followup(progress=0):
    query = """
        INSERT INTO followup (progress)
        VALUES (%s)
        RETURNING followID
    """
    result = DatabaseConnection.execute_query(
        query,
        (progress,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_followup_by_id(follow_id):
    query = """
        SELECT 
            followID,
            progress
        FROM followup
        WHERE followID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (follow_id,),
        fetch_one=True,
        fetch_dict=True
    )

def update_followup_progress(follow_id, progress):
    query = """
        UPDATE followup
        SET progress = %s
        WHERE followID = %s
        RETURNING followID
    """
    result = DatabaseConnection.execute_query(
        query,
        (progress, follow_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_appointments_with_followup(patient_id=None):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            a.createdAt,
            f.followID,
            f.progress,
            p.firstName || ' ' || p.lastName as patient_name,
            p.pID as patient_id,
            e.firstName || ' ' || e.lastName as doctor_name,
            CASE 
                WHEN a.followID IN (
                    SELECT followID FROM appointment WHERE followID = a.followID AND appoID != a.appoID
                ) THEN TRUE
                ELSE FALSE
            END as is_followup,
            CASE 
                WHEN a.followID IN (
                    SELECT followID FROM appointment WHERE followID = a.followID AND appoID != a.appoID
                ) THEN (
                    SELECT appoID FROM appointment 
                    WHERE followID = a.followID AND appoID != a.appoID 
                    ORDER BY createdAt DESC LIMIT 1
                )
                ELSE NULL
            END as followup_from
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor d ON a.doctorID = d.employeeID
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN followup f ON a.followID = f.followID
    """
    params = []
    
    if patient_id:
        query += " WHERE mr.pID = %s"
        params.append(patient_id)
    
    query += " ORDER BY a.date DESC, a.time DESC"
    
    return DatabaseConnection.execute_query(
        query,
        tuple(params) if params else None,
        fetch_all=True,
        fetch_dict=True
    )

def get_followup_chain(follow_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            p.firstName || ' ' || p.lastName as patient_name,
            e.firstName || ' ' || e.lastName as doctor_name,
            f.progress
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor d ON a.doctorID = d.employeeID
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN followup f ON a.followID = f.followID
        WHERE a.followID = %s
        ORDER BY a.date ASC, a.time ASC
    """
    return DatabaseConnection.execute_query(
        query,
        (follow_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_available_appointments_for_followup(patient_id, current_appointment_id=None):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            p.firstName || ' ' || p.lastName as patient_name,
            e.firstName || ' ' || e.lastName as doctor_name,
            f.followID,
            f.progress
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor d ON a.doctorID = d.employeeID
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN followup f ON a.followID = f.followID
        WHERE mr.pID = %s
        AND a.status NOT IN ('Cancelled', 'Completed')
        AND a.followID NOT IN (
            SELECT followID FROM appointment WHERE followID = a.followID AND appoID != a.appoID
        )
    """
    params = [patient_id]
    
    if current_appointment_id:
        query += " AND a.appoID != %s"
        params.append(current_appointment_id)
    
    query += " ORDER BY a.date DESC, a.time DESC"
    
    return DatabaseConnection.execute_query(
        query,
        tuple(params),
        fetch_all=True,
        fetch_dict=True
    )

def create_appointment_with_followup(data):
    follow_id = data.get('followID')
    
    if not follow_id:
        follow_id = create_followup(0)
        if not follow_id:
            raise ValueError("Failed to create followup record")
    
    query = """
        INSERT INTO appointment (
            mID, doctorID, staffID, followID, date, time, status, isOnlineReserved
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING appoID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('doctorID'),
            data.get('staffID'),
            follow_id,
            data.get('date'),
            data.get('time'),
            data.get('status', 'Scheduled'),
            data.get('isOnlineReserved', False)
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_appointment_followup(appointment_id, follow_id):
    query = """
        UPDATE appointment
        SET followID = %s
        WHERE appoID = %s
        RETURNING appoID
    """
    result = DatabaseConnection.execute_query(
        query,
        (follow_id, appointment_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_appointment_by_id_with_followup(appointment_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            a.createdAt,
            a.mID,
            a.doctorID,
            a.staffID,
            a.followID,
            f.progress,
            p.pID as patient_id,
            p.firstName,
            p.lastName,
            p.nationalCode,
            p.phoneNumber
        FROM appointment a
        JOIN followup f ON a.followID = f.followID
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        WHERE a.appoID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_one=True,
        fetch_dict=True
    )