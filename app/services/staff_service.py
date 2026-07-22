from app.database.queries.staff_queries import *
from datetime import datetime


def search_patients_service(search_term):
    if not search_term or len(search_term) < 2:
        return []
    return search_patients(search_term)


def get_patient_basic_info_service(patient_id):
    patient = get_patient_basic_info(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} not found")

    appointments = get_appointments_by_patient(patient_id)

    return {
        "id": patient.get("pid"),
        "firstName": patient.get("firstname"),
        "lastName": patient.get("lastname"),
        "nationalCode": patient.get("nationalcode"),
        "gender": patient.get("gender"),
        "dateOfBirth": patient.get("dateofbirth"),
        "age": patient.get("age"),
        "phone": patient.get("phonenumber"),
        "city": patient.get("city"),
        "province": patient.get("province"),
        "bloodType": patient.get("bloodtype"),
        "smokingHistory": patient.get("smokinghistory"),
        "appointments": [
            {
                "id": apt["appoid"],
                "date": apt["date"],
                "time": apt["time"],
                "status": apt["status"],
                "doctor": apt["doctor_name"],
                # 'specialization': apt['specialization']
            }
            for apt in appointments
        ],
    }


def get_patient_with_admission_info_service(patient_id):
    patient = get_patient_with_admission_info(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID {patient_id} not found")

    return {
        "id": patient.get("pid"),
        "firstName": patient.get("firstname"),
        "lastName": patient.get("lastname"),
        "nationalCode": patient.get("nationalcode"),
        "gender": patient.get("gender"),
        "dateOfBirth": patient.get("dateofbirth"),
        "age": patient.get("age"),
        "phoneNumber": patient.get("phonenumber"),
        "homeNumber": patient.get("homenumber"),
        "city": patient.get("city"),
        "province": patient.get("province"),
        "street": patient.get("street"),
        "alley": patient.get("alley"),
        "houseCode": patient.get("housecode"),
        "bloodType": patient.get("bloodtype"),
        "smokingHistory": patient.get("smokinghistory"),
        "admID": patient.get("admid"),
        "cost": patient.get("cost"),
        "admission_date": patient.get("admission_date"),
        "bedID": patient.get("bedid"),
        "bed_status": patient.get("bed_status"),
        "room_name": patient.get("room_name"),
        "department_name": patient.get("department_name"),
        "bed_cost": patient.get("bed_cost"),
    }


def get_doctors_service():
    return get_doctors_list()


def get_doctors_on_shift_service(shift_date):
    return get_doctors_on_shift(shift_date)


def get_available_slots_service(doctor_id, shift_date):
    return get_available_slots(doctor_id, shift_date)


def get_doctors_with_availability_service(shift_date):
    return get_doctors_with_availability(shift_date)


def check_time_availability_service(doctor_id, date, time):
    return check_time_availability(doctor_id, date, time)


def create_appointment_service(data):
    if not data.get("patient_id"):
        raise ValueError("Patient is required")
    if not data.get("doctor_id"):
        raise ValueError("Doctor is required")
    if not data.get("date"):
        raise ValueError("Date is required")
    if not data.get("time"):
        raise ValueError("Time is required")

    try:
        appointment_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if appointment_date < datetime.now().date():
            raise ValueError("Cannot book appointment in the past")
    except ValueError:
        raise ValueError("Invalid date format")

    return create_appointment(data)


def get_today_appointments_service():
    return get_today_appointments()


def update_appointment_status_service(appointment_id, status):
    valid_statuses = [
        "Scheduled",
        "Completed",
        "Cancelled",
        "No Show",
        "Reserved",
        "Not Reserved",
    ]
    if status not in valid_statuses:
        raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

    return update_appointment_status(appointment_id, status)


def get_surgeons_service():
    return get_surgeons_list()


def get_surgery_codes_service():
    return get_surgery_codes()


def get_rooms_service():
    return get_rooms_list()


def get_available_rooms_service(surgery_date):
    return get_available_rooms(surgery_date)


def create_surgery_service(data):
    if not data.get("patient_id"):
        raise ValueError("Patient is required")
    if not data.get("surgeon_id"):
        raise ValueError("Surgeon is required")
    if not data.get("surgery_code"):
        raise ValueError("Surgery type is required")
    if not data.get("room_id"):
        raise ValueError("Room is required")
    if not data.get("surgery_date"):
        raise ValueError("Surgery date is required")

    return create_surgery(data)


def get_today_surgeries_service():
    return get_today_surgeries()


def create_shift_service(shift_date, start_time, end_time):
    if not shift_date:
        raise ValueError("Shift date is required")
    if not start_time:
        raise ValueError("Start time is required")
    if not end_time:
        raise ValueError("End time is required")

    if start_time >= end_time:
        raise ValueError("Start time must be before end time")

    return create_shift(shift_date, start_time, end_time)


def assign_employee_to_shift_service(employee_id, shift_id):
    if not employee_id:
        raise ValueError("Employee ID is required")
    if not shift_id:
        raise ValueError("Shift ID is required")

    return assign_employee_to_shift(employee_id, shift_id)


def get_employee_shifts_service(employee_id, start_date=None, end_date=None):
    return get_employee_shifts(employee_id, start_date, end_date)


def get_dashboard_stats_service():
    return get_dashboard_stats()


def get_occupied_beds_by_department():
    return get_occupied_beds()


def working_pressure_service():
    return working_pressure()


def avg_admission_time_service():
    return avg_admission_time()


def visits_per_hour_service():
    return visits_per_hour()


def visits_per_day_service():
    return visits_per_day()

def get_most_diseases_service():
    return get_most_diseases()

def get_most_used_medicine_service():
    return get_most_used_medicine()