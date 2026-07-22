from app.database.connection import DatabaseConnection
from datetime import datetime

def get_all_admissions():
    query = """
        SELECT 
            a.admID,
            a.cost,
            a.createdAt,
            a.endTime,
            p.pID as patient_id,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            e.firstName || ' ' || e.lastName as doctor_name,
            doc.visitCost,
            b.bedID,
            b.cost as bed_cost,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.name as room_name,
            dep.name as department_name,
            EXTRACT(EPOCH FROM (COALESCE(bi.startTimestamp, CURRENT_TIMESTAMP) - a.createdAt)) / 60 as waiting_minutes
        FROM admission a
        JOIN medicalRecord mr ON a.mID = mr.mID
        JOIN patient p ON mr.pID = p.pID
        JOIN doctor doc ON a.doctorID = doc.employeeID
        JOIN employee e ON doc.employeeID = e.employeeID
        LEFT JOIN bedInfo bi ON a.admID = bi.asgAdmID AND bi.status = 'Occupied'
        LEFT JOIN bed b ON bi.bedID = b.bedID
        LEFT JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        ORDER BY a.admID DESC
    """
    results = DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )
    
    for row in results:
        if 'createdat' in row and row['createdat']:
            row['createdat'] = str(row['createdat'])
        if 'endtime' in row and row['endtime']:
            row['endtime'] = str(row['endtime'])
        if 'admission_date' in row and row['admission_date']:
            row['admission_date'] = str(row['admission_date'])
        if 'waiting_minutes' in row and row['waiting_minutes']:
            row['waiting_minutes'] = round(float(row['waiting_minutes']), 2)
    
    return results

def get_admission_by_id(admID):
    query = """
        SELECT 
            a.admID,
            a.cost,
            a.createdAt,
            a.endTime,
            a.mID,
            a.doctorID,
            a.officeStaffID,
            p.pID as patient_id,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            e.firstName || ' ' || e.lastName as doctor_name,
            doc.visitCost,
            b.bedID,
            b.cost as bed_cost,
            bi.biID as bed_info_id,
            bi.startTimestamp as admission_date,
            bi.status as bed_status,
            r.roomID,
            r.name as room_name,
            dep.departID,
            dep.name as department_name,
            EXTRACT(EPOCH FROM (COALESCE(bi.startTimestamp, CURRENT_TIMESTAMP) - a.createdAt)) / 60 as waiting_minutes
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
    result = DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        fetch_dict=True
    )
    
    if result:
        if 'createdat' in result and result['createdat']:
            result['createdat'] = str(result['createdat'])
        if 'endtime' in result and result['endtime']:
            result['endtime'] = str(result['endtime'])
        if 'admission_date' in result and result['admission_date']:
            result['admission_date'] = str(result['admission_date'])
        if 'waiting_minutes' in result and result['waiting_minutes']:
            result['waiting_minutes'] = round(float(result['waiting_minutes']), 2)
    
    return result

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
        WITH latest_bedinfo AS (
            SELECT DISTINCT ON (bedID) 
                bedID, 
                roomID, 
                status
            FROM bedInfo
            ORDER BY bedID, startTimestamp DESC
        )
        SELECT 
            b.bedID,
            b.cost,
            r.roomID,
            r.name as room_name,
            dep.departID,
            dep.name as department_name
        FROM bed b
        CROSS JOIN room r
        LEFT JOIN latest_bedinfo lbi ON b.bedID = lbi.bedID AND r.roomID = lbi.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE (lbi.status IS NULL OR lbi.status != 'Occupied')
        ORDER BY r.name, b.bedID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_available_beds_by_room(roomID):
    query = """
        WITH latest_bedinfo AS (
            SELECT DISTINCT ON (bedID) 
                bedID, 
                roomID, 
                status
            FROM bedInfo
            ORDER BY bedID, startTimestamp DESC
        )
        SELECT 
            b.bedID,
            b.cost
        FROM bed b
        LEFT JOIN latest_bedinfo lbi ON b.bedID = lbi.bedID AND lbi.roomID = %s
        WHERE (lbi.status IS NULL OR lbi.status != 'Occupied')
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
            doc.visitCost
        FROM doctor doc
        JOIN employee e ON doc.employeeID = e.employeeID
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
        WITH latest_bedinfo AS (
            SELECT DISTINCT ON (bedID) 
                bedID, 
                roomID, 
                status
            FROM bedInfo
            ORDER BY bedID, startTimestamp DESC
        )
        SELECT 
            b.bedID,
            b.cost,
            COALESCE(lbi.status, 'Available') as status
        FROM bed b
        LEFT JOIN latest_bedinfo lbi ON b.bedID = lbi.bedID AND lbi.roomID = %s
        ORDER BY b.bedID
    """
    return DatabaseConnection.execute_query(
        query,
        (roomID,),
        fetch_all=True,
        fetch_dict=True
    )

def transfer_patient(admID, new_bedID, new_roomID, cost):
    current_bed = """
        SELECT biID, bedID, roomID 
        FROM bedInfo 
        WHERE asgAdmID = %s AND status = 'Occupied'
        ORDER BY startTimestamp DESC
        LIMIT 1
    """
    current = DatabaseConnection.execute_query(
        current_bed,
        (admID,),
        fetch_one=True,
        fetch_dict=True
    )
    
    if not current:
        raise ValueError("No active bed assignment found for this admission")
    
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
            WHERE biID = %s
        """
        DatabaseConnection.execute_query(
            update_bed_info,
            (current['biid'],),
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
        WITH bed_history AS (
            SELECT 
                bi.biID,
                bi.bedID,
                bi.roomID,
                bi.startTimestamp,
                bi.status,
                ROW_NUMBER() OVER (ORDER BY bi.startTimestamp) as rn
            FROM bedInfo bi
            WHERE bi.asgAdmID = %s
            ORDER BY bi.startTimestamp
        ),
        transfer_data AS (
            SELECT 
                t.transferID,
                t.admID,
                t.destBedID,
                t.transferedAt,
                t.cost,
                ROW_NUMBER() OVER (PARTITION BY t.admID ORDER BY t.transferedAt) as trn
            FROM transfer t
            WHERE t.admID = %s
        )
        SELECT 
            bh_prev.bedID as from_bed_id,
            bh_curr.bedID as to_bed_id,
            r_prev.name as from_room,
            r_curr.name as to_room,
            dep_prev.name as from_department,
            dep_curr.name as to_department,
            bh_curr.startTimestamp as transferedAt,
            COALESCE(td.cost, 0) as cost,
            COALESCE(td.transferID, 0) as transferID
        FROM bed_history bh_curr
        JOIN bed_history bh_prev ON bh_prev.rn = bh_curr.rn - 1
        JOIN room r_prev ON bh_prev.roomID = r_prev.roomID
        JOIN room r_curr ON bh_curr.roomID = r_curr.roomID
        LEFT JOIN department dep_prev ON r_prev.departID = dep_prev.departID
        LEFT JOIN department dep_curr ON r_curr.departID = dep_curr.departID
        LEFT JOIN transfer_data td ON td.trn = bh_curr.rn - 1
        WHERE bh_curr.rn > 1
        ORDER BY bh_curr.startTimestamp DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (admID, admID),
        fetch_all=True,
        fetch_dict=True
    )
    
def update_admission_end_time(admID):
    query = """
        UPDATE admission
        SET endTime = CURRENT_TIMESTAMP
        WHERE admID = %s
        RETURNING admID
    """
    result = DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_admission_waiting_time(admID):
    query = """
        SELECT 
            admID,
            createdAt,
            endTime,
            EXTRACT(EPOCH FROM (COALESCE(endTime, CURRENT_TIMESTAMP) - createdAt)) / 60 as waiting_minutes
        FROM admission
        WHERE admID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (admID,),
        fetch_one=True,
        fetch_dict=True
    )