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

def get_doctor_appointments(doctor_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            a.createdAt,
            a.followID,
            p.pID as patient_id,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            p.phoneNumber,
            mr.mID,
            mr.bloodType,
            mr.smokingHistory
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        WHERE a.doctorID = %s
        ORDER BY a.date DESC, a.time DESC
    """
    results = DatabaseConnection.execute_query(
        query,
        (doctor_id,),
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
        if 'followid' not in row:
            row['followid'] = None
    
    return results

def get_appointment_by_id(appointment_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            a.isOnlineReserved,
            a.mID,
            a.doctorID,
            a.staffID,
            p.pID as patient_id,
            p.firstName,
            p.lastName,
            p.nationalCode,
            p.phoneNumber
        FROM appointment a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        WHERE a.appoID = %s
    """
    result = DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_one=True,
        fetch_dict=True
    )
    
    if result:
        if 'time' in result and result['time']:
            result['time'] = str(result['time'])
        if 'date' in result and result['date']:
            result['date'] = str(result['date'])
    
    return result

def get_appointment_diseases(appointment_id):
    query = """
        SELECT 
            dd.disDiagID,
            dd.appoID,
            dd.icdID,
            icd.code,
            icd.diseaseName,
            dd.description
        FROM diseaseDiag dd
        JOIN icdCode icd ON dd.icdID = icd.icdID
        WHERE dd.appoID = %s
        ORDER BY dd.disDiagID
    """
    return DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_disease_by_id(dis_diag_id):
    query = """
        SELECT 
            dd.disDiagID,
            dd.appoID,
            dd.icdID,
            icd.code,
            icd.diseaseName,
            dd.description
        FROM diseaseDiag dd
        JOIN icdCode icd ON dd.icdID = icd.icdID
        WHERE dd.disDiagID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (dis_diag_id,),
        fetch_one=True,
        fetch_dict=True
    )

def get_disease_medicines(dis_diag_id):
    query = """
        SELECT 
            md.medDiagID,
            md.disDiagID,
            md.icdmID,
            icdm.medicineName,
            md.description
        FROM medicineDiag md
        JOIN icdmCode icdm ON md.icdmID = icdm.icdmID
        WHERE md.disDiagID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (dis_diag_id,),
        fetch_all=True,
        fetch_dict=True
    )

def add_disease_diagnosis(data):
    query = """
        INSERT INTO diseaseDiag (appoID, icdID, description)
        VALUES (%s, %s, %s)
        RETURNING disDiagID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('appoID'),
            data.get('icdID'),
            data.get('description')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_disease_diagnosis(dis_diag_id, data):
    query = """
        UPDATE diseaseDiag
        SET icdID = %s, description = %s
        WHERE disDiagID = %s
        RETURNING disDiagID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('icdID'),
            data.get('description'),
            dis_diag_id
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_disease_diagnosis(dis_diag_id):
    query = "DELETE FROM diseaseDiag WHERE disDiagID = %s RETURNING disDiagID"
    result = DatabaseConnection.execute_query(
        query,
        (dis_diag_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def add_medicine_to_disease(data):
    query = """
        INSERT INTO medicineDiag (disDiagID, icdmID, description)
        VALUES (%s, %s, %s)
        RETURNING medDiagID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('disDiagID'),
            data.get('icdmID'),
            data.get('description')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_medicine_from_disease(med_diag_id):
    query = "DELETE FROM medicineDiag WHERE medDiagID = %s RETURNING medDiagID"
    result = DatabaseConnection.execute_query(
        query,
        (med_diag_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def add_disease_history(data):
    query = """
        INSERT INTO diseaseRecord (mID, icdID, description)
        VALUES (%s, %s, %s)
        RETURNING diseaseID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('icdID'),
            data.get('description')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def add_medicine_history(data):
    query = """
        INSERT INTO medicineRecord (mID, icdmID, description)
        VALUES (%s, %s, %s)
        RETURNING medicineID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('icdmID'),
            data.get('description')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def add_drug_history(data):
    query = """
        INSERT INTO drugRecord (mID, description)
        VALUES (%s, %s)
        RETURNING drugID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('mID'),
            data.get('description')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def add_vital_sign(data):
    query = """
        INSERT INTO vitalSign (appoID, parameterID, parameterValue)
        VALUES (%s, %s, %s)
        RETURNING vitalID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('appoID'),
            data.get('parameterID'),
            data.get('parameterValue')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_appointment_vitals(appointment_id):
    query = """
        SELECT 
            vs.vitalID,
            vs.parameterValue,
            p.parameterName,
            p.min,
            p.max,
            p.average
        FROM vitalSign vs
        JOIN parameterList p ON vs.parameterID = p.parameterID
        WHERE vs.appoID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_icd_codes():
    query = """
        SELECT 
            icdID as id,
            code,
            diseaseName as name
        FROM icdCode
        ORDER BY code
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_icdm_codes():
    query = """
        SELECT 
            icdmID as id,
            medicineName as name
        FROM icdmCode
        ORDER BY medicineName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_parameter_list():
    query = """
        SELECT 
            parameterID as id,
            parameterName as name,
            min,
            max,
            average
        FROM parameterList
        ORDER BY parameterName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_disease_history(patient_id):
    query = """
        SELECT 
            dr.diseaseID,
            icd.code,
            icd.diseaseName,
            dr.description
        FROM diseaseRecord dr
        JOIN icdCode icd ON dr.icdID = icd.icdID
        JOIN medicalRecord mr ON dr.mID = mr.mID
        WHERE mr.pID = %s
        ORDER BY dr.diseaseID DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_medicine_history(patient_id):
    query = """
        SELECT 
            mr.medicineID,
            icdm.medicineName,
            mr.description
        FROM medicineRecord mr
        JOIN icdmCode icdm ON mr.icdmID = icdm.icdmID
        JOIN medicalRecord m ON mr.mID = m.mID
        WHERE m.pID = %s
        ORDER BY mr.medicineID DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
def get_medicine_allergy(appointment_id):
    query = """
        SELECT 
            i.medicineName
        FROM medicalRecord m
        JOIN medicineAllergy ma ON ma.mID = m.mID
        JOIN icdmCode i ON i.icdmID = ma.icdmID
        WHERE m.mID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (appointment_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_drug_history(patient_id):
    query = """
        SELECT 
            dr.drugID,
            dr.description
        FROM drugRecord dr
        JOIN medicalRecord m ON dr.mID = m.mID
        WHERE m.pID = %s
        ORDER BY dr.drugID DESC
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
    results = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    for row in results:
        if 'createdat' in row and row['createdat']:
            row['createdat'] = str(row['createdat'])
    
    return results

def get_medicine_feedback(med_diag_id):
    query = """
        SELECT 
            feedBackID,
            medDiagID,
            effectPercentage
        FROM feedBack
        WHERE medDiagID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (med_diag_id,),
        fetch_one=True,
        fetch_dict=True
    )

def add_or_update_feedback(data):
    med_diag_id = data.get('medDiagID')
    effect = data.get('effectPercentage')
    
    check_query = "SELECT feedBackID FROM feedBack WHERE medDiagID = %s"
    existing = DatabaseConnection.execute_query(
        check_query,
        (med_diag_id,),
        fetch_one=True,
        fetch_dict=True
    )
    
    if existing:
        query = """
            UPDATE feedBack
            SET effectPercentage = %s
            WHERE medDiagID = %s
            RETURNING feedBackID
        """
        result = DatabaseConnection.execute_query(
            query,
            (effect, med_diag_id),
            fetch_one=True,
            commit=True
        )
    else:
        query = """
            INSERT INTO feedBack (medDiagID, effectPercentage)
            VALUES (%s, %s)
            RETURNING feedBackID
        """
        result = DatabaseConnection.execute_query(
            query,
            (med_diag_id, effect),
            fetch_one=True,
            commit=True
        )
    
    return result[0] if result else None

def delete_feedback(med_diag_id):
    query = "DELETE FROM feedBack WHERE medDiagID = %s RETURNING feedBackID"
    result = DatabaseConnection.execute_query(
        query,
        (med_diag_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_disease_medicines_with_feedback(dis_diag_id):
    query = """
        SELECT 
            md.medDiagID,
            md.disDiagID,
            md.icdmID,
            icdm.medicineName,
            md.description,
            fb.effectPercentage,
            fb.feedBackID
        FROM medicineDiag md
        JOIN icdmCode icdm ON md.icdmID = icdm.icdmID
        LEFT JOIN feedBack fb ON md.medDiagID = fb.medDiagID
        WHERE md.disDiagID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (dis_diag_id,),
        fetch_all=True,
        fetch_dict=True
    )
