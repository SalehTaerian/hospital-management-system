# seed_database.py
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import sys

class DatabaseSeeder:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="127.0.0.1",
            database="hospital_management_system",
            user="postgres",
            password="saleh1385"
        )
        self.cur = self.conn.cursor()
        self.fake = Faker('en_US')
    
    def is_seeded(self):
        tables = ['patient', 'doctor', 'nurse', 'surgeon']
        for table in tables:
            try:
                self.cur.execute(f"SELECT COUNT(*) FROM {table};")
                count = self.cur.fetchone()[0]
                if count > 0:
                    print(f"Table '{table}' has {count} records.")
                    return True
            except Exception as e:
                print(f"Error checking table {table}: {e}")
        return False
    
    def clear_all_data(self):
        tables = ['patient', 'medicalRecord', 'insurance', 'hospital',
                  'department', 'employee', 'doctor', 'surgeon', 'nurse',
                  'officeStaff', 'admission', 'appointment', 'surgery',
                  'shift', 'room', 'bed', 'equipment', 'log', 'warning',
                  'invoice', 'request', 'medicineConflict', 'storage',
                  'transfer', 'receptionReserve', 'medicineDiag', 'diseaseDiag',
                  'vitalSign', 'diseaseRecord', 'drugRecord', 'medicineRecord',
                  'parameterResult', 'equipInfo', 'bedInfo', 'surgeryTeam',
                  'doctorSpecialization', 'surgeonSpecialization', 'allItems',
                  'invoiceItem']
        
        print("Clearing all existing data...")
        for table in tables:
            try:
                self.cur.execute(f"TRUNCATE TABLE {table} CASCADE;")
                print(f"    Cleared {table}")
            except Exception as e:
                print(f"Could not clear {table}: {e}")
        self.conn.commit()
        print("All data cleared!")
    
    def generate_national_id(self):
        return str(random.randint(1000000000, 9999999999))
    
    def generate_phone_number(self):
        return str(random.randint(1000000000, 9999999999))
    
    def generate_house_code(self):
        return str(random.randint(1, 9999))
    
    def generate_postal_code(self):
        return str(random.randint(1000000000, 9999999999))[:10]
    
    def truncate_string(self, text, max_length):
        if text is None:
            return "unknown"
        if len(text) > max_length:
            return text[:max_length]
        return text
    
    def seed(self, force=False):
        if not force and self.is_seeded():
            print("\nDatabase already has data!")
            print("Use --force to clear and reseed:")
            print("python seed_database.py --force")
            return False
        
        if force:
            self.clear_all_data()
        
        print("\nStarting database seeding...")
        
        patients = []
        for i in range(100):
            firstName = self.truncate_string(self.fake.first_name(), 10)
            lastName = self.truncate_string(self.fake.last_name(), 10)
            nationalCode = self.generate_national_id()
            password = self.truncate_string(self.fake.password(length=8), 10)
            gender = random.choice(['Male', 'Female'])
            dateOfBirth = self.fake.date_of_birth(minimum_age=18, maximum_age=90)
            phoneNumber = self.generate_phone_number()
            homeNumber = self.generate_phone_number()
            city = self.truncate_string(self.fake.city(), 10)
            province = self.truncate_string(self.fake.state(), 10)
            street = self.truncate_string(self.fake.street_name(), 10)
            alley = self.truncate_string(self.fake.street_name(), 10)
            houseCode = self.generate_house_code()
            
            self.cur.execute("""
                INSERT INTO patient (firstName, lastName, nationalCode, password, gender,
                                    dateOfBirth, phoneNumber, homeNumber, city, province,
                                    street, alley, houseCode)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING pID;
            """, (firstName, lastName, nationalCode, password, gender, dateOfBirth,
                  phoneNumber, homeNumber, city, province, street, alley, houseCode))
            
            pID = self.cur.fetchone()[0]
            patients.append(pID)
        self.conn.commit()
        print("100 patients inserted")
        
        medical_records = []
        for pID in patients:
            bloodType = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
            smokingHistory = self.truncate_string(random.choice(['Never', 'Former', 'Current', 'Passive']), 10)
            
            self.cur.execute("""
                INSERT INTO medicalRecord (pID, bloodType, smokingHistory)
                VALUES (%s, %s, %s)
                RETURNING mID;
            """, (pID, bloodType, smokingHistory))
            
            mID = self.cur.fetchone()[0]
            medical_records.append((pID, mID))
        self.conn.commit()
        print("100 medical records inserted")
        
        for pID in patients:
            name = self.truncate_string(random.choice(['Health', 'Atieh', 'Asia', 'Dana', 'Pasargad']), 10)
            coveragePercentage = round(random.uniform(60, 90), 2)
            policyNumber = str(random.randint(1000000000, 9999999999))
            startDate = self.fake.date_between(start_date='-5y', end_date='-1y')
            endDate = startDate + timedelta(days=random.randint(365, 730))
            
            self.cur.execute("""
                INSERT INTO insurance (pID, name, coveragePercentage, policyNumber, startDate, endDate)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (pID, name, coveragePercentage, policyNumber, startDate, endDate))
        self.conn.commit()
        print("100 insurance records inserted")
        
        hospitals = []
        for i in range(10):
            name = self.truncate_string(self.fake.company(), 10)
            city = self.truncate_string(self.fake.city(), 10)
            province = self.truncate_string(self.fake.state(), 10)
            street = self.truncate_string(self.fake.street_name(), 10)
            alley = self.truncate_string(self.fake.street_name(), 10)
            postalCode = self.generate_postal_code()
            
            self.cur.execute("""
                INSERT INTO hospital (name, city, province, street, alley, postalCode)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING hospitalID;
            """, (name, city, province, street, alley, postalCode))
            
            hospitalID = self.cur.fetchone()[0]
            hospitals.append(hospitalID)
        self.conn.commit()
        print("10 hospitals inserted")
        
        departments = []
        dept_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Internal', 'Surgery',
                      'Pediatrics', 'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT']
        for hospitalID in hospitals:
            for dept_name in random.sample(dept_names, random.randint(3, 5)):
                dept_name = self.truncate_string(dept_name, 10)
                score = random.randint(1, 100)
                self.cur.execute("""
                    INSERT INTO department (hospitalID, name, score)
                    VALUES (%s, %s, %s)
                    RETURNING departID;
                """, (hospitalID, dept_name, score))
                
                departID = self.cur.fetchone()[0]
                departments.append(departID)
        self.conn.commit()
        print(f"{len(departments)} departments inserted")
        
        employees = []
        employee_types = []
        for departID in departments:
            num_employees = random.randint(3, 8)
            for _ in range(num_employees):
                firstName = self.truncate_string(self.fake.first_name(), 10)
                lastName = self.truncate_string(self.fake.last_name(), 10)
                nationalCode = self.generate_national_id()
                password = self.truncate_string(self.fake.password(length=8), 10)
                contractType = self.truncate_string(random.choice(['Permanent', 'Temporary', 'Contract']), 10)
                hireDate = self.fake.date_between(start_date='-10y', end_date='today')
                accessLevel = self.truncate_string(random.choice(['Admin', 'Doctor', 'Nurse', 'Staff', 'Surgeon']), 10)
                salary = random.randint(20000000, 100000000)
                
                self.cur.execute("""
                    INSERT INTO employee (departID, firstName, lastName, nationalCode, password,
                                         contractType, hireDate, accessLevel, salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING employeeID;
                """, (departID, firstName, lastName, nationalCode, password,
                      contractType, hireDate, accessLevel, salary))
                
                employeeID = self.cur.fetchone()[0]
                employees.append(employeeID)
                employee_types.append((employeeID, accessLevel))
        self.conn.commit()
        print(f"{len(employees)} employees inserted")
        
        specializations = []
        spec_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Internal', 'Pediatrics',
                      'Gynecology', 'Dermatology', 'Ophthalmology', 'ENT', 'General']
        for spec_name in spec_names:
            spec_name = self.truncate_string(spec_name, 10)
            self.cur.execute("""
                INSERT INTO specializationFields (name)
                VALUES (%s)
                RETURNING specID;
            """, (spec_name,))
            specID = self.cur.fetchone()[0]
            specializations.append(specID)
        self.conn.commit()
        print("10 specializations inserted")
        
        doctors = []
        for empID, accessLevel in employee_types:
            if accessLevel == 'Doctor':
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='?????-######'), 10)
                visitCost = random.randint(50000, 200000)
                self.cur.execute("""
                    INSERT INTO doctor (employeeID, medicalNumber, visitCost)
                    VALUES (%s, %s, %s);
                """, (empID, medicalNumber, visitCost))
                doctors.append(empID)
                for specID in random.sample(specializations, random.randint(1, 3)):
                    self.cur.execute("""
                        INSERT INTO doctorSpecialization (docID, specID)
                        VALUES (%s, %s);
                    """, (empID, specID))
        self.conn.commit()
        print(f"{len(doctors)} doctors inserted")
        
        surgeons = []
        for empID, accessLevel in employee_types:
            if accessLevel == 'Surgeon':
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='?????-######'), 10)
                surgicalField = self.truncate_string(random.choice(['Cardiac', 'Orthopedic', 'Neuro', 'General', 'Plastic']), 10)
                self.cur.execute("""
                    INSERT INTO surgeon (employeeID, medicalNumber, surgicalField)
                    VALUES (%s, %s, %s);
                """, (empID, medicalNumber, surgicalField))
                surgeons.append(empID)
                for specID in random.sample(specializations, random.randint(1, 2)):
                    self.cur.execute("""
                        INSERT INTO surgeonSpecialization (surgeonID, specID)
                        VALUES (%s, %s);
                    """, (empID, specID))
        self.conn.commit()
        print(f"{len(surgeons)} surgeons inserted")
        
        nurses = []
        for empID, accessLevel in employee_types:
            if accessLevel == 'Nurse':
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='NUR-######'), 10)
                self.cur.execute("""
                    INSERT INTO nurse (employeeID, medicalNumber)
                    VALUES (%s, %s);
                """, (empID, medicalNumber))
                nurses.append(empID)
        self.conn.commit()
        print(f"{len(nurses)} nurses inserted")
        
        office_staffs = []
        for empID, accessLevel in employee_types:
            if accessLevel == 'Staff':
                role = self.truncate_string(random.choice(['Reception', 'Secretary', 'Admin', 'Billing']), 10)
                self.cur.execute("""
                    INSERT INTO officeStaff (employeeID, role)
                    VALUES (%s, %s);
                """, (empID, role))
                office_staffs.append(empID)
        self.conn.commit()
        print(f"{len(office_staffs)} office staff inserted")
        
        shifts = []
        for i in range(30):
            shift_date = self.fake.date_between(start_date='-1y', end_date='+1y')
            start_time = datetime.combine(shift_date, datetime.min.time()) + timedelta(hours=random.randint(8, 20))
            end_time = start_time + timedelta(hours=random.randint(8, 12))
            
            self.cur.execute("""
                INSERT INTO shift (shiftDate, startTime, endTime)
                VALUES (%s, %s, %s)
                RETURNING shiftID;
            """, (shift_date, start_time, end_time))
            shiftID = self.cur.fetchone()[0]
            shifts.append(shiftID)
        self.conn.commit()
        print("30 shifts inserted")
        
        for empID in employees:
            shift_count = random.randint(5, 15)
            for _ in range(shift_count):
                shiftID = random.choice(shifts)
                self.cur.execute("""
                    INSERT INTO employeeShift (employeeID, shiftID)
                    VALUES (%s, %s);
                """, (empID, shiftID))
        self.conn.commit()
        print("Employee shifts inserted")
        
        parameters = []
        param_names = ['Cold', 'Fever', 'BP', 'HR', 'O2', 'Sugar', 'Chol', 'Trig']
        for param_name in param_names:
            param_name = self.truncate_string(param_name, 10)
            min_val = round(random.uniform(1, 50), 2)
            max_val = round(min_val + random.uniform(20, 100), 2)
            avg_val = round((min_val + max_val) / 2, 2)
            
            self.cur.execute("""
                INSERT INTO parameterList (parameterName, min, max, average)
                VALUES (%s, %s, %s, %s)
                RETURNING parameterID;
            """, (param_name, min_val, max_val, avg_val))
            paramID = self.cur.fetchone()[0]
            parameters.append(paramID)
        self.conn.commit()
        print("8 parameters inserted")
        
        icd_codes = []
        diseases = ['Flu', 'Cold', 'Hypertension', 'Diabetes', 'Asthma', 'Bronchitis', 'Pneumonia']
        for disease in diseases:
            disease = self.truncate_string(disease, 10)
            code = self.truncate_string(self.fake.unique.bothify(text='??-###'), 10)
            self.cur.execute("""
                INSERT INTO icdCode (code, diseaseName)
                VALUES (%s, %s)
                RETURNING icdID;
            """, (code, disease))
            icdID = self.cur.fetchone()[0]
            icd_codes.append(icdID)
        self.conn.commit()
        print("7 ICD codes inserted")
        
        icdm_codes = []
        medicines = ['Acetaminophen', 'Ibuprofen', 'Aspirin', 'Penicillin', 'Amoxicillin', 'Losartan', 'Metformin']
        for icdID in icd_codes:
            for medicine in random.sample(medicines, random.randint(1, 3)):
                medicine = self.truncate_string(medicine, 10)
                self.cur.execute("""
                    INSERT INTO icdmCode (icdID, medicineName)
                    VALUES (%s, %s)
                    RETURNING icdmID;
                """, (icdID, medicine))
                icdmID = self.cur.fetchone()[0]
                icdm_codes.append(icdmID)
        self.conn.commit()
        print(f"{len(icdm_codes)} ICDM codes inserted")
        
        icds_codes = []
        surgeries = ['Bypass', 'Knee', 'Spinal', 'Appendectomy', 'Gallbladder']
        for surgery_name in surgeries:
            surgery_name = self.truncate_string(surgery_name, 10)
            cost = random.randint(5000000, 50000000)
            self.cur.execute("""
                INSERT INTO icdsCode (surgeryName, cost)
                VALUES (%s, %s)
                RETURNING icdsID;
            """, (surgery_name, cost))
            icdsID = self.cur.fetchone()[0]
            icds_codes.append(icdsID)
        self.conn.commit()
        print("5 ICDS codes inserted")
        
        icdt_codes = []
        tests = ['Blood', 'Urine', 'CT', 'MRI', 'Echo', 'ECG']
        for test_name in tests:
            test_name = self.truncate_string(test_name, 10)
            cost = random.randint(200000, 5000000)
            self.cur.execute("""
                INSERT INTO icdtCode (testName, cost)
                VALUES (%s, %s)
                RETURNING icdtID;
            """, (test_name, cost))
            icdtID = self.cur.fetchone()[0]
            icdt_codes.append(icdtID)
        self.conn.commit()
        print("6 ICDT codes inserted")
        
        rooms = []
        for departID in departments:
            num_rooms = random.randint(3, 8)
            room_names = ['Room1', 'Room2', 'Room3', 'Room4', 'Room5', 'VIP', 'ICU']
            for room_name in random.sample(room_names, min(num_rooms, len(room_names))):
                room_name = self.truncate_string(room_name, 10)
                description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
                self.cur.execute("""
                    INSERT INTO room (departID, name, description)
                    VALUES (%s, %s, %s)
                    RETURNING roomID;
                """, (departID, room_name, description))
                roomID = self.cur.fetchone()[0]
                rooms.append(roomID)
        self.conn.commit()
        print(f"{len(rooms)} rooms inserted")
        
        beds = []
        for _ in range(150):
            cost = random.randint(100000, 1000000)
            self.cur.execute("""
                INSERT INTO bed (cost)
                VALUES (%s)
                RETURNING bedID;
            """, (cost,))
            bedID = self.cur.fetchone()[0]
            beds.append(bedID)
        self.conn.commit()
        print("150 beds inserted")
        
        admissions = []
        for _ in range(80):
            pID, mID = random.choice(medical_records)
            doctorID = random.choice(doctors)
            officeStaffID = random.choice(office_staffs)
            cost = random.randint(1000000, 20000000)
            
            self.cur.execute("""
                INSERT INTO admission (mID, doctorID, officeStaffID, cost)
                VALUES (%s, %s, %s, %s)
                RETURNING admID;
            """, (mID, doctorID, officeStaffID, cost))
            admID = self.cur.fetchone()[0]
            admissions.append(admID)
        self.conn.commit()
        print(f"{len(admissions)} admissions inserted")
        
        for admID in admissions[:50]:
            bedID = random.choice(beds)
            roomID = random.choice(rooms)
            startTimestamp = self.fake.date_time_between(start_date='-30d', end_date='now')
            status = self.truncate_string(random.choice(['Occupied', 'Available', 'Cleaning']), 10)
            
            self.cur.execute("""
                INSERT INTO bedInfo (bedID, roomID, asgAdmID, startTimestamp, status)
                VALUES (%s, %s, %s, %s, %s);
            """, (bedID, roomID, admID, startTimestamp, status))
        self.conn.commit()
        print("Bed info inserted")
        
        appointments = []
        for _ in range(100):
            pID, mID = random.choice(medical_records)
            doctorID = random.choice(doctors)
            date = self.fake.date_between(start_date='-30d', end_date='+30d')
            time = self.fake.time()
            status = self.truncate_string(random.choice(['Scheduled', 'Completed', 'Cancelled', 'NoShow']), 10)
            isOnlineReserved = random.choice([True, False])
            
            self.cur.execute("""
                INSERT INTO appointment (mID, doctorID, date, time, status, isOnlineReserved)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING appoID;
            """, (mID, doctorID, date, time, status, isOnlineReserved))
            appoID = self.cur.fetchone()[0]
            appointments.append((appoID, mID, doctorID))
        self.conn.commit()
        print(f"{len(appointments)} appointments inserted")
        
        disease_diag_count = 0
        for appoID, mID, doctorID in appointments:
            icdID = random.choice(icd_codes)
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            self.cur.execute("""
                INSERT INTO diseaseDiag (appoID, icdID, description)
                VALUES (%s, %s, %s);
            """, (appoID, icdID, description))
            disease_diag_count += 1
        self.conn.commit()
        print(f"{disease_diag_count} disease diagnoses inserted")
        
        medicine_diag_count = 0
        for appoID, mID, doctorID in appointments:
            icdmID = random.choice(icdm_codes)
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            self.cur.execute("""
                INSERT INTO medicineDiag (appoID, icdmID, description)
                VALUES (%s, %s, %s);
            """, (appoID, icdmID, description))
            medicine_diag_count += 1
        self.conn.commit()
        print(f"{medicine_diag_count} medicine diagnoses inserted")
        
        vital_sign_count = 0
        for appoID, mID, doctorID in appointments:
            for paramID in random.sample(parameters, random.randint(2, 4)):
                value = round(random.uniform(50, 120), 2)
                self.cur.execute("""
                    INSERT INTO vitalSign (appoID, parameterID, parameterValue)
                    VALUES (%s, %s, %s);
                """, (appoID, paramID, value))
                vital_sign_count += 1
        self.conn.commit()
        print(f"{vital_sign_count} vital signs inserted")
        
        surgery_ids = []
        for _ in range(40):
            surgeryCode = random.choice(icds_codes)
            pID = random.choice(patients)
            chiefSurgeonId = random.choice(surgeons)
            roomID = random.choice(rooms)
            surgeryDate = self.fake.date_time_between(start_date='-60d', end_date='+30d')
            status = self.truncate_string(random.choice(['Scheduled', 'InProgress', 'Completed', 'Cancelled']), 10)
            finalReport = self.truncate_string(self.fake.text(max_nb_chars=30), 30)
            
            self.cur.execute("""
                INSERT INTO surgery (surgeryCode, pID, chiefSurgeonId, roomID, surgeryDate, status, finalReport)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING surgeryID;
            """, (surgeryCode, pID, chiefSurgeonId, roomID, surgeryDate, status, finalReport))
            surgeryID = self.cur.fetchone()[0]
            surgery_ids.append(surgeryID)
        self.conn.commit()
        print(f"{len(surgery_ids)} surgeries inserted")
        
        for surgeryID in surgery_ids:
            num_surgeons = random.randint(1, 3)
            for surgeonID in random.sample(surgeons, min(num_surgeons, len(surgeons))):
                self.cur.execute("""
                    INSERT INTO surgeryTeam (surgeryID, surgeonID)
                    VALUES (%s, %s);
                """, (surgeryID, surgeonID))
        self.conn.commit()
        print("Surgery teams inserted")
        
        reception_count = 0
        for _ in range(80):
            officeStaffID = random.choice(office_staffs)
            pID = random.choice(patients)
            appoID = random.choice([a[0] for a in appointments])
            surgeryID = random.choice(surgery_ids)
            
            self.cur.execute("""
                INSERT INTO receptionReserve (officeStaffID, pID, appoID, surgeryID)
                VALUES (%s, %s, %s, %s);
            """, (officeStaffID, pID, appoID, surgeryID))
            reception_count += 1
        self.conn.commit()
        print(f"{reception_count} reception reserves inserted")
        
        requests = []
        for _ in range(70):
            pID, mID = random.choice(medical_records)
            doctorID = random.choice(doctors)
            departID = random.choice(departments)
            medID = random.choice(icdm_codes)
            testID = random.choice(icdt_codes)
            name = self.truncate_string(self.fake.word(), 10)
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            status = self.truncate_string(random.choice(['Pending', 'Approved', 'Rejected', 'Completed']), 10)
            isPatientConfirmed = random.choice([True, False])
            cost = random.randint(100000, 5000000)
            
            self.cur.execute("""
                INSERT INTO request (mID, doctorID, departID, medID, testID, name,
                                   description, status, isPatientConfirmed, cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING reqID;
            """, (mID, doctorID, departID, medID, testID, name,
                  description, status, isPatientConfirmed, cost))
            reqID = self.cur.fetchone()[0]
            requests.append(reqID)
        self.conn.commit()
        print(f"{len(requests)} requests inserted")
        
        param_result_count = 0
        for reqID in requests:
            for paramID in random.sample(parameters, random.randint(1, 3)):
                value = random.randint(1, 100)
                self.cur.execute("""
                    INSERT INTO parameterResult (reqID, parameterID, parameterValue)
                    VALUES (%s, %s, %s);
                """, (reqID, paramID, value))
                param_result_count += 1
        self.conn.commit()
        print(f"{param_result_count} parameter results inserted")
        
        invoice_count = 0
        invoice_ids = []
        for _ in range(60):
            pID = random.choice(patients)
            appoID = random.choice([a[0] for a in appointments])
            reqID = random.choice(requests)
            surgeryID = random.choice(surgery_ids)
            admID = random.choice(admissions)
            
            totalAmount = random.randint(500000, 10000000)
            insuranceShare = int(totalAmount * random.uniform(0.1, 0.5))
            patientShare = totalAmount - insuranceShare
            isPaid = random.choice([True, False])
            
            self.cur.execute("""
                INSERT INTO invoice (pID, appoID, reqID, surgeryID, admID, totalAmount,
                                    insuranceShare, patientShare, isPaid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING invID;
            """, (pID, appoID, reqID, surgeryID, admID, totalAmount,
                  insuranceShare, patientShare, isPaid))
            invID = self.cur.fetchone()[0]
            invoice_ids.append(invID)
            invoice_count += 1
        self.conn.commit()
        print(f"{invoice_count} invoices inserted")
        
        all_item_ids = []
        for _ in range(50):
            itemType = self.truncate_string(random.choice(['Medicine', 'Test', 'Surgery', 'Service', 'Equipment']), 10)
            description = self.truncate_string(self.fake.text(max_nb_chars=30), 30)
            
            self.cur.execute("""
                INSERT INTO allItems (itemType, description)
                VALUES (%s, %s)
                RETURNING itemID;
            """, (itemType, description))
            itemID = self.cur.fetchone()[0]
            all_item_ids.append(itemID)
        self.conn.commit()
        print("50 allItems inserted")
        
        invoice_item_count = 0
        for invID in invoice_ids:
            num_items = random.randint(1, 5)
            for itemID in random.sample(all_item_ids, min(num_items, len(all_item_ids))):
                description = self.truncate_string(self.fake.text(max_nb_chars=30), 30)
                self.cur.execute("""
                    INSERT INTO invoiceItem (itemID, invoiceID, description)
                    VALUES (%s, %s, %s);
                """, (invID, itemID, description))
                invoice_item_count += 1
        self.conn.commit()
        print(f"{invoice_item_count} invoice items inserted")
        
        sign_types = []
        sign_names = ['Vital', 'Resp', 'Cardiac', 'GI', 'Neuro']
        for sign_name in sign_names:
            sign_name = self.truncate_string(sign_name, 10)
            self.cur.execute("""
                INSERT INTO signType (signName)
                VALUES (%s)
                RETURNING sTypeID;
            """, (sign_name,))
            sTypeID = self.cur.fetchone()[0]
            sign_types.append(sTypeID)
        self.conn.commit()
        print("5 sign types inserted")
        
        equipment_ids = []
        equip_names = ['Monitor', 'Oximeter', 'BP', 'Thermo', 'ECG', 'Oxygen']
        for _ in range(50):
            sTypeID = random.choice(sign_types)
            name = self.truncate_string(random.choice(equip_names), 10)
            MACAddress = self.truncate_string(self.fake.mac_address(), 10)
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            
            self.cur.execute("""
                INSERT INTO equipment (sTypeID, name, MACAddress, description)
                VALUES (%s, %s, %s, %s)
                RETURNING equipID;
            """, (sTypeID, name, MACAddress, description))
            equipID = self.cur.fetchone()[0]
            equipment_ids.append(equipID)
        self.conn.commit()
        print("50 equipment inserted")
        
        equip_info_count = 0
        for equipID in equipment_ids[:30]:
            roomID = random.choice(rooms)
            asgAdmID = random.choice(admissions)
            startTimestamp = self.fake.date_time_between(start_date='-30d', end_date='now')
            status = self.truncate_string(random.choice(['Active', 'Inactive', 'Maintenance']), 10)
            
            self.cur.execute("""
                INSERT INTO equipInfo (equipID, roomID, asgAdmID, startTimestamp, status)
                VALUES (%s, %s, %s, %s, %s);
            """, (equipID, roomID, asgAdmID, startTimestamp, status))
            equip_info_count += 1
        self.conn.commit()
        print(f"{equip_info_count} equipment info inserted")
        
        logs = []
        for equipID in equipment_ids[:30]:
            parameterID = random.choice(parameters)
            asgAdmID = random.choice(admissions)
            parameterValue = round(random.uniform(50, 120), 2)
            
            self.cur.execute("""
                INSERT INTO log (equipID, parameterID, asgAdmID, parameterValue)
                VALUES (%s, %s, %s, %s)
                RETURNING logID;
            """, (equipID, parameterID, asgAdmID, parameterValue))
            logID = self.cur.fetchone()[0]
            logs.append(logID)
        self.conn.commit()
        print("30 logs inserted")
        
        warning_count = 0
        for logID in logs:
            importance = self.truncate_string(random.choice(['Low', 'Medium', 'High', 'Critical']), 10)
            occuredTime = self.fake.date_time_between(start_date='-7d', end_date='now')
            checkedStatus = self.truncate_string(random.choice(['Pending', 'Checked', 'Resolved']), 10)
            checkedTime = occuredTime + timedelta(hours=random.randint(1, 48))
            
            self.cur.execute("""
                INSERT INTO warning (logID, importance, occuredTime, checkedStatus, checkedTime)
                VALUES (%s, %s, %s, %s, %s);
            """, (logID, importance, occuredTime, checkedStatus, checkedTime))
            warning_count += 1
        self.conn.commit()
        print(f"{warning_count} warnings inserted")
        
        storage_count = 0
        for _ in range(60):
            departID = random.choice(departments)
            medID = random.choice(icdm_codes)
            name = self.truncate_string(self.fake.word(), 10)
            type = self.truncate_string(random.choice(['Tablet', 'Syrup', 'Injection', 'Capsule']), 10)
            enterDate = self.fake.date_time_between(start_date='-180d', end_date='now')
            exitDate = enterDate + timedelta(days=random.randint(1, 90))
            cost = random.randint(10000, 500000)
            
            self.cur.execute("""
                INSERT INTO storage (departID, medID, name, type, enterDate, exitDate, cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (departID, medID, name, type, enterDate, exitDate, cost))
            storage_count += 1
        self.conn.commit()
        print(f"{storage_count} storage records inserted")
        
        conflict_count = 0
        for _ in range(30):
            departID = random.choice(departments)
            icdm1ID = random.choice(icdm_codes)
            icdm2ID = random.choice(icdm_codes)
            if icdm1ID != icdm2ID:
                self.cur.execute("""
                    INSERT INTO medicineConflict (departID, icdm1ID, icdm2ID)
                    VALUES (%s, %s, %s);
                """, (departID, icdm1ID, icdm2ID))
                conflict_count += 1
        self.conn.commit()
        print(f"{conflict_count} medicine conflicts inserted")
        
        transfer_count = 0
        for admID in admissions[:30]:
            destBedID = random.choice(beds)
            cost = random.randint(100000, 500000)
            self.cur.execute("""
                INSERT INTO transfer (admID, destBedID, cost)
                VALUES (%s, %s, %s);
            """, (admID, destBedID, cost))
            transfer_count += 1
        self.conn.commit()
        print(f"{transfer_count} transfers inserted")
        
        disease_record_count = 0
        for pID, mID in medical_records:
            for icdID in random.sample(icd_codes, random.randint(1, 3)):
                description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
                self.cur.execute("""
                    INSERT INTO diseaseRecord (mID, icdID, description)
                    VALUES (%s, %s, %s);
                """, (mID, icdID, description))
                disease_record_count += 1
        self.conn.commit()
        print(f"{disease_record_count} disease records inserted")
        
        drug_record_count = 0
        for pID, mID in medical_records:
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            self.cur.execute("""
                INSERT INTO drugRecord (mID, description)
                VALUES (%s, %s);
            """, (mID, description))
            drug_record_count += 1
        self.conn.commit()
        print(f"{drug_record_count} drug records inserted")
        
        medicine_record_count = 0
        for pID, mID in medical_records:
            icdmID = random.choice(icdm_codes)
            description = self.truncate_string(self.fake.text(max_nb_chars=20), 20)
            self.cur.execute("""
                INSERT INTO medicineRecord (mID, icdmID, description)
                VALUES (%s, %s, %s);
            """, (mID, icdmID, description))
            medicine_record_count += 1
        self.conn.commit()
        print(f"{medicine_record_count} medicine records inserted")
        
        print("\nDatabase seeding completed successfully!")
        return True
    
    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    force = "--force" in sys.argv
    
    seeder = DatabaseSeeder()
    success = seeder.seed(force=force)
    seeder.close()
    
    if success:
        print("\nAll done! Database is ready.")
    else:
        print("\nSeeding skipped.")