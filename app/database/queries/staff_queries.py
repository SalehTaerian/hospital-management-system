from app.database.connection import DatabaseConnection
from datetime import datetime, timedelta


def search_patients(search_term):
    query = """
        SELECT 
            p.pID,
            p.firstName,
            p.lastName,
            p.nationalCode,
            p.phoneNumber,
            p.city,
            p.dateOfBirth,
            EXTRACT(YEAR FROM age(CURRENT_DATE, p.dateOfBirth)) as age
        FROM patient AS p
        WHERE 
            p.nationalCode ILIKE %s
        ORDER BY p.lastName
        LIMIT 50
    """
    search_pattern = f'%{search_term}%'
    return DatabaseConnection.execute_query(
        query, 
        (search_pattern, search_pattern, search_pattern, search_pattern), 
        fetch_all=True, 
        fetch_dict=True
    )

def get_patient_basic_info(patient_id):
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
            p.city,
            p.province,
            p.createdAt,
            m.mID,
            m.bloodType,
            m.smokingHistory
        FROM patient p
        LEFT JOIN medicalRecord AS m ON p.pID = m.pID
        WHERE p.pID = %s
    """
    return DatabaseConnection.execute_query(
        query, 
        (patient_id,), 
        fetch_one=True, 
        fetch_dict=True
    )

def get_doctors_list():
    query = """
        SELECT 
            e.employeeID AS id,
            e.firstName || ' ' || e.lastName as name,
            d.specialization
        FROM doctor AS d
        JOIN employee AS e ON d.employeeID = e.employeeID
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def get_today_appointments():
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            p.firstName || ' ' || p.lastName as patient_name,
            e.firstName || ' ' || e.lastName as doctor_name,
            d.specialization
        FROM appointment AS a
        JOIN medicalRecord AS mr ON a.mID = mr.mID
        JOIN patient AS p ON mr.pID = p.pID
        JOIN doctor AS d ON a.doctorID = d.employeeID
        JOIN employee AS e ON d.employeeID = e.employeeID
        WHERE a.date = CURRENT_DATE
        ORDER BY a.time
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def create_appointment(data):
    shift = get_doctor_shift(data['doctor_id'], data['date'])
    if not shift:
        raise ValueError("Doctor is not on shift for this date")
    
    shift_start = shift['starttime']
    shift_end = shift['endtime']
    appointment_time = data['time']
    
    if appointment_time < shift_start or appointment_time >= shift_end:
        raise ValueError("Appointment time is outside doctor's shift hours")
    
    booked = get_booked_appointments(data['doctor_id'], data['date'])
    booked_times = [apt['time'] for apt in booked]
    
    if appointment_time in booked_times:
        raise ValueError("This time slot is already booked")
    
    mr_query = "SELECT mID FROM medicalRecord WHERE pID = %s"
    mr_result = DatabaseConnection.execute_query(
        mr_query,
        (data['patient_id'],),
        fetch_one=True,
        fetch_dict=True
    )
    
    if not mr_result:
        raise ValueError("Patient has no medical record")
    
    query = """
        INSERT INTO appointment (
            mID, doctorID, date, time, status, isOnlineReserved
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
        RETURNING appoID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            mr_result['mid'],
            data['doctor_id'],
            data['date'],
            data['time'],
            'Scheduled',
            False
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_appointments_by_patient(patient_id):
    query = """
        SELECT 
            a.appoID,
            a.date,
            a.time,
            a.status,
            e.firstName || ' ' || e.lastName AS doctor_name,
            d.specialization
        FROM appointment AS a
        JOIN doctor AS d ON a.doctorID = d.employeeID
        JOIN employee AS e ON d.employeeID = e.employeeID
        JOIN medicalRecord AS mr ON a.mID = mr.mID
        WHERE mr.pID = %s
        ORDER BY a.date DESC, a.time DESC
    """
    return DatabaseConnection.execute_query(
        query, 
        (patient_id,), 
        fetch_all=True, 
        fetch_dict=True
    )


def get_surgeons_list():
    query = """
        SELECT 
            e.employeeID AS id,
            e.firstName || ' ' || e.lastName AS name,
            s.surgicalField
        FROM surgeon AS s
        JOIN employee AS e ON s.employeeID = e.employeeID
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def get_surgery_codes():
    query = """
        SELECT 
            icdsID as id,
            surgeryName as name,
            cost
        FROM icdsCode
        ORDER BY surgeryName
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def get_today_surgeries():
    query = """
        SELECT 
            s.surgeryID,
            s.surgeryDate,
            s.status,
            p.firstName || ' ' || p.lastName AS patient_name,
            e.firstName || ' ' || e.lastName AS surgeon_name,
            sc.surgeryName AS surgery_name,
            r.name AS room_name
        FROM surgery AS s
        JOIN patient AS p ON s.pID = p.pID
        JOIN surgeon AS su ON s.chiefSurgeonId = su.employeeID
        JOIN employee AS e ON su.employeeID = e.employeeID
        JOIN icdsCode AS sc ON s.surgeryCode = sc.icdsID
        JOIN room AS r ON s.roomID = r.roomID
        WHERE DATE(s.surgeryDate) = CURRENT_DATE
        ORDER BY s.surgeryDate
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def create_surgery(data):
    query = """
        INSERT INTO surgery (
            surgeryCode, pID, chiefSurgeonId, roomID, surgeryDate, status
        ) VALUES (
            %s, %s, %s, %s, %s, %s
        )
        RETURNING surgeryID
    """
    result = DatabaseConnection.execute_query(
        query,
        (
            data['surgery_code'],
            data['patient_id'],
            data['surgeon_id'],
            data['room_id'],
            data['surgery_date'],
            'Scheduled'
        ),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_rooms_list():
    query = """
        SELECT 
            roomID as id,
            name,
            description
        FROM room
        ORDER BY name
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_all=True, 
        fetch_dict=True
    )

def get_available_rooms(surgery_date):
    query = """
        SELECT 
            r.roomID AS id,
            r.name,
            r.description
        FROM room AS r
        WHERE r.roomID NOT IN (
            SELECT roomID FROM surgery 
            WHERE DATE(surgeryDate) = %s
            AND status NOT IN ('Completed', 'Cancelled')
        )
        ORDER BY r.name
    """
    return DatabaseConnection.execute_query(
        query, 
        (surgery_date,), 
        fetch_all=True, 
        fetch_dict=True
    )


def get_dashboard_stats():
    query = """
        SELECT 
            (SELECT COUNT(*) FROM patient) AS total_patients,
            (SELECT COUNT(*) FROM appointment WHERE date = CURRENT_DATE) AS today_appointments,
            (SELECT COUNT(*) FROM surgery WHERE DATE(surgeryDate) = CURRENT_DATE) AS today_surgeries,
            (SELECT COUNT(*) FROM appointment WHERE status = 'Scheduled') AS pending_appointments,
            (SELECT COUNT(*) FROM surgery WHERE status = 'Scheduled') AS pending_surgeries
    """
    return DatabaseConnection.execute_query(
        query, 
        fetch_one=True, 
        fetch_dict=True
    )
    
def get_doctors_on_shift(shift_date):
    query = """
        SELECT DISTINCT
            e.employeeID AS id,
            e.firstName || ' ' || e.lastName AS name,
            e.lastName,
            d.specialization,
            s.startTime AS shift_start,
            s.endTime AS shift_end,
            s.shiftID
        FROM employeeShift AS es
        JOIN doctor AS d ON es.employeeID = d.employeeID
        JOIN employee AS e ON d.employeeID = e.employeeID
        JOIN shift AS s ON es.shiftID = s.shiftID
        WHERE s.shiftDate = %s
        ORDER BY e.lastName
    """
    return DatabaseConnection.execute_query(
        query, 
        (shift_date,), 
        fetch_all=True, 
        fetch_dict=True
    )
    
def get_doctor_shift(doctor_id, shift_date):
    query = """
        SELECT 
            shiftID,
            shiftDate,
            startTime,
            endTime,
            doctorID
        FROM shift
        WHERE doctorID = %s
        AND shiftDate = %s
        AND isActive = TRUE
    """
    return DatabaseConnection.execute_query(
        query, 
        (doctor_id, shift_date), 
        fetch_one=True, 
        fetch_dict=True
    )
    
def get_booked_appointments(doctor_id, shift_date):
    query = """
        SELECT 
            time,
            status
        FROM appointment
        WHERE doctorID = %s
        AND date = %s
        AND status NOT IN ('Cancelled', 'Completed')
        ORDER BY time
    """
    return DatabaseConnection.execute_query(
        query, 
        (doctor_id, shift_date), 
        fetch_all=True, 
        fetch_dict=True
    )
    
def get_available_slots(doctor_id, shift_date, slot_duration_minutes=10):
    shift = get_doctor_shift(doctor_id, shift_date)
    if not shift:
        return []
    
    booked = get_booked_appointments(doctor_id, shift_date)
    booked_times = [apt['time'] for apt in booked]
    
    start_time = shift['starttime']
    end_time = shift['endtime']
    
    start = datetime.strptime(str(start_time), '%H:%M:%S')
    end = datetime.strptime(str(end_time), '%H:%M:%S')
    
    available_slots = []
    current = start
    
    while current < end:
        time_str = current.strftime('%H:%M:%S')
        
        is_booked = time_str in booked_times
        
        available_slots.append({
            'time': time_str,
            'display': current.strftime('%I:%M %p'),
            'available': not is_booked,
            'booked_by': None
        })
        
        current += timedelta(minutes=slot_duration_minutes)
    
    return available_slots

def get_doctors_with_availability(shift_date):
    doctors = get_doctors_on_shift(shift_date)
    
    result = []
    for doctor in doctors:
        slots = get_available_slots(doctor['id'], shift_date)
        available_count = sum(1 for slot in slots if slot['available'])
        
        result.append({
            'id': doctor['id'],
            'name': doctor['name'],
            'specialization': doctor['specialization'],
            'shift_start': doctor['shift_start'],
            'shift_end': doctor['shift_end'],
            'available_slots': slots,
            'available_count': available_count
        })
    
    return result

def create_shift(shift_date, start_time, end_time):
    query = """
        INSERT INTO shift (shiftDate, startTime, endTime)
        VALUES (%s, %s, %s)
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (shift_date, start_time, end_time),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def assign_employee_to_shift(employee_id, shift_id):
    query = """
        INSERT INTO employeeShift (employeeID, shiftID)
        VALUES (%s, %s)
        RETURNING shiftID
    """
    DatabaseConnection.execute_query(
        query,
        (employee_id, shift_id),
        fetch_one=True,
        commit=True
    )
    
def update_shift(shift_id, shift_date, start_time, end_time):
    query = """
        UPDATE shift
        SET shift_date = %s, startTime = %s, endTime = %s
        WHERE shiftID = %s
        RETURNING shiftID
    """
    result = DatabaseConnection.execute_query(
        query,
        (shift_date, start_time, end_time, shift_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_shift(shift_id):
    query = "DELETE FROM shift WHERE shiftID = %s RETURNING shiftID"
    result = DatabaseConnection.execute_query(
        query,
        (shift_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def delete_employee_from_shift(employee_id, shift_id):
    query = "DELETE FROM employeeShift WHERE employeeID = %s AND shiftID = %s RETURNING shiftID"
    result = DatabaseConnection.execute_query(
        query,
        (employee_id, shift_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_employee_shifts(employee_id, start_date=None, end_date=None):
    query = """
        SELECT 
            shiftID,
            shiftDate,
            startTime,
            endTime,
            isActive
        FROM shift
        WHERE employeeID = %s
    """
    params = [employee_id]
    
    if start_date:
        query += " AND shiftDate >= %s"
        params.append(start_date)
    
    if end_date:
        query += " AND shiftDate <= %s"
        params.append(end_date)
    
    query += " ORDER BY shiftDate, startTime"
    
    return DatabaseConnection.execute_query(
        query,
        tuple(params),
        fetch_all=True,
        fetch_dict=True
    )
    
def check_time_availability(doctor_id, date, time):
    shift = get_doctor_shift(doctor_id, date)
    if not shift:
        return {'available': False, 'reason': 'Doctor not on shift'}
    
    if time < shift['starttime'] or time >= shift['endtime']:
        return {'available': False, 'reason': 'Outside shift hours'}
    
    booked = get_booked_appointments(doctor_id, date)
    booked_times = [apt['time'] for apt in booked]
    
    if time in booked_times:
        return {'available': False, 'reason': 'Already booked'}
    
    return {'available': True, 'reason': 'Available'}

def update_appointment_status(appointment_id, status):
    """Update appointment status"""
    valid_statuses = ['Scheduled', 'Completed', 'Cancelled', 'No Show', 'Reserved', 'Not Reserved']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}")
    
    query = """
        UPDATE appointment
        SET status = %s
        WHERE appoID = %s
        RETURNING appoID
    """
    result = DatabaseConnection.execute_query(
        query,
        (status, appointment_id),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None