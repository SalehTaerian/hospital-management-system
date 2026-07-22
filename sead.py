import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('en_US')

conn = psycopg2.connect(
    host="127.0.0.1",
    database="hospital_management_system",
    user="postgres",
    password="saleh1385"
)

cur = conn.cursor()

# -------------------------
# Clear DB
# -------------------------
def clear_tables():
    tables = [
        "invoiceItem","allItems","surgeonSpecialization","doctorSpecialization",
        "surgeryTeam","bedInfo","equipInfo","parameterResult","medicineRecord",
        "drugRecord","diseaseRecord","vitalSign","diseaseDiag","medicineDiag",
        "feedBack","transfer","storage","medicineConflict","request","invoice",
        "warning","log","equipment","signType","bed","room","shift",
        "employeeShift","surgery","appointment","admission","officeStaff",
        "nurse","surgeon","doctor","employee","department","hospital",
        "insurance","medicalRecord","patient","icdCode","icdmCode",
        "icdsCode","icdtCode","medicineAllergy","specializationFields",
        "parameterList","followup"
    ]
    for t in tables:
        try:
            cur.execute(f"TRUNCATE TABLE {t} CASCADE;")
        except Exception as e:
            print(f"Error truncating {t}: {e}")
    conn.commit()

# -------------------------
# 1. Hospital (100)
# -------------------------
def seed_hospital():
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO hospital(name, city, province, street, alley, postalCode)
            VALUES (%s,%s,%s,%s,%s,%s) RETURNING hospitalID
        """, (
            fake.company()[:30],
            fake.city()[:20],
            fake.state()[:20],
            fake.street_name()[:20],
            fake.street_name()[:20],
            fake.postcode()[:15]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 2. Department (100)
# -------------------------
def seed_department(hospital_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO department(hospitalID, name, score)
            VALUES (%s,%s,%s) RETURNING departID
        """, (
            random.choice(hospital_ids),
            fake.job()[:30],
            random.randint(1,100)
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 3. Patient (100)
# -------------------------
def seed_patient():
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO patient(
                firstName,lastName,nationalCode,password,
                gender,dateOfBirth,phoneNumber,homeNumber,
                city,province,street,alley,houseCode,createdAt
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING pID
        """, (
            fake.first_name()[:35],
            fake.last_name()[:35],
            str(fake.unique.random_number(digits=10)),
            "123456",
            random.choice(["male","female"]),
            fake.date_of_birth(minimum_age=1, maximum_age=90),
            fake.phone_number()[:13],
            fake.phone_number()[:13],
            fake.city()[:15],
            fake.state()[:15],
            fake.street_name()[:100],
            fake.street_name()[:100],
            str(random.randint(1,999))[:10],
            datetime.now()
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 4. MedicalRecord (100)
# -------------------------
def seed_medical_record(patient_ids):
    ids = []
    for pid in patient_ids:
        cur.execute("""
            INSERT INTO medicalRecord(pID,bloodType,smokingHistory)
            VALUES (%s,%s,%s) RETURNING mID
        """, (
            pid,
            random.choice(["A+","B+","O+","AB+"]),
            random.choice(["none","light","heavy"])
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 5. Insurance (100)
# -------------------------
def seed_insurance(patient_ids):
    for pid in patient_ids:
        cur.execute("""
            INSERT INTO insurance(
                pID,name,coveragePercentage,policyNumber,
                startDate,endDate,createdAt
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            pid,
            fake.company()[:35],
            round(random.uniform(50,100), 2),
            str(fake.unique.random_number(digits=10)),
            datetime.now().date(),
            (datetime.now() + timedelta(days=365)).date(),
            datetime.now()
        ))

# -------------------------
# 6. Employee (100)
# -------------------------
def seed_employee(department_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO employee(
                departID,firstName,lastName,nationalCode,password,
                contractType,hireDate,accessLevel,salary
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING employeeID
        """, (
            random.choice(department_ids),
            fake.first_name()[:50],
            fake.last_name()[:50],
            str(fake.unique.random_number(digits=10)),
            "123456",
            random.choice(["full-time","part-time"]),
            datetime.now(),
            random.choice(["admin","doctor","nurse","staff"])[:50],
            random.randint(5000,20000)
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 7. OfficeStaff (30)
# -------------------------
def seed_office_staff(employee_ids):
    ids = []
    selected = random.sample(employee_ids, min(30, len(employee_ids)))
    for eid in selected:
        cur.execute("""
            INSERT INTO officeStaff(employeeID, role)
            VALUES (%s,%s) RETURNING employeeID
        """, (eid, random.choice(["reception","admin","clerk"])[:30]))
        ids.append(eid)
    return ids

# -------------------------
# 8. Nurse (30)
# -------------------------
def seed_nurse(employee_ids):
    ids = []
    selected = random.sample(employee_ids, min(30, len(employee_ids)))
    for eid in selected:
        cur.execute("""
            INSERT INTO nurse(employeeID, medicalNumber)
            VALUES (%s,%s) RETURNING employeeID
        """, (eid, str(fake.unique.random_number(digits=10))[:20]))
        ids.append(eid)
    return ids

# -------------------------
# 9. Surgeon (20)
# -------------------------
def seed_surgeon(employee_ids):
    ids = []
    selected = random.sample(employee_ids, min(20, len(employee_ids)))
    for eid in selected:
        cur.execute("""
            INSERT INTO surgeon(employeeID, medicalNumber, surgicalField)
            VALUES (%s,%s,%s) RETURNING employeeID
        """, (eid, str(fake.unique.random_number(digits=10))[:20], 
              random.choice(["cardiac","ortho","neuro","general"])[:30]))
        ids.append(eid)
    return ids

# -------------------------
# 10. Doctor (40)
# -------------------------
def seed_doctor(employee_ids):
    ids = []
    selected = random.sample(employee_ids, min(40, len(employee_ids)))
    for eid in selected:
        cur.execute("""
            INSERT INTO doctor(employeeID, medicalNumber, visitCost)
            VALUES (%s,%s,%s) RETURNING employeeID
        """, (eid, str(fake.unique.random_number(digits=10))[:20], 
              random.randint(100,500)))
        ids.append(eid)
    return ids

# -------------------------
# 11. SpecializationFields (10)
# -------------------------
def seed_specialization_fields():
    ids = []
    fields = ["Cardiology","Neurology","Orthopedics","Dermatology","Ophthalmology",
              "Pediatrics","Psychiatry","Radiology","Oncology","Emergency"]
    for field in fields:
        cur.execute("""
            INSERT INTO specializationFields(name)
            VALUES (%s) RETURNING specID
        """, (field[:20],))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 12. DoctorSpecialization (100)
# -------------------------
def seed_doctor_specialization(doctor_ids, spec_ids):
    for doc_id in doctor_ids:
        for spec_id in random.sample(spec_ids, min(3, len(spec_ids))):
            cur.execute("""
                INSERT INTO doctorSpecialization(docID, specID)
                VALUES (%s,%s)
            """, (doc_id, spec_id))

# -------------------------
# 13. SurgeonSpecialization (50)
# -------------------------
def seed_surgeon_specialization(surgeon_ids, spec_ids):
    for surg_id in surgeon_ids:
        for spec_id in random.sample(spec_ids, min(2, len(spec_ids))):
            cur.execute("""
                INSERT INTO surgeonSpecialization(surgeonID, specID)
                VALUES (%s,%s)
            """, (surg_id, spec_id))

# -------------------------
# 14. Shift (100)
# -------------------------
def seed_shift():
    ids = []
    for _ in range(100):
        start = datetime.now() + timedelta(hours=random.randint(0, 720))
        end = start + timedelta(hours=random.randint(4, 12))
        cur.execute("""
            INSERT INTO shift(shiftDate, startTime, endTime)
            VALUES (%s,%s,%s) RETURNING shiftID
        """, (start, start, end))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 15. EmployeeShift (300)
# -------------------------
def seed_employee_shift(employee_ids, shift_ids):
    for eid in employee_ids:
        for _ in range(random.randint(1, 5)):
            cur.execute("""
                INSERT INTO employeeShift(employeeID, shiftID)
                VALUES (%s,%s)
            """, (eid, random.choice(shift_ids)))

# -------------------------
# 16. icdCode (50)
# -------------------------
def seed_icd_code():
    ids = []
    diseases = [
        ("A00", "Cholera"), ("B01", "Chickenpox"), ("C00", "Lip cancer"),
        ("D10", "Benign neoplasm"), ("E10", "Diabetes"), ("F10", "Alcoholism"),
        ("G40", "Epilepsy"), ("I10", "Hypertension"), ("J10", "Influenza"),
        ("K00", "Dental caries"), ("L00", "Impetigo"), ("M00", "Osteomyelitis"),
        ("N00", "Nephritis"), ("O00", "Ectopic pregnancy"), ("P00", "Fetus affected"),
        ("Q00", "Congenital malformation"), ("R00", "Abnormal heartbeat"),
        ("S00", "Head injury"), ("T00", "Burns"), ("U00", "Unknown")
    ]
    for code, name in diseases[:50]:
        cur.execute("""
            INSERT INTO icdCode(code, diseaseName)
            VALUES (%s,%s) RETURNING icdID
        """, (code, name[:50]))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 17. icdmCode (100)
# -------------------------
def seed_icdm_code(icd_ids):
    ids = []
    medicines = ["Aspirin", "Ibuprofen", "Paracetamol", "Amoxicillin", "Ciprofloxacin",
                 "Lisinopril", "Metformin", "Omeprazole", "Simvastatin", "Losartan",
                 "Atorvastatin", "Levothyroxine", "Metoprolol", "Warfarin", "Clopidogrel"]
    for _ in range(100):
        cur.execute("""
            INSERT INTO icdmCode(icdID, medicineName)
            VALUES (%s,%s) RETURNING icdmID
        """, (random.choice(icd_ids), random.choice(medicines)[:20]))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 18. icdsCode (50)
# -------------------------
def seed_icds_code():
    ids = []
    surgeries = ["Appendectomy", "Cholecystectomy", "Hernia repair", "Knee replacement",
                 "Cataract surgery", "Heart bypass", "Tonsillectomy", "Hysterectomy",
                 "Laparoscopy", "Endoscopy"]
    for _ in range(50):
        cur.execute("""
            INSERT INTO icdsCode(surgeryName, cost)
            VALUES (%s,%s) RETURNING icdsID
        """, (random.choice(surgeries)[:20], random.randint(1000, 10000)))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 19. icdtCode (50)
# -------------------------
def seed_icdt_code():
    ids = []
    tests = ["Blood test", "X-ray", "MRI", "CT scan", "Ultrasound", 
             "ECG", "Biopsy", "Urine test", "Stool test", "Spirometry"]
    for _ in range(50):
        cur.execute("""
            INSERT INTO icdtCode(testName, cost)
            VALUES (%s,%s) RETURNING icdtID
        """, (random.choice(tests)[:50], random.randint(100, 2000)))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 20. MedicineAllergy (30)
# -------------------------
def seed_medicine_allergy(medical_record_ids, icdm_ids):
    for mr_id in medical_record_ids[:30]:
        for _ in range(random.randint(1, 3)):
            cur.execute("""
                INSERT INTO medicineAllergy(mID, icdmID)
                VALUES (%s,%s)
            """, (mr_id, random.choice(icdm_ids)))

# -------------------------
# 21. Room (100)
# -------------------------
def seed_room(department_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO room(departID, name, description)
            VALUES (%s,%s,%s) RETURNING roomID
        """, (
            random.choice(department_ids),
            fake.word()[:20],
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 22. Bed (100)
# -------------------------
def seed_bed():
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO bed(cost)
            VALUES (%s) RETURNING bedID
        """, (random.randint(100, 500),))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 23. Admission (100)
# -------------------------
def seed_admission(medical_record_ids, doctor_ids, office_staff_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO admission(mID, doctorID, officeStaffID, cost, createdAt, endTime)
            VALUES (%s,%s,%s,%s,%s,%s) RETURNING admID
        """, (
            random.choice(medical_record_ids),
            random.choice(doctor_ids),
            random.choice(office_staff_ids),
            random.randint(100, 2000),
            datetime.now(),
            datetime.now() + timedelta(days=random.randint(1, 10))
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 24. BedInfo (100)
# -------------------------
def seed_bed_info(bed_ids, room_ids, adm_ids):
    for i, bed_id in enumerate(bed_ids):
        room_id = random.choice(room_ids)
        adm_id = random.choice(adm_ids) if random.random() > 0.5 else None
        start = datetime.now() + timedelta(days=random.randint(0, 30))
        end = start + timedelta(days=random.randint(1, 10))
        cur.execute("""
            INSERT INTO bedInfo(bedID, roomID, asgAdmID, startTimestamp, endTime, status)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            bed_id, room_id, adm_id, start, end,
            random.choice(["available","occupied","reserved"])
        ))

# -------------------------
# 25. Transfer (50)
# -------------------------
def seed_transfer(adm_ids, bed_ids):
    for _ in range(50):
        cur.execute("""
            INSERT INTO transfer(admID, destBedID, transferedAt, cost)
            VALUES (%s,%s,%s,%s)
        """, (
            random.choice(adm_ids),
            random.choice(bed_ids),
            datetime.now(),
            random.randint(50, 300)
        ))

# -------------------------
# 26. SignType (5)
# -------------------------
def seed_sign_type():
    ids = []
    signs = ["Monitor", "Pump", "Ventilator", "Defibrillator", "Infusion"]
    for sign in signs:
        cur.execute("""
            INSERT INTO signType(signName)
            VALUES (%s) RETURNING sTypeID
        """, (sign[:20],))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 27. Equipment (100)
# -------------------------
def seed_equipment(sign_type_ids):
    ids = []
    equip_names = ["Monitor", "Pump", "Ventilator", "Defibrillator", "Infusion"]
    for _ in range(100):
        cur.execute("""
            INSERT INTO equipment(sTypeID, name, MACAddress, description)
            VALUES (%s,%s,%s,%s) RETURNING equipID
        """, (
            random.choice(sign_type_ids),
            random.choice(equip_names)[:30],
            fake.mac_address()[:30],
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 28. EquipInfo (100)
# -------------------------
def seed_equip_info(equip_ids, room_ids, adm_ids):
    for equip_id in equip_ids:
        start = datetime.now() + timedelta(days=random.randint(0, 30))
        end = start + timedelta(days=random.randint(1, 10))
        cur.execute("""
            INSERT INTO equipInfo(equipID, roomID, asgAdmID, startTimestamp, endTime, status)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            equip_id,
            random.choice(room_ids),
            random.choice(adm_ids),
            start, end,
            random.choice(["active","inactive","maintenance"])
        ))

# -------------------------
# 29. ParameterList (10)
# -------------------------
def seed_parameter_list():
    ids = []
    params = [
        ("Heart Rate", 60, 100, 72.5),
        ("Blood Pressure", 90, 140, 120.0),
        ("Temperature", 36.5, 37.5, 37.0),
        ("Oxygen", 95, 100, 98.0),
        ("Glucose", 70, 140, 100.0),
        ("Respiratory", 12, 20, 16.0),
        ("BMI", 18.5, 30, 24.0),
        ("Cholesterol", 125, 200, 160.0),
        ("Potassium", 3.5, 5.0, 4.2),
        ("Sodium", 135, 145, 140.0)
    ]
    for name, min_val, max_val, avg in params:
        cur.execute("""
            INSERT INTO parameterList(parameterName, min, max, average)
            VALUES (%s,%s,%s,%s) RETURNING parameterID
        """, (name[:25], min_val, max_val, avg))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 30. Log (100)
# -------------------------
def seed_log(equip_ids, param_ids, adm_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO log(equipID, parameterID, asgAdmID, parameterValue, createdAt)
            VALUES (%s,%s,%s,%s,%s) RETURNING logID
        """, (
            random.choice(equip_ids),
            random.choice(param_ids),
            random.choice(adm_ids),
            round(random.uniform(50, 150), 2),
            datetime.now()
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 31. Warning (50)
# -------------------------
def seed_warning(log_ids):
    for log_id in log_ids[:50]:
        cur.execute("""
            INSERT INTO warning(logID, importance, occuredTime, checkedStatus, checkedTime)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            log_id,
            random.choice(["low","medium","high","critical"]),
            datetime.now(),
            random.choice(["pending","checked","resolved"]),
            datetime.now() if random.random() > 0.5 else None
        ))

# -------------------------
# 32. Surgery (100)
# -------------------------
def seed_surgery(icds_ids, patient_ids, surgeon_ids, room_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO surgery(surgeryCode, pID, chiefSurgeonId, roomID, 
                              surgeryDate, status, finalReport)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING surgeryID
        """, (
            random.choice(icds_ids),
            random.choice(patient_ids),
            random.choice(surgeon_ids),
            random.choice(room_ids),
            datetime.now() + timedelta(days=random.randint(1, 30)),
            random.choice(["scheduled","in progress","completed","cancelled"]),
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 33. SurgeryTeam (100)
# -------------------------
def seed_surgery_team(surgery_ids, surgeon_ids):
    for surg_id in surgery_ids:
        for _ in range(random.randint(1, 3)):
            cur.execute("""
                INSERT INTO surgeryTeam(surgeryID, surgeonID)
                VALUES (%s,%s)
            """, (surg_id, random.choice(surgeon_ids)))

# -------------------------
# 34. Followup (100)
# -------------------------
def seed_followup():
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO followup(progress)
            VALUES (%s) RETURNING followID
        """, (random.randint(0, 100),))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 35. Appointment (100)
# -------------------------
def seed_appointment(medical_record_ids, doctor_ids, office_staff_ids, followup_ids):
    ids = []
    for _ in range(100):
        follow_id = random.choice(followup_ids) if random.random() > 0.3 else None
        cur.execute("""
            INSERT INTO appointment(
                mID, doctorID, staffID, followID, date, time,
                status, isOnlineReserved, reserveTime, enterTime
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING appoID
        """, (
            random.choice(medical_record_ids),
            random.choice(doctor_ids),
            random.choice(office_staff_ids) if random.random() > 0.3 else None,
            follow_id,
            datetime.now().date(),
            datetime.now().time(),
            random.choice(["pending","confirmed","completed","cancelled"]),
            random.choice([True, False]),
            datetime.now(),
            datetime.now()
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 36. DiseaseDiag (100)
# -------------------------
def seed_disease_diag(appo_ids, icd_ids):
    ids = []
    for appo_id in appo_ids:
        cur.execute("""
            INSERT INTO diseaseDiag(appoID, icdID, description)
            VALUES (%s,%s,%s) RETURNING disDiagID
        """, (
            appo_id,
            random.choice(icd_ids),
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 37. MedicineDiag (100)
# -------------------------
def seed_medicine_diag(dis_diag_ids, icdm_ids):
    ids = []
    for dis_id in dis_diag_ids:
        cur.execute("""
            INSERT INTO medicineDiag(disDiagID, icdmID, description)
            VALUES (%s,%s,%s) RETURNING medDiagID
        """, (
            dis_id,
            random.choice(icdm_ids),
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 38. Feedback (50)
# -------------------------
def seed_feedback(med_diag_ids):
    for med_id in med_diag_ids[:50]:
        cur.execute("""
            INSERT INTO feedBack(medDiagID, effectPercentage)
            VALUES (%s,%s)
        """, (med_id, random.randint(0, 100)))

# -------------------------
# 39. VitalSign (100)
# -------------------------
def seed_vital_sign(appo_ids, param_ids):
    for appo_id in appo_ids:
        for _ in range(random.randint(1, 3)):
            cur.execute("""
                INSERT INTO vitalSign(appoID, parameterID, parameterValue)
                VALUES (%s,%s,%s)
            """, (
                appo_id,
                random.choice(param_ids),
                round(random.uniform(50, 150), 2)
            ))

# -------------------------
# 40. DiseaseRecord (50)
# -------------------------
def seed_disease_record(medical_record_ids, icd_ids):
    for mr_id in medical_record_ids[:50]:
        cur.execute("""
            INSERT INTO diseaseRecord(mID, icdID, description)
            VALUES (%s,%s,%s)
        """, (
            mr_id,
            random.choice(icd_ids),
            fake.text()[:200]
        ))

# -------------------------
# 41. DrugRecord (50)
# -------------------------
def seed_drug_record(medical_record_ids):
    for mr_id in medical_record_ids[:50]:
        cur.execute("""
            INSERT INTO drugRecord(mID, description)
            VALUES (%s,%s)
        """, (mr_id, fake.text()[:200]))

# -------------------------
# 42. MedicineRecord (100)
# -------------------------
def seed_medicine_record(medical_record_ids, icdm_ids):
    for mr_id in medical_record_ids:
        for _ in range(random.randint(1, 3)):
            cur.execute("""
                INSERT INTO medicineRecord(mID, icdmID, description)
                VALUES (%s,%s,%s)
            """, (
                mr_id,
                random.choice(icdm_ids),
                fake.text()[:200]
            ))

# -------------------------
# 43. Storage (50)
# -------------------------
def seed_storage(department_ids, icdm_ids):
    for _ in range(50):
        cur.execute("""
            INSERT INTO storage(departID, medID, name, type, enterDate, exitDate, cost)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            random.choice(department_ids),
            random.choice(icdm_ids),
            fake.word()[:30],
            random.choice(["tablet","capsule","syrup","injection"])[:20],
            datetime.now(),
            datetime.now() + timedelta(days=random.randint(1, 30)),
            random.randint(10, 500)
        ))

# -------------------------
# 44. MedicineConflict (30)
# -------------------------
def seed_medicine_conflict(department_ids, icdm_ids):
    for _ in range(30):
        cur.execute("""
            INSERT INTO medicineConflict(departID, icdm1ID, icdm2ID)
            VALUES (%s,%s,%s)
        """, (
            random.choice(department_ids),
            random.choice(icdm_ids),
            random.choice(icdm_ids)
        ))

# -------------------------
# 45. Request (100)
# -------------------------
def seed_request(medical_record_ids, doctor_ids, department_ids, icdm_ids, icdt_ids):
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO request(
                mID, doctorID, departID, medID, testID,
                name, description, status, isPatientConfirmed,
                cost, createdAt
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING reqID
        """, (
            random.choice(medical_record_ids),
            random.choice(doctor_ids),
            random.choice(department_ids),
            random.choice(icdm_ids) if random.random() > 0.5 else None,
            random.choice(icdt_ids) if random.random() > 0.5 else None,
            fake.word()[:50],
            fake.text()[:200],
            random.choice(["pending","approved","rejected","completed"]),
            random.choice([True, False]),
            random.randint(50, 1000),
            datetime.now()
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 46. ParameterResult (100)
# -------------------------
def seed_parameter_result(req_ids, param_ids):
    for req_id in req_ids:
        for _ in range(random.randint(1, 3)):
            cur.execute("""
                INSERT INTO parameterResult(reqID, parameterID, parameterValue)
                VALUES (%s,%s,%s)
            """, (
                req_id,
                random.choice(param_ids),
                random.randint(0, 200)
            ))

# -------------------------
# 47. Invoice (100)
# -------------------------
def seed_invoice(patient_ids, appo_ids, req_ids, surgery_ids, adm_ids):
    ids = []
    for _ in range(100):
        total = random.randint(100, 5000)
        insurance_share = total * random.uniform(0.3, 0.7)
        cur.execute("""
            INSERT INTO invoice(
                pID, appoID, reqID, surgeryID, admID,
                issueDate, totalAmount, insuranceShare, patientShare, isPaid
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING invID
        """, (
            random.choice(patient_ids),
            random.choice(appo_ids) if random.random() > 0.5 else None,
            random.choice(req_ids) if random.random() > 0.5 else None,
            random.choice(surgery_ids) if random.random() > 0.5 else None,
            random.choice(adm_ids) if random.random() > 0.5 else None,
            datetime.now(),
            total,
            round(insurance_share, 2),
            round(total - insurance_share, 2),
            random.choice([True, False])
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 48. AllItems (100)
# -------------------------
def seed_all_items():
    ids = []
    for _ in range(100):
        cur.execute("""
            INSERT INTO allItems(itemType, description)
            VALUES (%s,%s) RETURNING itemID
        """, (
            random.choice(["service","medicine","equipment","test","surgery"]),
            fake.text()[:200]
        ))
        ids.append(cur.fetchone()[0])
    return ids

# -------------------------
# 49. InvoiceItem (100)
# -------------------------
def seed_invoice_item(invoice_ids, all_items_ids):
    for inv_id in invoice_ids:
        for _ in range(random.randint(1, 5)):
            cur.execute("""
                INSERT INTO invoiceItem(itemID, invoiceID, description)
                VALUES (%s,%s,%s)
            """, (
                inv_id,
                random.choice(all_items_ids),
                fake.text()[:200]
            ))

# -------------------------
# MAIN
# -------------------------
def main():
    print("Clearing tables...")
    clear_tables()
    
    print("1. Seeding hospitals...")
    hospital_ids = seed_hospital()
    
    print("2. Seeding departments...")
    department_ids = seed_department(hospital_ids)
    
    print("3. Seeding patients...")
    patient_ids = seed_patient()
    
    print("4. Seeding medical records...")
    medical_record_ids = seed_medical_record(patient_ids)
    
    print("5. Seeding insurance...")
    seed_insurance(patient_ids)
    
    print("6. Seeding employees...")
    employee_ids = seed_employee(department_ids)
    
    print("7. Seeding office staff...")
    office_staff_ids = seed_office_staff(employee_ids)
    
    print("8. Seeding nurses...")
    nurse_ids = seed_nurse(employee_ids)
    
    print("9. Seeding surgeons...")
    surgeon_ids = seed_surgeon(employee_ids)
    
    print("10. Seeding doctors...")
    doctor_ids = seed_doctor(employee_ids)
    
    print("11. Seeding specialization fields...")
    spec_ids = seed_specialization_fields()
    
    print("12. Seeding doctor specializations...")
    seed_doctor_specialization(doctor_ids, spec_ids)
    
    print("13. Seeding surgeon specializations...")
    seed_surgeon_specialization(surgeon_ids, spec_ids)
    
    print("14. Seeding shifts...")
    shift_ids = seed_shift()
    
    print("15. Seeding employee shifts...")
    seed_employee_shift(employee_ids, shift_ids)
    
    print("16. Seeding icd codes...")
    icd_ids = seed_icd_code()
    
    print("17. Seeding icdm codes...")
    icdm_ids = seed_icdm_code(icd_ids)
    
    print("18. Seeding icds codes...")
    icds_ids = seed_icds_code()
    
    print("19. Seeding icdt codes...")
    icdt_ids = seed_icdt_code()
    
    print("20. Seeding medicine allergies...")
    seed_medicine_allergy(medical_record_ids, icdm_ids)
    
    print("21. Seeding rooms...")
    room_ids = seed_room(department_ids)
    
    print("22. Seeding beds...")
    bed_ids = seed_bed()
    
    print("23. Seeding admissions...")
    adm_ids = seed_admission(medical_record_ids, doctor_ids, office_staff_ids)
    
    print("24. Seeding bed info...")
    seed_bed_info(bed_ids, room_ids, adm_ids)
    
    print("25. Seeding transfers...")
    seed_transfer(adm_ids, bed_ids)
    
    print("26. Seeding sign types...")
    sign_type_ids = seed_sign_type()
    
    print("27. Seeding equipment...")
    equip_ids = seed_equipment(sign_type_ids)
    
    print("28. Seeding equip info...")
    seed_equip_info(equip_ids, room_ids, adm_ids)
    
    print("29. Seeding parameter list...")
    param_ids = seed_parameter_list()
    
    print("30. Seeding logs...")
    log_ids = seed_log(equip_ids, param_ids, adm_ids)
    
    print("31. Seeding warnings...")
    seed_warning(log_ids)
    
    print("32. Seeding surgeries...")
    surgery_ids = seed_surgery(icds_ids, patient_ids, surgeon_ids, room_ids)
    
    print("33. Seeding surgery teams...")
    seed_surgery_team(surgery_ids, surgeon_ids)
    
    print("34. Seeding followups...")
    followup_ids = seed_followup()
    
    print("35. Seeding appointments...")
    appo_ids = seed_appointment(medical_record_ids, doctor_ids, office_staff_ids, followup_ids)
    
    print("36. Seeding disease diag...")
    dis_diag_ids = seed_disease_diag(appo_ids, icd_ids)
    
    print("37. Seeding medicine diag...")
    med_diag_ids = seed_medicine_diag(dis_diag_ids, icdm_ids)
    
    print("38. Seeding feedback...")
    seed_feedback(med_diag_ids)
    
    print("39. Seeding vital signs...")
    seed_vital_sign(appo_ids, param_ids)
    
    print("40. Seeding disease records...")
    seed_disease_record(medical_record_ids, icd_ids)
    
    print("41. Seeding drug records...")
    seed_drug_record(medical_record_ids)
    
    print("42. Seeding medicine records...")
    seed_medicine_record(medical_record_ids, icdm_ids)
    
    print("43. Seeding storage...")
    seed_storage(department_ids, icdm_ids)
    
    print("44. Seeding medicine conflicts...")
    seed_medicine_conflict(department_ids, icdm_ids)
    
    print("45. Seeding requests...")
    req_ids = seed_request(medical_record_ids, doctor_ids, department_ids, icdm_ids, icdt_ids)
    
    print("46. Seeding parameter results...")
    seed_parameter_result(req_ids, param_ids)
    
    print("47. Seeding invoices...")
    invoice_ids = seed_invoice(patient_ids, appo_ids, req_ids, surgery_ids, adm_ids)
    
    print("48. Seeding all items...")
    all_items_ids = seed_all_items()
    
    print("49. Seeding invoice items...")
    seed_invoice_item(invoice_ids, all_items_ids)
    
    conn.commit()
    print("✅ All 49 tables seeded successfully!")

if __name__ == "__main__":
    main()