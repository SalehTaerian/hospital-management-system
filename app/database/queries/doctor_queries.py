from app.database.connection import DatabaseConnection
from datetime import datetime, timedelta

def get_doctor_patients(doctor_id):
    query = """
        SELECT 
            p.pID,
            p.firstName,
            p.lastName,
            p.nationalCode,
            p.gender,
            p.dateOfBirth,
            EXTRACT(YEAR FROM age(CURRENT_DATE, p.dateOfBirth)) as age,
            p.phoneNumber,
            a.admID,
            a.cost,
            bi.bedID,
            bi.status as bed_status,
            r.name as room_name,
            r.roomID,
            dep.name as department_name,
            dep.departID,
            m.bloodType,
            m.smokingHistory,
            b.cost as bed_cost
        FROM admission a
        JOIN medicalRecord m ON a.mID = m.mID
        JOIN patient p ON m.pID = p.pID
        JOIN bedInfo bi ON a.admID = bi.asgAdmID AND bi.status = 'Occupied'
        JOIN bed b ON bi.bedID = b.bedID
        JOIN room r ON bi.roomID = r.roomID
        JOIN department dep ON r.departID = dep.departID
        WHERE a.doctorID = %s
        ORDER BY p.lastName, p.firstName
    """
    return DatabaseConnection.execute_query(
        query,
        (doctor_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_logs(patient_id):
    query = """
        SELECT 
            l.logID,
            l.parameterValue,
            l.createdAt,
            p.parameterName,
            p.min,
            p.max,
            p.average,
            e.name as equipment_name,
            e.MACAddress,
            CASE 
                WHEN l.parameterValue < p.min THEN 'Low'
                WHEN l.parameterValue > p.max THEN 'High'
                ELSE 'Normal'
            END as status,
            CASE 
                WHEN l.parameterValue < p.min THEN 'danger'
                WHEN l.parameterValue > p.max THEN 'danger'
                ELSE 'success'
            END as status_color
        FROM log l
        JOIN parameterList p ON l.parameterID = p.parameterID
        JOIN equipment e ON l.equipID = e.equipID
        JOIN admission a ON l.asgAdmID = a.admID
        JOIN medicalRecord mr ON a.mID = mr.mID
        WHERE mr.pID = %s
        ORDER BY l.createdAt DESC
        LIMIT 100
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_warnings(patient_id):
    query = """
        SELECT 
            w.warnID,
            l.logID,
            l.parameterValue,
            l.createdAt,
            p.parameterName,
            p.min,
            p.max,
            p.average,
            e.name as equipment_name,
            w.checkedStatus,
            w.checkedTime,
            CASE 
                WHEN l.parameterValue < p.min THEN 'Low'
                WHEN l.parameterValue > p.max THEN 'High'
                ELSE 'Normal'
            END as status
        FROM log l
        JOIN parameterList p ON l.parameterID = p.parameterID
        JOIN equipment e ON l.equipID = e.equipID
        JOIN admission a ON l.asgAdmID = a.admID
        JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN warning w ON l.logID = w.logID
        WHERE mr.pID = %s
        AND (l.parameterValue < p.min OR l.parameterValue > p.max)
        ORDER BY l.createdAt DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_all_active_warnings():
    query = """
        SELECT 
            w.warnID,
            l.logID,
            l.parameterValue,
            l.createdAt,
            mr.pID as patient_id,
            pat.firstName,
            pat.lastName,
            pat.phoneNumber,
            p.parameterName,
            p.min,
            p.max,
            p.average,
            e.name as equipment_name,
            w.checkedStatus,
            w.checkedTime,
            CASE 
                WHEN l.parameterValue < p.min THEN 'Low'
                WHEN l.parameterValue > p.max THEN 'High'
                ELSE 'Normal'
            END as status
        FROM log l
        JOIN parameterList p ON l.parameterID = p.parameterID
        JOIN equipment e ON l.equipID = e.equipID
        JOIN admission a ON l.asgAdmID = a.admID
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient pat ON mr.pID = pat.pID
        LEFT JOIN warning w ON l.logID = w.logID
        WHERE (l.parameterValue < p.min OR l.parameterValue > p.max)
        AND (w.checkedStatus IS NULL OR w.checkedStatus = 'Unchecked')
        ORDER BY l.createdAt DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_latest_logs_for_patients(patient_ids):
    if not patient_ids:
        return []
    
    placeholders = ','.join(['%s'] * len(patient_ids))
    query = f"""
        SELECT DISTINCT ON (mr.pID)
            mr.pID as patient_id,
            l.logID,
            l.parameterValue,
            l.createdAt,
            p.parameterName,
            p.min,
            p.max,
            p.average,
            e.name as equipment_name,
            CASE 
                WHEN l.parameterValue < p.min THEN 'Low'
                WHEN l.parameterValue > p.max THEN 'High'
                ELSE 'Normal'
            END as status
        FROM log l
        JOIN parameterList p ON l.parameterID = p.parameterID
        JOIN equipment e ON l.equipID = e.equipID
        JOIN admission a ON l.asgAdmID = a.admID
        JOIN medicalRecord mr ON a.mID = mr.mID
        WHERE mr.pID IN ({placeholders})
        ORDER BY mr.pID, l.createdAt DESC
    """
    return DatabaseConnection.execute_query(
        query,
        tuple(patient_ids),
        fetch_all=True,
        fetch_dict=True
    )

def get_all_active_warnings():
    query = """
        SELECT 
            l.logID,
            l.parameterValue,
            l.createdAt,
            mr.pID as patient_id,
            pa.firstName,
            pa.lastName,
            pa.phoneNumber,
            p.parameterName,
            p.min,
            p.max,
            p.average,
            e.name as equipment_name,
            CASE 
                WHEN l.parameterValue < p.min THEN 'Low'
                WHEN l.parameterValue > p.max THEN 'High'
                ELSE 'Normal'
            END as status
        FROM log l
        JOIN parameterList p ON l.parameterID = p.parameterID
        JOIN equipment e ON l.equipID = e.equipID
        JOIN admission a ON l.asgAdmID = a.admID
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient pa ON mr.pID = pa.pID
        WHERE (l.parameterValue < p.min OR l.parameterValue > p.max)
        AND l.createdAt >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
        ORDER BY l.createdAt DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )
    
def mark_warning_checked(warning_id):
    query = """
        UPDATE warning
        SET checkedStatus = 'Checked',
            checkedTime = CURRENT_TIMESTAMP
        WHERE warnID = %s
        RETURNING warnID
    """
    result = DatabaseConnection.execute_query(
        query,
        (warning_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def mark_warnings_checked_for_patient(patient_id):
    query = """
        UPDATE warning
        SET checkedStatus = 'Checked',
            checkedTime = CURRENT_TIMESTAMP
        WHERE logID IN (
            SELECT l.logID
            FROM log l
            JOIN admission a ON l.asgAdmID = a.admID
            JOIN medicalRecord mr ON a.mID = mr.mID
            WHERE mr.pID = %s
        )
        AND checkedStatus = 'Unchecked'
        RETURNING warnID
    """
    results = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        commit=True
    )
    return [row['warnid'] for row in results] if results else []