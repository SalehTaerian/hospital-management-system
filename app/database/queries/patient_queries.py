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

def get_patient_admissions(patient_id):
    query = """
        SELECT 
            a.admID,
            a.cost,
            a.mID,
            a.doctorID,
            e.firstName || ' ' || e.lastName as doctor_name,
            doc.visitCost,
            b.bedID,
            b.cost as bed_cost,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.name as room_name,
            dep.name as department_name
        FROM admission a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN doctor doc ON a.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN bedInfo bi ON a.admID = bi.asgAdmID
        LEFT JOIN bed b ON bi.bedID = b.bedID
        LEFT JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE mr.pID = %s
        ORDER BY a.admID DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_admission_by_id(admID, patient_id):
    query = """
        SELECT 
            a.admID,
            a.cost,
            a.mID,
            a.doctorID,
            e.firstName || ' ' || e.lastName as doctor_name,
            doc.visitCost,
            b.bedID,
            b.cost as bed_cost,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.name as room_name,
            dep.name as department_name
        FROM admission a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN doctor doc ON a.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN bedInfo bi ON a.admID = bi.asgAdmID
        LEFT JOIN bed b ON bi.bedID = b.bedID
        LEFT JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE a.admID = %s AND mr.pID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (admID, patient_id),
        fetch_one=True,
        fetch_dict=True
    )
    
def get_patient_insurance(patient_id):
    query = """
        SELECT 
            insuranceID,
            name,
            coveragePercentage,
            policyNumber,
            startDate,
            endDate,
            createdAt
        FROM insurance
        WHERE pID = %s
        ORDER BY createdAt DESC
        LIMIT 1
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )

def get_insurance_by_id(insurance_id, patient_id):
    query = """
        SELECT 
            insuranceID,
            name,
            coveragePercentage,
            policyNumber,
            startDate,
            endDate,
            createdAt
        FROM insurance
        WHERE insuranceID = %s AND pID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (insurance_id, patient_id),
        fetch_one=True,
        fetch_dict=True
    )

def check_insurance_exists(patient_id):
    query = "SELECT insuranceID FROM insurance WHERE pID = %s"
    result = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )
    return result is not None

def create_insurance(data):
    query = """
        INSERT INTO insurance (
            pID, name, coveragePercentage, policyNumber, startDate, endDate
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
        RETURNING insuranceID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('pID'),
            data.get('name'),
            data.get('coveragePercentage'),
            data.get('policyNumber'),
            data.get('startDate'),
            data.get('endDate')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_insurance(insurance_id, data):
    query = """
        UPDATE insurance
        SET 
            name = %s,
            coveragePercentage = %s,
            policyNumber = %s,
            startDate = %s,
            endDate = %s
        WHERE insuranceID = %s AND pID = %s
        RETURNING insuranceID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('coveragePercentage'),
            data.get('policyNumber'),
            data.get('startDate'),
            data.get('endDate'),
            insurance_id,
            data.get('pID')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_insurance(insurance_id, patient_id):
    query = "DELETE FROM insurance WHERE insuranceID = %s AND pID = %s RETURNING insuranceID"
    result = DatabaseConnection.execute_query(
        query,
        (insurance_id, patient_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None