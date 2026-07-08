from app.database.connection import DatabaseConnection
from datetime import datetime, timedelta

# ==================== SHIFT MANAGEMENT QUERIES ====================

def get_all_shifts(start_date=None, end_date=None):
    """Get all shifts with employee assignments"""
    query = """
        SELECT 
            s.shiftID,
            s.shiftDate::DATE as shiftDate,
            s.startTime::TIME as startTime,
            s.endTime::TIME as endTime,
            COUNT(es.employeeID) as assigned_count,
            STRING_AGG(e.firstName || ' ' || e.lastName, ', ') as assigned_employees
        FROM shift s
        LEFT JOIN employeeShift es ON s.shiftID = es.shiftID
        LEFT JOIN employee e ON es.employeeID = e.employeeID
        WHERE 1=1
    """
    params = []
    
    if start_date:
        query += " AND s.shiftDate::DATE >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND s.shiftDate::DATE <= %s"
        params.append(end_date)
    
    query += """
        GROUP BY s.shiftID, s.shiftDate, s.startTime, s.endTime
        ORDER BY s.shiftDate DESC, s.startTime
    """
    
    results = DatabaseConnection.execute_query(
        query,
        tuple(params) if params else None,
        fetch_all=True,
        fetch_dict=True
    )
    
    # Convert time objects to strings for JSON serialization
    for row in results:
        if 'starttime' in row and row['starttime']:
            row['starttime'] = str(row['starttime'])
        if 'endtime' in row and row['endtime']:
            row['endtime'] = str(row['endtime'])
        if 'shiftdate' in row and row['shiftdate']:
            row['shiftdate'] = str(row['shiftdate'])
    
    return results

def get_shift_by_id(shift_id):
    """Get a specific shift by ID"""
    query = """
        SELECT 
            s.shiftID,
            s.shiftDate::DATE as shiftDate,
            s.startTime::TIME as startTime,
            s.endTime::TIME as endTime
        FROM shift s
        WHERE s.shiftID = %s
    """
    result = DatabaseConnection.execute_query(
        query,
        (shift_id,),
        fetch_one=True,
        fetch_dict=True
    )
    
    # Convert time objects to strings
    if result:
        if 'starttime' in result and result['starttime']:
            result['starttime'] = str(result['starttime'])
        if 'endtime' in result and result['endtime']:
            result['endtime'] = str(result['endtime'])
        if 'shiftdate' in result and result['shiftdate']:
            result['shiftdate'] = str(result['shiftdate'])
    
    return result

def get_employees_on_shift(shift_id):
    """Get all employees assigned to a specific shift"""
    query = """
        SELECT 
            e.employeeID,
            e.firstName,
            e.lastName,
            e.nationalCode,
            e.accessLevel,
            e.contractType,
            d.name as department_name
        FROM employeeShift es
        JOIN employee e ON es.employeeID = e.employeeID
        LEFT JOIN department d ON e.departID = d.departID
        WHERE es.shiftID = %s
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query,
        (shift_id,),
        fetch_all=True,
        fetch_dict=True
    )

def create_shift(shift_date, start_time, end_time):
    """Create a new shift - convert times to TIMESTAMP format"""
    # Convert to datetime objects for TIMESTAMP columns
    start_datetime = f"{shift_date} {start_time}:00"
    end_datetime = f"{shift_date} {end_time}:00"
    
    query = """
        INSERT INTO shift (shiftDate, startTime, endTime)
        VALUES (%s, %s, %s)
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (shift_date, start_datetime, end_datetime),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def update_shift(shift_id, shift_date, start_time, end_time):
    """Update an existing shift"""
    start_datetime = f"{shift_date} {start_time}:00"
    end_datetime = f"{shift_date} {end_time}:00"
    
    query = """
        UPDATE shift
        SET shiftDate = %s, startTime = %s, endTime = %s
        WHERE shiftID = %s
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (shift_date, start_datetime, end_datetime, shift_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_shift(shift_id):
    """Delete a shift (also removes employee assignments via CASCADE)"""
    query = "DELETE FROM shift WHERE shiftID = %s RETURNING shiftID"
    result = DatabaseConnection.execute_query(
        query,
        (shift_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def assign_employee_to_shift(employee_id, shift_id):
    """Assign an employee to a shift"""
    # Check if already assigned
    check_query = """
        SELECT 1 FROM employeeShift 
        WHERE employeeID = %s AND shiftID = %s
    """
    existing = DatabaseConnection.execute_query(
        check_query,
        (employee_id, shift_id),
        fetch_one=True
    )
    
    if existing:
        return False  # Already assigned
    
    query = """
        INSERT INTO employeeShift (employeeID, shiftID)
        VALUES (%s, %s)
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (employee_id, shift_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def remove_employee_from_shift(employee_id, shift_id):
    """Remove an employee from a shift"""
    query = """
        DELETE FROM employeeShift 
        WHERE employeeID = %s AND shiftID = %s
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (employee_id, shift_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_employees():
    """Get all employees for assignment dropdown"""
    query = """
        SELECT 
            e.employeeID as id,
            e.firstName || ' ' || e.lastName as name,
            e.nationalCode,
            e.accessLevel,
            d.name as department_name
        FROM employee e
        LEFT JOIN department d ON e.departID = d.departID
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_available_employees_for_shift(shift_id):
    """Get employees not assigned to a specific shift"""
    query = """
        SELECT 
            e.employeeID as id,
            e.firstName || ' ' || e.lastName as name,
            e.nationalCode,
            e.accessLevel,
            d.name as department_name
        FROM employee e
        LEFT JOIN department d ON e.departID = d.departID
        WHERE e.employeeID NOT IN (
            SELECT employeeID FROM employeeShift WHERE shiftID = %s
        )
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query,
        (shift_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_shift_statistics():
    """Get shift statistics for dashboard - fixed column names"""
    query = """
        SELECT 
            COUNT(*) as total_shifts,
            COUNT(DISTINCT s.shiftDate::DATE) as total_days,
            COALESCE(AVG(assigned_count), 0) as avg_employees_per_shift
        FROM shift s
        LEFT JOIN (
            SELECT shiftID, COUNT(employeeID) as assigned_count
            FROM employeeShift
            GROUP BY shiftID
        ) es ON s.shiftID = es.shiftID
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )

def get_shifts_by_date_range(start_date, end_date):
    """Get shifts within a date range with assignments"""
    query = """
        SELECT 
            s.shiftID,
            s.shiftDate::DATE as shiftDate,
            s.startTime::TIME as startTime,
            s.endTime::TIME as endTime,
            COUNT(es.employeeID) as assigned_count,
            STRING_AGG(e.firstName || ' ' || e.lastName, ', ') as assigned_employees
        FROM shift s
        LEFT JOIN employeeShift es ON s.shiftID = es.shiftID
        LEFT JOIN employee e ON es.employeeID = e.employeeID
        WHERE s.shiftDate::DATE BETWEEN %s AND %s
        GROUP BY s.shiftID, s.shiftDate, s.startTime, s.endTime
        ORDER BY s.shiftDate, s.startTime
    """
    results = DatabaseConnection.execute_query(
        query,
        (start_date, end_date),
        fetch_all=True,
        fetch_dict=True
    )
    
    # Convert time objects to strings
    for row in results:
        if 'starttime' in row and row['starttime']:
            row['starttime'] = str(row['starttime'])
        if 'endtime' in row and row['endtime']:
            row['endtime'] = str(row['endtime'])
        if 'shiftdate' in row and row['shiftdate']:
            row['shiftdate'] = str(row['shiftdate'])
    
    return results

def get_employee_shifts(employee_id, start_date=None, end_date=None):
    """Get all shifts for a specific employee"""
    query = """
        SELECT 
            s.shiftID,
            s.shiftDate::DATE as shiftDate,
            s.startTime::TIME as startTime,
            s.endTime::TIME as endTime
        FROM shift s
        JOIN employeeShift es ON s.shiftID = es.shiftID
        WHERE es.employeeID = %s
    """
    params = [employee_id]
    
    if start_date:
        query += " AND s.shiftDate::DATE >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND s.shiftDate::DATE <= %s"
        params.append(end_date)
    
    query += " ORDER BY s.shiftDate DESC, s.startTime"
    
    results = DatabaseConnection.execute_query(
        query,
        tuple(params),
        fetch_all=True,
        fetch_dict=True
    )
    
    # Convert time objects to strings
    for row in results:
        if 'starttime' in row and row['starttime']:
            row['starttime'] = str(row['starttime'])
        if 'endtime' in row and row['endtime']:
            row['endtime'] = str(row['endtime'])
        if 'shiftdate' in row and row['shiftdate']:
            row['shiftdate'] = str(row['shiftdate'])
    
    return results