from app.database.connection import DatabaseConnection

def get_all_staff():
    query = """
        SELECT 
            e.employeeID,
            e.firstName,
            e.lastName,
            e.nationalCode,
            e.contractType,
            e.hireDate,
            e.accessLevel,
            e.salary,
            d.name as department_name,
            CASE 
                WHEN doc.employeeID IS NOT NULL THEN 'Doctor'
                WHEN surg.employeeID IS NOT NULL THEN 'Surgeon'
                WHEN nur.employeeID IS NOT NULL THEN 'Nurse'
                WHEN off.employeeID IS NOT NULL THEN 'Office Staff'
                ELSE 'Unknown'
            END as role
        FROM employee e
        LEFT JOIN department d ON e.departID = d.departID
        LEFT JOIN doctor doc ON e.employeeID = doc.employeeID
        LEFT JOIN surgeon surg ON e.employeeID = surg.employeeID
        LEFT JOIN nurse nur ON e.employeeID = nur.employeeID
        LEFT JOIN officeStaff off ON e.employeeID = off.employeeID
        ORDER BY e.employeeID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_staff_by_id(employee_id):
    query = """
        SELECT 
            e.employeeID,
            e.firstName,
            e.lastName,
            e.nationalCode,
            e.contractType,
            e.hireDate,
            e.accessLevel,
            e.salary,
            e.departID,
            d.name as department_name,
            CASE 
                WHEN doc.employeeID IS NOT NULL THEN 'Doctor'
                WHEN surg.employeeID IS NOT NULL THEN 'Surgeon'
                WHEN nur.employeeID IS NOT NULL THEN 'Nurse'
                WHEN off.employeeID IS NOT NULL THEN 'Office Staff'
                ELSE 'Unknown'
            END as role,
            doc.medicalNumber as doctor_medicalNumber,
            doc.visitCost,
            surg.medicalNumber as surgeon_medicalNumber,
            nur.medicalNumber as nurse_medicalNumber
        FROM employee e
        LEFT JOIN department d ON e.departID = d.departID
        LEFT JOIN doctor doc ON e.employeeID = doc.employeeID
        LEFT JOIN surgeon surg ON e.employeeID = surg.employeeID
        LEFT JOIN nurse nur ON e.employeeID = nur.employeeID
        LEFT JOIN officeStaff off ON e.employeeID = off.employeeID
        WHERE e.employeeID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (employee_id,),
        fetch_one=True,
        fetch_dict=True
    )

def get_staff_by_national_code(national_code):
    query = """
        SELECT employeeID FROM employee WHERE nationalCode = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (national_code,),
        fetch_one=True,
        fetch_dict=True
    )

def update_employee(employee_id, data):
    query = """
        UPDATE employee
        SET 
            firstName = %s,
            lastName = %s,
            nationalCode = %s,
            contractType = %s,
            hireDate = %s,
            accessLevel = %s,
            salary = %s,
            departID = %s
        WHERE employeeID = %s
        RETURNING employeeID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('firstName'),
            data.get('lastName'),
            data.get('nationalCode'),
            data.get('contractType'),
            data.get('hireDate'),
            data.get('accessLevel'),
            data.get('salary'),
            data.get('departID'),
            employee_id
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_employee(employee_id):
    query = "DELETE FROM employee WHERE employeeID = %s RETURNING employeeID"
    result = DatabaseConnection.execute_query(
        query,
        (employee_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_employee_role(employee_id, new_role):
    query = """
        DELETE FROM doctor WHERE employeeID = %s;
        DELETE FROM surgeon WHERE employeeID = %s;
        DELETE FROM nurse WHERE employeeID = %s;
        DELETE FROM officeStaff WHERE employeeID = %s;
    """
    DatabaseConnection.execute_query(
        query,
        (employee_id, employee_id, employee_id, employee_id),
        commit=True
    )
    
    if new_role == 'doctor':
        query = """
            INSERT INTO doctor (employeeID, medicalNumber, visitCost)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', '', 0)
    elif new_role == 'surgeon':
        query = """
            INSERT INTO surgeon (employeeID, medicalNumber)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', '')
    elif new_role == 'nurse':
        query = """
            INSERT INTO nurse (employeeID, medicalNumber, grade)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', '')
    elif new_role == 'officeStaff':
        query = """
            INSERT INTO officeStaff (employeeID, role)
            VALUES (%s, %s)
        """
        params = (employee_id, '')
    else:
        raise ValueError(f"Invalid role: {new_role}")
    
    DatabaseConnection.execute_query(
        query,
        params,
        commit=True
    )
    
    query = """
        UPDATE employee
        SET accessLevel = %s
        WHERE employeeID = %s
        RETURNING employeeID
    """
    result = DatabaseConnection.execute_query(
        query,
        (new_role, employee_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_staff_count():
    query = "SELECT COUNT(*) as total FROM employee"
    result = DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )
    return result['total'] if result else 0

def get_staff_by_role(role):
    role_table_map = {
        'doctor': 'doctor',
        'surgeon': 'surgeon',
        'nurse': 'nurse',
        'officeStaff': 'officeStaff'
    }
    
    if role not in role_table_map:
        return []
    
    query = f"""
        SELECT 
            e.employeeID,
            e.firstName,
            e.lastName,
            e.nationalCode,
            e.contractType,
            e.hireDate,
            e.salary,
            d.name as department_name
        FROM employee e
        JOIN {role_table_map[role]} r ON e.employeeID = r.employeeID
        LEFT JOIN department d ON e.departID = d.departID
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )