from app.database.connection import DatabaseConnection

def get_patient_by_national_code(national_code):
    query = """
        SELECT 
            pID,
            firstName,
            lastName,
            nationalCode,
            password
        FROM patient
        WHERE nationalCode = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (national_code,),
        fetch_one=True,
        fetch_dict=True
    )

def get_patient_by_id(patient_id):
    query = """
        SELECT 
            pID,
            firstName,
            lastName,
            nationalCode,
            gender,
            dateOfBirth,
            phoneNumber,
            homeNumber,
            city,
            province,
            street,
            alley,
            houseCode,
            createdAt
        FROM patient
        WHERE pID = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )

def create_patient(data):
    query = """
        INSERT INTO patient (
            firstName, lastName, nationalCode, password, gender,
            dateOfBirth, homeNumber, phoneNumber, province,
            city, street, alley, houseCode
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING pID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('firstName'),
            data.get('lastName'),
            data.get('nationalCode'),
            data.get('password'),
            data.get('gender'),
            data.get('dateOfBirth'),
            data.get('homeNumber'),
            data.get('phoneNumber'),
            data.get('province'),
            data.get('city'),
            data.get('street'),
            data.get('alley'),
            data.get('houseCode')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def check_patient_exists(national_code):
    query = "SELECT pID FROM patient WHERE nationalCode = %s"
    result = DatabaseConnection.execute_query(
        query,
        (national_code,),
        fetch_one=True,
        fetch_dict=True
    )
    return result is not None

def create_medical_record(patient_id):
    query = """
        INSERT INTO medicalRecord (pID)
        VALUES (%s)
        RETURNING mID
    """
    result = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_employee_by_national_code(national_code):
    query = """
        SELECT 
            employeeID,
            firstName,
            lastName,
            nationalCode,
            password,
            accessLevel
        FROM employee
        WHERE nationalCode = %s
    """
    return DatabaseConnection.execute_query(
        query,
        (national_code,),
        fetch_one=True,
        fetch_dict=True
    )

def get_employee_role(employee_id):
    query = """
        SELECT 
            CASE 
                WHEN EXISTS (SELECT 1 FROM doctor WHERE employeeID = %s) THEN 'doctor'
                WHEN EXISTS (SELECT 1 FROM surgeon WHERE employeeID = %s) THEN 'surgeon'
                WHEN EXISTS (SELECT 1 FROM nurse WHERE employeeID = %s) THEN 'nurse'
                WHEN EXISTS (SELECT 1 FROM officeStaff WHERE employeeID = %s) THEN 'officeStaff'
                ELSE 'employee'
            END as role
    """
    return DatabaseConnection.execute_query(
        query,
        (employee_id, employee_id, employee_id, employee_id),
        fetch_one=True,
        fetch_dict=True
    )

def get_all_departments():
    query = """
        SELECT 
            departID,
            name
        FROM department
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def create_employee(data):
    query = """
        INSERT INTO employee (
            firstName, lastName, nationalCode, password, departID,
            contractType, hireDate, accessLevel, salary
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING employeeID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data.get('firstName'),
            data.get('lastName'),
            data.get('nationalCode'),
            data.get('password'),
            data.get('departID'),
            data.get('contractType'),
            data.get('hireDate'),
            data.get('accessLevel'),
            data.get('salary')
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def assign_employee_role(employee_id, role):
    if role == 'doctor':
        query = """
            INSERT INTO doctor (employeeID, medicalNumber, visitCost)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', 0)
    elif role == 'surgeon':
        query = """
            INSERT INTO surgeon (employeeID, medicalNumber)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', '')
    elif role == 'nurse':
        query = """
            INSERT INTO nurse (employeeID, medicalNumber, grade)
            VALUES (%s, %s, %s)
        """
        params = (employee_id, '', '')
    elif role == 'officeStaff':
        query = """
            INSERT INTO officeStaff (employeeID, role)
            VALUES (%s, %s)
        """
        params = (employee_id, '')
    else:
        raise ValueError(f"Invalid role: {role}")
    
    DatabaseConnection.execute_query(
        query,
        params,
        commit=True
    )

def check_employee_exists(national_code):
    query = "SELECT employeeID FROM employee WHERE nationalCode = %s"
    result = DatabaseConnection.execute_query(
        query,
        (national_code,),
        fetch_one=True,
        fetch_dict=True
    )
    return result is not None

def get_doctors_with_specialization(search_term=None):
    query = """
        SELECT 
            e.employeeID,
            e.firstName,
            e.lastName,
            s.name
        FROM employee e
        JOIN doctor d ON e.employeeID = d.employeeID JOIN doctorSpecialization ds ON d.employeeID = ds.docID JOIN specializationFields s 
        ON s.specID = ds.specID
    """
    params = []
    
    if search_term:
        query += """
            WHERE e.firstName ILIKE %s 
            OR e.lastName ILIKE %s 
            OR s.name ILIKE %s
            LIMIT 9
        """
        search_pattern = f'%{search_term}%'
        params = [search_pattern, search_pattern, search_pattern]
    else:
        query += " LIMIT 6"
    
    return DatabaseConnection.execute_query(
        query,
        tuple(params) if params else None,
        fetch_all=True,
        fetch_dict=True
    )

def get_patient_medical_info(patient_id):
    query = """
        SELECT 
            p.firstName,
            p.lastName,
            m.bloodType,
            m.smokingHistory
        FROM patient p
        JOIN medicalRecord m ON p.pID = m.pID
        WHERE p.pID = %s
    """
    info = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_one=True,
        fetch_dict=True
    )
    
    query = """
        SELECT 
            icdCode.diseaseName,
            diseaseRecord.description
        FROM diseaseRecord
        JOIN icdCode ON diseaseRecord.icdID = icdCode.icdID
        JOIN medicalRecord ON diseaseRecord.mID = medicalRecord.mID
        WHERE medicalRecord.pID = %s
    """
    diseases = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    query = """
        SELECT 
            drugRecord.description
        FROM drugRecord
        JOIN medicalRecord ON drugRecord.mID = medicalRecord.mID
        WHERE medicalRecord.pID = %s
    """
    drugs = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    query = """
        SELECT 
            icdmCode.medicineName,
            medicineRecord.description
        FROM medicineRecord
        JOIN icdmCode ON medicineRecord.icdmID = icdmCode.icdmID
        JOIN medicalRecord ON medicineRecord.mID = medicalRecord.mID
        WHERE medicalRecord.pID = %s
    """
    medicines = DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )
    
    return {
        'info': info,
        'diseases': diseases,
        'drugs': drugs,
        'medicines': medicines
    }