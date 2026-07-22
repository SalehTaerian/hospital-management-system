CREATE OR REPLACE VIEW v_get_appointment_working_pressure AS
    SELECT d.name , count(distinct a.appoID)  AS docAppo   
    FROM department d
    JOIN employee e ON d.departID = e.departID
    JOIN doctor doc ON doc.employeeID = e.employeeID
    JOIN appointment a ON a.doctorID = doc.employeeID
    WHERE a.date >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY d.name;
CREATE OR REPLACE VIEW v_get_appointment_working_pressure_for_staff AS
    SELECT d.name , count(distinct a.appoID)  AS staffAppo    
    FROM department d
    JOIN employee e ON d.departID = e.departID
    JOIN officeStaff o ON o.employeeID = e.employeeID
    JOIN appointment a ON a.staffID = o.employeeID
    WHERE a.date >= CURRENT_DATE - INTERVAL '7 days' AND a.isOnlineReserved = false
    GROUP BY d.name;

CREATE OR REPLACE VIEW v_get_admission_working_pressure_for_doctors AS
    SELECT d.name , count(distinct a.admID)  AS docAdm    
    FROM department d
    JOIN employee e ON d.departID = e.departID
    JOIN doctor doc ON doc.employeeID = e.employeeID
    JOIN admission a ON a.doctorID = doc.employeeID
    JOIN transfer t ON t.admID = a.admID
    WHERE t.transferedAt = 
    (
    SELECT MAX(t2.transferedAt)
    FROM transfer t2
    WHERE t2.admID = t.admID
    )
    AND
    t.transferedAt >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY d.name;
CREATE OR REPLACE VIEW v_get_admission_working_pressure_for_staff AS
    SELECT d.name , count(distinct a.admID)  AS staffAdm    
    FROM department d
    JOIN employee e ON d.departID = e.departID
    JOIN officeStaff o ON o.employeeID = e.employeeID
    JOIN admission a ON a.officeStaffID = o.employeeID
    JOIN transfer t ON t.admID = a.admID
    WHERE t.transferedAt = 
    (
    SELECT MAX(t2.transferedAt)
    FROM transfer t2
    WHERE t2.admID = t.admID
    )
    AND
    t.transferedAt >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY d.name;
CREATE OR REPLACE VIEW v_get_surgery_working_pressure AS
    SELECT d.name , count(distinct surgery.surgeryID)  AS surgeryPres    
    FROM department d
    JOIN employee e ON d.departID = e.departID
    JOIN surgeon s ON s.employeeID = e.employeeID
    JOIN surgery ON surgery.chiefSurgeonId = s.employeeID
    WHERE surgery.surgeryDate >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY d.name;