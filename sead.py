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
            database="hospital-management-system", 
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
                  'doctorSpecialization', 'surgeonSpecialization']
        
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
            firstName = self.truncate_string(self.fake.first_name(), 35)
            lastName = self.truncate_string(self.fake.last_name(), 35)
            nationalCode = self.generate_national_id()
            password = self.truncate_string(self.fake.password(length=10), 30)
            gender = random.choice(['Male', 'Female'])
            dateOfBirth = self.fake.date_of_birth(minimum_age=18, maximum_age=90)
            phoneNumber = self.generate_phone_number()
            homeNumber = self.generate_phone_number()
            city = self.truncate_string(self.fake.city(), 15)
            province = self.truncate_string(self.fake.state(), 15)
            street = self.truncate_string(self.fake.street_name(), 100)
            alley = self.truncate_string(self.fake.street_name(), 100)
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
            smokingHistory = self.truncate_string(random.choice(['Never', 'Former', 'Current', 'Passive']), 50)
            
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
            name = self.truncate_string(random.choice(['Health', 'Atieh', 'Asia', 'Dana', 'Pasargad']), 35)
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
            name = self.truncate_string(self.fake.company(), 30)
            city = self.truncate_string(self.fake.city(), 20)
            province = self.truncate_string(self.fake.state(), 20)
            street = self.truncate_string(self.fake.street_name(), 20)
            alley = self.truncate_string(self.fake.street_name(), 20)
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
        dept_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Internal Medicine', 
                      'General Surgery', 'Pediatrics', 'Gynecology', 'Dermatology', 
                      'Ophthalmology', 'ENT']
        for hospitalID in hospitals:
            for dept_name in random.sample(dept_names, random.randint(3, 5)):
                dept_name = self.truncate_string(dept_name, 30)
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
                firstName = self.truncate_string(self.fake.first_name(), 50)
                lastName = self.truncate_string(self.fake.last_name(), 50)
                nationalCode = self.generate_national_id()
                password = self.truncate_string(self.fake.password(length=10), 30)
                contractType = self.truncate_string(random.choice(['Permanent', 'Temporary', 'Contract']), 20)
                hireDate = self.fake.date_between(start_date='-10y', end_date='today')
                accessLevel = self.truncate_string(random.choice(['Admin', 'Doctor', 'Nurse', 'Staff', 'Surgeon']), 50)
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
        spec_names = ['Cardiology', 'Neurology', 'Orthopedics', 'Internal Medicine', 
                      'Pediatrics', 'Gynecology', 'Dermatology', 'Ophthalmology', 
                      'ENT', 'General Medicine']
        for spec_name in spec_names:
            spec_name = self.truncate_string(spec_name, 20)
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
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='?????-######'), 20)
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
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='?????-######'), 20)
                surgicalField = self.truncate_string(random.choice(['Cardiac', 'Orthopedic', 'Neurosurgery', 'General', 'Plastic']), 30)
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
                medicalNumber = self.truncate_string(self.fake.unique.bothify(text='NUR-######'), 20)
                grade = self.truncate_string(random.choice(['A', 'B', 'C']), 30)
                self.cur.execute("""
                    INSERT INTO nurse (employeeID, medicalNumber, grade)
                    VALUES (%s, %s, %s);
                """, (empID, medicalNumber, grade))
                nurses.append(empID)
        self.conn.commit()
        print(f"{len(nurses)} nurses inserted")
        
        office_staffs = []
        for empID, accessLevel in employee_types:
            if accessLevel == 'Staff':
                role = self.truncate_string(random.choice(['Receptionist', 'Secretary', 'Administrator', 'Billing']), 30)
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
                try:
                    self.cur.execute("""
                        INSERT INTO employeeShift (employeeID, shiftID)
                        VALUES (%s, %s);
                    """, (empID, shiftID))
                except:
                    self.conn.rollback()
        self.conn.commit()
        print("Employee shifts inserted")
        
        parameters = []
        param_names = ['Cold', 'Fever', 'Blood Pressure', 'Heart Rate', 'Blood Oxygen', 
                       'Blood Sugar', 'Cholesterol', 'Triglyceride']
        for param_name in param_names:
            param_name = self.truncate_string(param_name, 25)
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
        diseases = ['Influenza', 'Common Cold', 'Hypertension', 'Diabetes', 
                    'Asthma', 'Bronchitis', 'Pneumonia']
        for disease in diseases:
            disease = self.truncate_string(disease, 50)
            code = self.truncate_string(self.fake.unique.bothify(text='??-###'), 20)
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
        medicines = ['Acetaminophen', 'Ibuprofen', 'Aspirin', 'Penicillin', 
                     'Amoxicillin', 'Losartan', 'Metformin']
        for icdID in icd_codes:
            for medicine in random.sample(medicines, random.randint(1, 3)):
                medicine = self.truncate_string(medicine, 20)
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
        surgeries = ['Cardiac Bypass', 'Knee Surgery', 'Spinal Surgery', 
                     'Appendectomy', 'Gallbladder Surgery']
        for surgery_name in surgeries:
            surgery_name = self.truncate_string(surgery_name, 20)
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
        tests = ['Blood Test', 'Urine Test', 'CT Scan', 'MRI', 'Echocardiography', 'ECG']
        for test_name in tests:
            test_name = self.truncate_string(test_name, 50)
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
            room_names = ['Room 1', 'Room 2', 'Room 3', 'Room 4', 'Room 5', 'VIP Room', 'ICU']
            for room_name in random.sample(room_names, min(num_rooms, len(room_names))):
                room_name = self.truncate_string(room_name, 20)
                description = self.truncate_string(self.fake.text(max_nb_chars=50), 1000)
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
            doctorID = random.choice(doctors) if doctors else None
            officeStaffID = random.choice(office_staffs) if office_staffs else None
            cost = random.randint(1000000, 20000000)
            
            if doctorID and officeStaffID:
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
            status = self.truncate_string(random.choice(['Occupied', 'Available', 'Cleaning']), 20)
            
            self.cur.execute("""
                INSERT INTO bedInfo (bedID, roomID, asgAdmID, startTimestamp, status)
                VALUES (%s, %s, %s, %s, %s);
            """, (bedID, roomID, admID, startTimestamp, status))
        self.conn.commit()
        print("Bed info inserted")
        
        appointments = []
        for _ in range(100):
            pID, mID = random.choice(medical_records)
            doctorID = random.choice(doctors) if doctors else None
            date = self.fake.date_between(start_date='-30d', end_date='+30d')
            time = self.fake.time()
            status = self.truncate_string(random.choice(['Scheduled', 'Completed', 'Cancelled', 'NoShow']), 20)
            isOnlineReserved = random.choice([True, False])
            
            if doctorID:
                self.cur.execute("""
                    INSERT INTO appointment (mID, doctorID, date, time, status, isOnlineReserved)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING appoID;
                """, (mID, doctorID, date, time, status, isOnlineReserved))
                appoID = self.cur.fetchone()[0]
                appointments.append((appoID, mID, doctorID))
        self.conn.commit()
        print(f"{len(appointments)} appointments inserted")
        
        for appoID, mID, doctorID in appointments:
            if random.random() > 0.3:
                icdID = random.choice(icd_codes)
                description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
                self.cur.execute("""
                    INSERT INTO diseaseDiag (appoID, icdID, description)
                    VALUES (%s, %s, %s);
                """, (appoID, icdID, description))
        self.conn.commit()
        print("Disease diagnoses inserted")
        
        for appoID, mID, doctorID in appointments:
            if random.random() > 0.4:
                icdmID = random.choice(icdm_codes)
                description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
                self.cur.execute("""
                    INSERT INTO medicineDiag (appoID, icdmID, description)
                    VALUES (%s, %s, %s);
                """, (appoID, icdmID, description))
        self.conn.commit()
        print("Medicine diagnoses inserted")
        
        for appoID, mID, doctorID in appointments:
            for paramID in random.sample(parameters, random.randint(2, 4)):
                value = round(random.uniform(50, 120), 2)
                self.cur.execute("""
                    INSERT INTO vitalSign (appoID, parameterID, parameterValue)
                    VALUES (%s, %s, %s);
                """, (appoID, paramID, value))
        self.conn.commit()
        print("Vital signs inserted")
        
        surgery_ids = []
        for _ in range(40):
            surgeryCode = random.choice(icds_codes)
            pID = random.choice(patients)
            chiefSurgeonId = random.choice(surgeons) if surgeons else None
            roomID = random.choice(rooms)
            surgeryDate = self.fake.date_time_between(start_date='-60d', end_date='+30d')
            status = self.truncate_string(random.choice(['Scheduled', 'InProgress', 'Completed', 'Cancelled']), 20)
            finalReport = self.truncate_string(self.fake.text(max_nb_chars=200), 1000) if random.random() > 0.3 else None
            
            if chiefSurgeonId:
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
        
        for _ in range(80):
            officeStaffID = random.choice(office_staffs) if office_staffs else None
            pID = random.choice(patients)
            appoID = random.choice([a[0] for a in appointments]) if random.random() > 0.5 else None
            surgeryID = random.choice(surgery_ids) if random.random() > 0.7 and surgery_ids else None
            
            if officeStaffID:
                self.cur.execute("""
                    INSERT INTO receptionReserve (officeStaffID, pID, appoID, surgeryID)
                    VALUES (%s, %s, %s, %s);
                """, (officeStaffID, pID, appoID, surgeryID))
        self.conn.commit()
        print("Reception reserves inserted")
        
        for _ in range(60):
            pID = random.choice(patients)
            appoID = random.choice([a[0] for a in appointments]) if random.random() > 0.3 else None
            surgeryID = random.choice(surgery_ids) if random.random() > 0.5 and surgery_ids else None
            admID = random.choice(admissions) if random.random() > 0.5 and admissions else None
            
            totalAmount = random.randint(500000, 10000000)
            insuranceShare = int(totalAmount * random.uniform(0.1, 0.5))
            patientShare = totalAmount - insuranceShare
            isPaid = random.choice([True, False])
            
            self.cur.execute("""
                INSERT INTO invoice (pID, appoID, reqID, surgeryID, admID, totalAmount, 
                                    insuranceShare, patientShare, isPaid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (pID, appoID, None, surgeryID, admID, totalAmount, 
                  insuranceShare, patientShare, isPaid))
        self.conn.commit()
        print("60 invoices inserted")
        
        requests = []
        for _ in range(70):
            pID, mID = random.choice(medical_records)
            doctorID = random.choice(doctors) if doctors else None
            departID = random.choice(departments)
            medID = random.choice(icdm_codes) if random.random() > 0.5 else None
            testID = random.choice(icdt_codes) if random.random() > 0.5 else None
            name = self.truncate_string(self.fake.word(), 50)
            description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
            status = self.truncate_string(random.choice(['Pending', 'Approved', 'Rejected', 'Completed']), 20)
            isPatientConfirmed = random.choice([True, False])
            cost = random.randint(100000, 5000000)
            
            if doctorID:
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
        
        for reqID in requests:
            for paramID in random.sample(parameters, random.randint(1, 3)):
                value = random.randint(1, 100)
                self.cur.execute("""
                    INSERT INTO parameterResult (reqID, parameterID, parameterValue)
                    VALUES (%s, %s, %s);
                """, (reqID, paramID, value))
        self.conn.commit()
        print("Parameter results inserted")
        
        sign_types = []
        sign_names = ['Vital Signs', 'Respiratory', 'Cardiac', 'Gastrointestinal', 'Neurological']
        for sign_name in sign_names:
            sign_name = self.truncate_string(sign_name, 20)
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
        equip_names = ['Vital Monitor', 'Pulse Oximeter', 'Sphygmomanometer', 
                       'Thermometer', 'ECG Machine', 'Oxygen Generator']
        for _ in range(50):
            sTypeID = random.choice(sign_types)
            name = self.truncate_string(random.choice(equip_names), 30)
            MACAddress = self.truncate_string(self.fake.mac_address(), 30)
            description = self.truncate_string(self.fake.text(max_nb_chars=50), 1000)
            
            self.cur.execute("""
                INSERT INTO equipment (sTypeID, name, MACAddress, description)
                VALUES (%s, %s, %s, %s)
                RETURNING equipID;
            """, (sTypeID, name, MACAddress, description))
            equipID = self.cur.fetchone()[0]
            equipment_ids.append(equipID)
        self.conn.commit()
        print("50 equipment inserted")
        
        for equipID in equipment_ids[:30]:
            roomID = random.choice(rooms)
            asgAdmID = random.choice(admissions) if random.random() > 0.3 else None
            startTimestamp = self.fake.date_time_between(start_date='-30d', end_date='now')
            status = self.truncate_string(random.choice(['Active', 'Inactive', 'Maintenance']), 20)
            
            self.cur.execute("""
                INSERT INTO equipInfo (equipID, roomID, asgAdmID, startTimestamp, status)
                VALUES (%s, %s, %s, %s, %s);
            """, (equipID, roomID, asgAdmID, startTimestamp, status))
        self.conn.commit()
        print("Equipment info inserted")
        
        logs = []
        for equipID in equipment_ids[:30]:
            parameterID = random.choice(parameters)
            asgAdmID = random.choice(admissions) if random.random() > 0.3 else None
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
        
        for logID in logs:
            if random.random() > 0.3:
                importance = self.truncate_string(random.choice(['Low', 'Medium', 'High', 'Critical']), 20)
                occuredTime = self.fake.date_time_between(start_date='-7d', end_date='now')
                checkedStatus = self.truncate_string(random.choice(['Pending', 'Checked', 'Resolved']), 20)
                checkedTime = occuredTime + timedelta(hours=random.randint(1, 48)) if checkedStatus != 'Pending' else None
                
                self.cur.execute("""
                    INSERT INTO warning (logID, importance, occuredTime, checkedStatus, checkedTime)
                    VALUES (%s, %s, %s, %s, %s);
                """, (logID, importance, occuredTime, checkedStatus, checkedTime))
        self.conn.commit()
        print("Warnings inserted")
        
        for _ in range(60):
            departID = random.choice(departments)
            medID = random.choice(icdm_codes)
            name = self.truncate_string(self.fake.word(), 30)
            type = self.truncate_string(random.choice(['Tablet', 'Syrup', 'Injection', 'Capsule']), 20)
            enterDate = self.fake.date_time_between(start_date='-180d', end_date='now')
            exitDate = enterDate + timedelta(days=random.randint(1, 90)) if random.random() > 0.3 else None
            cost = random.randint(10000, 500000)
            
            self.cur.execute("""
                INSERT INTO storage (departID, medID, name, type, enterDate, exitDate, cost)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (departID, medID, name, type, enterDate, exitDate, cost))
        self.conn.commit()
        print("60 storage records inserted")
        
        for _ in range(30):
            departID = random.choice(departments)
            icdm1ID = random.choice(icdm_codes)
            icdm2ID = random.choice(icdm_codes)
            if icdm1ID != icdm2ID:
                try:
                    self.cur.execute("""
                        INSERT INTO medicineConflict (departID, icdm1ID, icdm2ID)
                        VALUES (%s, %s, %s);
                    """, (departID, icdm1ID, icdm2ID))
                except:
                    self.conn.rollback()
        self.conn.commit()
        print("30 medicine conflicts inserted")
        
        for admID in admissions[:30]:
            destBedID = random.choice(beds)
            cost = random.randint(100000, 500000)
            self.cur.execute("""
                INSERT INTO transfer (admID, destBedID, cost)
                VALUES (%s, %s, %s);
            """, (admID, destBedID, cost))
        self.conn.commit()
        print("30 transfers inserted")
        
        for pID, mID in medical_records:
            for icdID in random.sample(icd_codes, random.randint(1, 3)):
                description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
                self.cur.execute("""
                    INSERT INTO diseaseRecord (mID, icdID, description)
                    VALUES (%s, %s, %s);
                """, (mID, icdID, description))
        self.conn.commit()
        print("Disease records inserted")
        
        for pID, mID in medical_records:
            description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
            self.cur.execute("""
                INSERT INTO drugRecord (mID, description)
                VALUES (%s, %s);
            """, (mID, description))
        self.conn.commit()
        print("Drug records inserted")
        
        for pID, mID in medical_records:
            if random.random() > 0.3:
                icdmID = random.choice(icdm_codes)
                description = self.truncate_string(self.fake.text(max_nb_chars=100), 1000)
                self.cur.execute("""
                    INSERT INTO medicineRecord (mID, icdmID, description)
                    VALUES (%s, %s, %s);
                """, (mID, icdmID, description))
        self.conn.commit()
        print("Medicine records inserted")
        
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