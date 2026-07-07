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