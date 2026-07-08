from app.database.connection import DatabaseConnection


def get_all_icd(limit=100, offset=0):
    query = """
        SELECT 
            icdID as id,
            code,
            diseaseName as name,
            'icd' as type
        FROM icdCode
        ORDER BY code
        LIMIT %s OFFSET %s
    """
    return DatabaseConnection.execute_query(query, (limit, offset), fetch_all=True, fetch_dict=True)

def get_icd_count():
    query = "SELECT COUNT(*) as total FROM icdCode"
    result = DatabaseConnection.execute_query(query, fetch_one=True, fetch_dict=True)
    return result['total'] if result else 0

def get_icd_by_id(icd_id):
    query = """
        SELECT 
            icdID as id,
            code,
            diseaseName as name,
            'icd' as type
        FROM icdCode
        WHERE icdID = %s
    """
    return DatabaseConnection.execute_query(query, (icd_id,), fetch_one=True, fetch_dict=True)

def search_icd(search_term):
    query = """
        SELECT 
            icdID as id,
            code,
            diseaseName as name,
            'icd' as type
        FROM icdCode
        WHERE code ILIKE %s OR diseaseName ILIKE %s
        ORDER BY code
        LIMIT 50
    """
    search_pattern = f'%{search_term}%'
    return DatabaseConnection.execute_query(query, (search_pattern, search_pattern), fetch_all=True, fetch_dict=True)

def insert_icd(data):
    query = """
        INSERT INTO icdCode (code, diseaseName)
        VALUES (%s, %s)
        RETURNING icdID
    """
    result = DatabaseConnection.execute_query(
        query, 
        (data.get('code'), data.get('name')), 
        fetch_one=True, 
        commit=True
    )
    if result:
        return result[0]
    return None

def update_icd(icd_id, data):
    query = """
        UPDATE icdCode
        SET code = %s, diseaseName = %s
        WHERE icdID = %s
        RETURNING icdID
    """
    result = DatabaseConnection.execute_query(query, (data.get('code'), data.get('name'), icd_id), fetch_one=True, commit=True)
    return result[0] if result else None

def delete_icd(icd_id):
    query = "DELETE FROM icdCode WHERE icdID = %s RETURNING icdID"
    result = DatabaseConnection.execute_query(query, (icd_id,), fetch_one=True, commit=True)
    return result[0] if result else None


def get_all_icdm(limit=100, offset=0):
    query = """
        SELECT 
            icdmID as id,
            medicineName as name,
            icdID,
            'icdm' as type
        FROM icdmCode
        ORDER BY medicineName
        LIMIT %s OFFSET %s
    """
    return DatabaseConnection.execute_query(query, (limit, offset), fetch_all=True, fetch_dict=True)

def get_icdm_count():
    query = "SELECT COUNT(*) as total FROM icdmCode"
    result = DatabaseConnection.execute_query(query, fetch_one=True, fetch_dict=True)
    return result['total'] if result else 0

def get_icdm_by_id(icdm_id):
    query = """
        SELECT 
            icdmID as id,
            medicineName as name,
            icdID,
            'icdm' as type
        FROM icdmCode
        WHERE icdmID = %s
    """
    return DatabaseConnection.execute_query(query, (icdm_id,), fetch_one=True, fetch_dict=True)

def search_icdm(search_term):
    query = """
        SELECT 
            icdmID as id,
            medicineName as name,
            icdID,
            'icdm' as type
        FROM icdmCode
        WHERE medicineName ILIKE %s
        ORDER BY medicineName
        LIMIT 50
    """
    search_pattern = f'%{search_term}%'
    return DatabaseConnection.execute_query(query, (search_pattern,), fetch_all=True, fetch_dict=True)

def insert_icdm(data):
    query = """
        INSERT INTO icdmCode (icdID, medicineName)
        VALUES (%s, %s)
        RETURNING icdmID
    """
    result = DatabaseConnection.execute_query(
        query, 
        (data.get('icd_id'), data.get('name')), 
        fetch_one=True, 
        commit=True
    )
    if result:
        return result[0]
    return None

def update_icdm(icdm_id, data):
    query = """
        UPDATE icdmCode
        SET medicineName = %s, icdID = %s
        WHERE icdmID = %s
        RETURNING icdmID
    """
    result = DatabaseConnection.execute_query(query, (data.get('name'), data.get('icd_id'), icdm_id), fetch_one=True, commit=True)
    return result[0] if result else None

def delete_icdm(icdm_id):
    query = "DELETE FROM icdmCode WHERE icdmID = %s RETURNING icdmID"
    result = DatabaseConnection.execute_query(query, (icdm_id,), fetch_one=True, commit=True)
    return result[0] if result else None


def get_all_icdt(limit=100, offset=0):
    query = """
        SELECT 
            icdtID as id,
            testName as name,
            cost,
            'icdt' as type
        FROM icdtCode
        ORDER BY testName
        LIMIT %s OFFSET %s
    """
    return DatabaseConnection.execute_query(query, (limit, offset), fetch_all=True, fetch_dict=True)

def get_icdt_count():
    query = "SELECT COUNT(*) as total FROM icdtCode"
    result = DatabaseConnection.execute_query(query, fetch_one=True, fetch_dict=True)
    return result['total'] if result else 0

def get_icdt_by_id(icdt_id):
    query = """
        SELECT 
            icdtID as id,
            testName as name,
            cost,
            'icdt' as type
        FROM icdtCode
        WHERE icdtID = %s
    """
    return DatabaseConnection.execute_query(query, (icdt_id,), fetch_one=True, fetch_dict=True)

def search_icdt(search_term):
    query = """
        SELECT 
            icdtID as id,
            testName as name,
            cost,
            'icdt' as type
        FROM icdtCode
        WHERE testName ILIKE %s
        ORDER BY testName
        LIMIT 50
    """
    search_pattern = f'%{search_term}%'
    return DatabaseConnection.execute_query(query, (search_pattern,), fetch_all=True, fetch_dict=True)

def insert_icdt(data):
    query = """
        INSERT INTO icdtCode (testName, cost)
        VALUES (%s, %s)
        RETURNING icdtID
    """
    result = DatabaseConnection.execute_query(
        query, 
        (data.get('name'), data.get('cost', 0)), 
        fetch_one=True, 
        commit=True
    )
    if result:
        return result[0]
    return None

def update_icdt(icdt_id, data):
    query = """
        UPDATE icdtCode
        SET testName = %s, cost = %s
        WHERE icdtID = %s
        RETURNING icdtID
    """
    result = DatabaseConnection.execute_query(query, (data.get('name'), data.get('cost', 0), icdt_id), fetch_one=True, commit=True)
    return result[0] if result else None

def delete_icdt(icdt_id):
    query = "DELETE FROM icdtCode WHERE icdtID = %s RETURNING icdtID"
    result = DatabaseConnection.execute_query(query, (icdt_id,), fetch_one=True, commit=True)
    return result[0] if result else None


def get_all_icds(limit=100, offset=0):
    query = """
        SELECT 
            icdsID as id,
            surgeryName as name,
            cost,
            'icds' as type
        FROM icdsCode
        ORDER BY surgeryName
        LIMIT %s OFFSET %s
    """
    return DatabaseConnection.execute_query(query, (limit, offset), fetch_all=True, fetch_dict=True)

def get_icds_count():
    query = "SELECT COUNT(*) as total FROM icdsCode"
    result = DatabaseConnection.execute_query(query, fetch_one=True, fetch_dict=True)
    return result['total'] if result else 0

def get_icds_by_id(icds_id):
    query = """
        SELECT 
            icdsID as id,
            surgeryName as name,
            cost,
            'icds' as type
        FROM icdsCode
        WHERE icdsID = %s
    """
    return DatabaseConnection.execute_query(query, (icds_id,), fetch_one=True, fetch_dict=True)

def search_icds(search_term):
    query = """
        SELECT 
            icdsID as id,
            surgeryName as name,
            cost,
            'icds' as type
        FROM icdsCode
        WHERE surgeryName ILIKE %s
        ORDER BY surgeryName
        LIMIT 50
    """
    search_pattern = f'%{search_term}%'
    return DatabaseConnection.execute_query(query, (search_pattern,), fetch_all=True, fetch_dict=True)

def insert_icds(data):
    query = """
        INSERT INTO icdsCode (surgeryName, cost)
        VALUES (%s, %s)
        RETURNING icdsID
    """
    result = DatabaseConnection.execute_query(
        query, 
        (data.get('name'), data.get('cost', 0)), 
        fetch_one=True, 
        commit=True
    )
    if result:
        return result[0]
    return None

def update_icds(icds_id, data):
    query = """
        UPDATE icdsCode
        SET surgeryName = %s, cost = %s
        WHERE icdsID = %s
        RETURNING icdsID
    """
    result = DatabaseConnection.execute_query(query, (data.get('name'), data.get('cost', 0), icds_id), fetch_one=True, commit=True)
    return result[0] if result else None

def delete_icds(icds_id):
    query = "DELETE FROM icdsCode WHERE icdsID = %s RETURNING icdsID"
    result = DatabaseConnection.execute_query(query, (icds_id,), fetch_one=True, commit=True)
    return result[0] if result else None


def get_all_icd_for_dropdown():
    query = """
        SELECT 
            icdID as id,
            code || ' - ' || diseaseName as label
        FROM icdCode
        ORDER BY code
    """
    return DatabaseConnection.execute_query(query, fetch_all=True, fetch_dict=True)

def get_all_signtypes():
    query = """
        SELECT 
            sTypeID as id,
            signName as name
        FROM signType
        ORDER BY signName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_signtype_by_id(signtype_id):
    query = """
        SELECT 
            sTypeID as id,
            signName as name
        FROM signType
        WHERE sTypeID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (signtype_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_signtype(data):
    query = """
        INSERT INTO signType (signName)
        VALUES (%s)
        RETURNING sTypeID
    """
    result = DatabaseConnection.execute_query(
        query,
        (data.get('name'),),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_signtype(signtype_id, data):
    query = """
        UPDATE signType
        SET signName = %s
        WHERE sTypeID = %s
        RETURNING sTypeID
    """
    result = DatabaseConnection.execute_query(
        query,
        (data.get('name'), signtype_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_signtype(signtype_id):
    query = "DELETE FROM signType WHERE sTypeID = %s RETURNING sTypeID"
    result = DatabaseConnection.execute_query(
        query,
        (signtype_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_parameters():
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

def get_parameter_by_id(parameter_id):
    query = """
        SELECT 
            parameterID as id,
            parameterName as name,
            min,
            max,
            average
        FROM parameterList
        WHERE parameterID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (parameter_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_parameter(data):
    query = """
        INSERT INTO parameterList (parameterName, min, max, average)
        VALUES (%s, %s, %s, %s)
        RETURNING parameterID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('min'),
            data.get('max'),
            data.get('average')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_parameter(parameter_id, data):
    query = """
        UPDATE parameterList
        SET parameterName = %s, min = %s, max = %s, average = %s
        WHERE parameterID = %s
        RETURNING parameterID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('min'),
            data.get('max'),
            data.get('average'),
            parameter_id
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_parameter(parameter_id):
    query = "DELETE FROM parameterList WHERE parameterID = %s RETURNING parameterID"
    result = DatabaseConnection.execute_query(
        query,
        (parameter_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_equipment():
    query = """
        SELECT 
            equipID as id,
            name,
            MACAddress,
            description,
            e.sTypeID,
            st.signName as sign_type_name
        FROM equipment e
        LEFT JOIN signType st ON e.sTypeID = st.sTypeID
        ORDER BY e.name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_equipment_by_id(equip_id):
    query = """
        SELECT 
            equipID as id,
            name,
            MACAddress,
            description,
            sTypeID
        FROM equipment
        WHERE equipID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (equip_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_equipment(data):
    query = """
        INSERT INTO equipment (name, MACAddress, description, sTypeID)
        VALUES (%s, %s, %s, %s)
        RETURNING equipID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('macaddress'),
            data.get('description'),
            data.get('sTypeID')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_equipment(equip_id, data):
    query = """
        UPDATE equipment
        SET name = %s, MACAddress = %s, description = %s, sTypeID = %s
        WHERE equipID = %s
        RETURNING equipID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('name'),
            data.get('macaddress'),
            data.get('description'),
            data.get('sTypeID'),
            equip_id
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_equipment(equip_id):
    query = "DELETE FROM equipment WHERE equipID = %s RETURNING equipID"
    result = DatabaseConnection.execute_query(
        query,
        (equip_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_beds():
    query = """
        SELECT 
            bedID as id,
            cost
        FROM bed
        ORDER BY bedID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_bed_by_id(bed_id):
    query = """
        SELECT 
            bedID as id,
            cost
        FROM bed
        WHERE bedID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (bed_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_bed(data):
    query = """
        INSERT INTO bed (cost)
        VALUES (%s)
        RETURNING bedID
    """
    result = DatabaseConnection.execute_query(
        query,
        (data.get('cost', 0),),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_bed(bed_id, data):
    query = """
        UPDATE bed
        SET cost = %s
        WHERE bedID = %s
        RETURNING bedID
    """
    result = DatabaseConnection.execute_query(
        query,
        (data.get('cost', 0), bed_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_bed(bed_id):
    query = "DELETE FROM bed WHERE bedID = %s RETURNING bedID"
    result = DatabaseConnection.execute_query(
        query,
        (bed_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_bedinfo():
    query = """
        SELECT 
            bi.biID,
            bi.bedID,
            bi.roomID,
            bi.asgAdmID,
            bi.startTimestamp,
            bi.status,
            b.cost as bed_cost,
            r.name as room_name,
            dep.name as department_name,
            p.firstName || ' ' || p.lastName as patient_name,
            a.admID
        FROM bedInfo bi
        JOIN bed b ON bi.bedID = b.bedID
        JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        LEFT JOIN admission a ON bi.asgAdmID = a.admID
        LEFT JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN patient p ON mr.pID = p.pID
        ORDER BY bi.startTimestamp DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_bedinfo_by_id(biID):
    query = """
        SELECT 
            bi.biID,
            bi.bedID,
            bi.roomID,
            bi.asgAdmID,
            bi.startTimestamp,
            bi.status,
            b.cost as bed_cost,
            r.name as room_name,
            dep.name as department_name
        FROM bedInfo bi
        JOIN bed b ON bi.bedID = b.bedID
        JOIN room r ON bi.roomID = r.roomID
        LEFT JOIN department dep ON r.departID = dep.departID
        WHERE bi.biID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (biID,),
        fetch_one=True,
        fetch_dict=True
    )

def create_bedinfo(data):
    query = """
        INSERT INTO bedInfo (bedID, roomID, asgAdmID, startTimestamp, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING biID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('bedID'),
            data.get('roomID'),
            data.get('asgAdmID') or None,
            data.get('startTimestamp') or 'CURRENT_TIMESTAMP',
            data.get('status', 'Available')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_bedinfo(biID, data):
    query = """
        UPDATE bedInfo
        SET bedID = %s,
            roomID = %s,
            asgAdmID = %s,
            startTimestamp = %s,
            status = %s
        WHERE biID = %s
        RETURNING biID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('bedID'),
            data.get('roomID'),
            data.get('asgAdmID') or None,
            data.get('startTimestamp'),
            data.get('status'),
            biID
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_bedinfo(biID):
    query = "DELETE FROM bedInfo WHERE biID = %s RETURNING biID"
    result = DatabaseConnection.execute_query(
        query,
        (biID,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_beds_for_dropdown():
    query = """
        SELECT 
            bedID as id,
            'Bed #' || bedID || ' - $' || cost as label,
            cost
        FROM bed
        ORDER BY bedID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_all_admissions_for_dropdown():
    query = """
        SELECT 
            admID as id,
            'Admission #' || admID as label
        FROM admission
        ORDER BY admID DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_all_rooms_for_dropdown():
    query = """
        SELECT 
            roomID as id,
            name as label
        FROM room
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )