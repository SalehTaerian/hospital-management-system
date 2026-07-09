from app.database.connection import DatabaseConnection
from datetime import datetime

def get_patient_upcoming_appointments(patient_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            a.createdAt,
            e.firstName || ' ' || e.lastName AS doctor_name,
            s.name,
            d.visitCost,
            i.invID,
            i.totalAmount,
            i.patientShare,
            i.insuranceShare,
            i.isPaid
        FROM appointment a
        JOIN doctor d ON a.doctorID = d.employeeID
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN doctorSpecialization ds ON d.employeeID = ds.docID JOIN specializationFields s 
        ON s.specID = ds.specID
        JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN invoice i ON a.appoID = i.appoID
        WHERE mr.pID = %s
        AND a.date >= CURRENT_DATE
        AND a.status NOT IN ('Cancelled', 'Completed')
        ORDER BY a.date ASC, a.time ASC
    """
    results = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    for row in results:
        if 'time' in row and row['time']:
            row['time'] = str(row['time'])
        if 'date' in row and row['date']:
            row['date'] = str(row['date'])
        if 'createdat' in row and row['createdat']:
            row['createdat'] = str(row['createdat'])
        if 'issuedate' in row and row['issuedate']:
            row['issuedate'] = str(row['issuedate'])
    
    return results

def get_patient_past_appointments(patient_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            e.firstName || ' ' || e.lastName AS doctor_name,
            s.name,
            d.visitCost,
            i.invID,
            i.totalAmount,
            i.patientShare,
            i.insuranceShare,
            i.isPaid
        FROM appointment a
        JOIN doctor d ON a.doctorID = d.employeeID
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN doctorSpecialization ds ON d.employeeID = ds.docID JOIN specializationFields s 
        ON s.specID = ds.specID
        JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN invoice i ON a.appoID = i.appoID
        WHERE mr.pID = %s
        AND (a.date < CURRENT_DATE OR a.status IN ('Completed', 'Cancelled'))
        ORDER BY a.date DESC, a.time DESC
    """
    results = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    for row in results:
        if 'time' in row and row['time']:
            row['time'] = str(row['time'])
        if 'date' in row and row['date']:
            row['date'] = str(row['date'])
    
    return results

def cancel_appointment(appointment_id, patient_id):
    check_query = """
        SELECT a.appoID 
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        WHERE a.appoID = %s AND mr.pID = %s AND a.status NOT IN ('Completed', 'Cancelled')
    """
    result = DatabaseConnection.execute_query(
        check_query,
        (appointment_id, patient_id),
        fetch_one=True
    )
    
    if not result:
        return None
    
    query = """
        UPDATE appointment
        SET status = 'Cancelled'
        WHERE appoID = %s
        RETURNING appoID
    """
    result = DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_patient_billing(patient_id):
    query = """
        SELECT 
            i.invID,
            i.issueDate,
            i.totalAmount,
            i.patientShare,
            i.insuranceShare,
            i.isPaid,
            a.date AS appointment_date,
            a.time AS appointment_time,
            e.firstName || ' ' || e.lastName AS doctor_name,
            s.name
        FROM invoice i
        JOIN appointment a ON i.appoID = a.appoID
        JOIN doctor d ON a.doctorID = d.employeeID 
        JOIN employee e ON d.employeeID = e.employeeID
        JOIN doctorSpecialization ds ON d.employeeID = ds.docID JOIN specializationFields s 
        ON s.specID = ds.specID
        WHERE i.pID = %s
        ORDER BY i.issueDate DESC
    """
    results = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    for row in results:
        if 'appointment_time' in row and row['appointment_time']:
            row['appointment_time'] = str(row['appointment_time'])
        if 'appointment_date' in row and row['appointment_date']:
            row['appointment_date'] = str(row['appointment_date'])
        if 'issuedate' in row and row['issuedate']:
            row['issuedate'] = str(row['issuedate'])
    
    return results