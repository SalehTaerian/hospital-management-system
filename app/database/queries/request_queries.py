from app.database.connection import DatabaseConnection
from datetime import datetime

def get_patient_requests(patient_id):
    query = """
        SELECT 
            r.reqID,
            r.name,
            r.description,
            r.status,
            r.isPatientConfirmed,
            r.cost,
            r.medID,
            r.testID,
            r.departID,
            e.firstName || ' ' || e.lastName AS doctor_name,
            dep.name AS department_name,
            icdm.medicineName,
            icdt.testName,
            CASE 
                WHEN r.medID IS NOT NULL THEN 'Medicine'
                WHEN r.testID IS NOT NULL THEN 'Test'
                ELSE 'Other'
            END as request_type
        FROM request r
        JOIN doctor doc ON r.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN department dep ON r.departID = dep.departID
        LEFT JOIN icdmCode icdm ON r.medID = icdm.icdmID
        LEFT JOIN icdtCode icdt ON r.testID = icdt.icdtID
        JOIN medicalRecord mr ON r.mID = mr.mID
        WHERE mr.pID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_pending_requests(patient_id):
    query = """
        SELECT 
            r.reqID,
            r.name,
            r.description,
            r.status,
            r.isPatientConfirmed,
            r.cost,
            r.medID,
            r.testID,
            r.departID,
            e.firstName || ' ' || e.lastName AS doctor_name,
            dep.name AS department_name,
            icdm.medicineName,
            icdt.testName,
            CASE 
                WHEN r.medID IS NOT NULL THEN 'Medicine'
                WHEN r.testID IS NOT NULL THEN 'Test'
                ELSE 'Other'
            END as request_type
        FROM request r
        JOIN doctor doc ON r.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN department dep ON r.departID = dep.departID
        LEFT JOIN icdmCode icdm ON r.medID = icdm.icdmID
        LEFT JOIN icdtCode icdt ON r.testID = icdt.icdtID
        JOIN medicalRecord mr ON r.mID = mr.mID
        WHERE mr.pID = %s
        AND r.isPatientConfirmed = FALSE
        AND r.status != 'Cancelled'
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_doctor_requests(doctor_id):
    query = """
        SELECT 
            r.reqID,
            r.name,
            r.description,
            r.status,
            r.isPatientConfirmed,
            r.cost,
            r.medID,
            r.testID,
            r.departID,
            dep.name AS department_name,
            p.firstName || ' ' || p.lastName AS patient_name,
            p.nationalCode,
            icdm.medicineName,
            icdt.testName,
            CASE 
                WHEN r.medID IS NOT NULL THEN 'Medicine'
                WHEN r.testID IS NOT NULL THEN 'Test'
                ELSE 'Other'
            END as request_type
        FROM request r
        JOIN medicalRecord mr ON r.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        LEFT JOIN department dep ON r.departID = dep.departID
        LEFT JOIN icdmCode icdm ON r.medID = icdm.icdmID
        LEFT JOIN icdtCode icdt ON r.testID = icdt.icdtID
        WHERE r.doctorID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (doctor_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_request_by_id(req_id):
    query = """
        SELECT 
            r.reqID,
            r.name,
            r.description,
            r.status,
            r.isPatientConfirmed,
            r.cost,
            r.mID,
            r.doctorID,
            r.medID,
            r.testID,
            r.departID
        FROM request r
        WHERE r.reqID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (req_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_medicine_request(data):
    query = """
        INSERT INTO request (
            mID, doctorID, departID, medID, name, description, status, isPatientConfirmed, cost
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING reqID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('doctorID'),
            data.get('departID'),
            data.get('medID'),
            data.get('name'),
            data.get('description'),
            'Pending',
            False,
            data.get('cost', 0)
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def create_test_request(data):
    query = """
        INSERT INTO request (
            mID, doctorID, departID, testID, name, description, status, isPatientConfirmed, cost
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING reqID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('doctorID'),
            data.get('departID'),
            data.get('testID'),
            data.get('name'),
            data.get('description'),
            'Pending',
            False,
            data.get('cost', 0)
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def confirm_request(req_id):
    query = """
        UPDATE request
        SET isPatientConfirmed = TRUE,
            status = 'Confirmed'
        WHERE reqID = %s
        RETURNING reqID
    """
    result = DatabaseConnection.execute_query(
        query,
        (req_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def cancel_request(req_id):
    query = """
        UPDATE request
        SET status = 'Cancelled'
        WHERE reqID = %s
        RETURNING reqID
    """
    result = DatabaseConnection.execute_query(
        query,
        (req_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_patient_medical_record_id(patient_id):
    query = "SELECT mID FROM medicalRecord WHERE pID = %s"
    result = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )
    return result['mid'] if result else None

def get_medicines_list():
    query = """
        SELECT 
            icdmID as id,
            medicineName as name,
            icdID
        FROM icdmCode
        ORDER BY medicineName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_tests_list():
    query = """
        SELECT 
            icdtID as id,
            testName as name,
            cost
        FROM icdtCode
        ORDER BY testName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_departments_list():
    query = """
        SELECT 
            departID as id,
            name
        FROM department
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )
    
    
def medicine_conflict(medId):
    query = """
        SELECT i.medicineName
        FROM medicineConflict m JOIN icdmCode i ON  m.icdm2ID = i.icdmID
        WHERE icdm1ID = %s
    """
    results = DatabaseConnection.execute_query(query,(medId,) , fetch_all=True, fetch_dict=True)
    return results