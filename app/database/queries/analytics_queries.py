from app.database.connection import DatabaseConnection

def get_disease_abundance():
    query = """
        SELECT 
            icd.icdID,
            icd.code,
            icd.diseaseName,
            COUNT(dd.disDiagID) as diagnosis_count,
            COUNT(DISTINCT dd.appoID) as appointment_count,
            COUNT(DISTINCT p.pID) as patient_count
        FROM icdCode icd
        LEFT JOIN diseaseDiag dd ON icd.icdID = dd.icdID
        LEFT JOIN appointment a ON dd.appoID = a.appoID
        LEFT JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN patient p ON mr.pID = p.pID
        GROUP BY icd.icdID, icd.code, icd.diseaseName
        ORDER BY diagnosis_count DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_disease_medicine_effectiveness(disease_id=None):
    query = """
        SELECT 
            icd.icdID,
            icd.code,
            icd.diseaseName,
            icdm.icdmID,
            icdm.medicineName,
            COUNT(DISTINCT md.medDiagID) as prescription_count,
            AVG(fb.effectPercentage) as avg_effectiveness,
            MIN(fb.effectPercentage) as min_effectiveness,
            MAX(fb.effectPercentage) as max_effectiveness,
            COUNT(fb.feedBackID) as feedback_count
        FROM icdCode icd
        JOIN diseaseDiag dd ON icd.icdID = dd.icdID
        JOIN medicineDiag md ON dd.disDiagID = md.disDiagID
        JOIN icdmCode icdm ON md.icdmID = icdm.icdmID
        LEFT JOIN feedBack fb ON md.medDiagID = fb.medDiagID
        WHERE 1=1
    """
    params = []
    
    if disease_id:
        query += " AND icd.icdID = %s"
        params.append(disease_id)
    
    query += """
        GROUP BY icd.icdID, icd.code, icd.diseaseName, icdm.icdmID, icdm.medicineName
        ORDER BY icd.diseaseName, prescription_count DESC
    """
    
    return DatabaseConnection.execute_query(
        query,
        tuple(params) if params else None,
        fetch_all=True,
        fetch_dict=True
    )

def get_disease_details(disease_id):
    query = """
        SELECT 
            icd.icdID,
            icd.code,
            icd.diseaseName,
            COUNT(DISTINCT dd.disDiagID) as total_diagnoses,
            COUNT(DISTINCT p.pID) as total_patients,
            COUNT(DISTINCT a.appoID) as total_appointments
        FROM icdCode icd
        LEFT JOIN diseaseDiag dd ON icd.icdID = dd.icdID
        LEFT JOIN appointment a ON dd.appoID = a.appoID
        LEFT JOIN medicalRecord mr ON a.mID = mr.mID
        LEFT JOIN patient p ON mr.pID = p.pID
        WHERE icd.icdID = %s
        GROUP BY icd.icdID, icd.code, icd.diseaseName
    """
    return DatabaseConnection.execute_query(
        query,
        (disease_id,),
        fetch_one=True,
        fetch_dict=True
    )

def get_top_diseases(limit=10):
    query = """
        SELECT 
            icd.icdID,
            icd.code,
            icd.diseaseName,
            COUNT(dd.disDiagID) as diagnosis_count
        FROM icdCode icd
        LEFT JOIN diseaseDiag dd ON icd.icdID = dd.icdID
        GROUP BY icd.icdID, icd.code, icd.diseaseName
        ORDER BY diagnosis_count DESC
        LIMIT %s
    """
    return DatabaseConnection.execute_query(
        query,
        (limit,),
        fetch_all=True,
        fetch_dict=True
    )

def get_medicine_effectiveness_summary():
    query = """
        SELECT 
            icdm.icdmID,
            icdm.medicineName,
            COUNT(DISTINCT md.medDiagID) as total_prescriptions,
            AVG(fb.effectPercentage) as avg_effectiveness,
            COUNT(fb.feedBackID) as feedback_count
        FROM icdmCode icdm
        LEFT JOIN medicineDiag md ON icdm.icdmID = md.icdmID
        LEFT JOIN feedBack fb ON md.medDiagID = fb.medDiagID
        GROUP BY icdm.icdmID, icdm.medicineName
        HAVING COUNT(fb.feedBackID) > 0
        ORDER BY avg_effectiveness DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_disease_timeline(disease_id):
    query = """
        SELECT 
            DATE_TRUNC('month', a.createdAt) as month,
            COUNT(dd.disDiagID) as diagnosis_count
        FROM diseaseDiag dd
        JOIN appointment a ON dd.appoID = a.appoID
        WHERE dd.icdID = %s
        GROUP BY DATE_TRUNC('month', a.createdAt)
        ORDER BY month DESC
        LIMIT 12
    """
    return DatabaseConnection.execute_query(
        query,
        (disease_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_overall_statistics():
    query = """
        SELECT 
            (SELECT COUNT(*) FROM patient) as total_patients,
            (SELECT COUNT(*) FROM icdCode) as total_diseases,
            (SELECT COUNT(*) FROM diseaseDiag) as total_diagnoses,
            (SELECT COUNT(DISTINCT icdID) FROM diseaseDiag) as diseases_with_diagnoses,
            (SELECT COUNT(*) FROM medicineDiag) as total_prescriptions,
            (SELECT COUNT(*) FROM feedBack) as total_feedback
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )
    
def get_average_waiting_time():
    query = """
        SELECT 
            AVG(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as avg_waiting_minutes,
            MIN(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as min_waiting_minutes,
            MAX(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as max_waiting_minutes,
            COUNT(*) as total_appointments
        FROM appointment a
        WHERE a.enterTime IS NOT NULL 
        AND a.reserveTime IS NOT NULL
        AND a.status = 'Completed'
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )

def get_bed_occupancy_rate():
    query = """
        WITH latest_bed_status AS (
            SELECT DISTINCT ON (bedID) 
                bedID, 
                status
            FROM bedInfo
            ORDER BY bedID, startTimestamp DESC
        ),
        bed_counts AS (
            SELECT 
                COUNT(*) as total_beds,
                COUNT(CASE WHEN status = 'Occupied' THEN 1 END) as occupied_beds
            FROM latest_bed_status
        )
        SELECT 
            total_beds,
            occupied_beds,
            CASE 
                WHEN total_beds > 0 THEN ROUND((occupied_beds::DECIMAL / total_beds) * 100, 2)
                ELSE 0
            END as occupancy_rate
        FROM bed_counts
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )

def get_readmission_rate_30_days():
    query = """
        WITH patient_admissions AS (
            SELECT 
                mr.pID,
                a.admID,
                a.createdAt,
                ROW_NUMBER() OVER (PARTITION BY mr.pID ORDER BY a.createdAt) as admission_number
            FROM admission a
            JOIN medicalRecord mr ON a.mID = mr.mID
        ),
        readmissions AS (
            SELECT 
                p1.pID,
                p1.admID as first_admission,
                p2.admID as readmission,
                p1.createdAt as first_date,
                p2.createdAt as readmission_date,
                EXTRACT(DAY FROM (p2.createdAt - p1.createdAt)) as days_between
            FROM patient_admissions p1
            JOIN patient_admissions p2 ON p1.pID = p2.pID 
                AND p2.admission_number = p1.admission_number + 1
                AND p2.createdAt - p1.createdAt <= INTERVAL '30 days'
            WHERE p1.admission_number = 1
        ),
        all_patients AS (
            SELECT COUNT(DISTINCT pID) as total_patients
            FROM patient
        ),
        readmitted_patients AS (
            SELECT COUNT(DISTINCT pID) as readmitted_count
            FROM readmissions
        )
        SELECT 
            COALESCE(rp.readmitted_count, 0) as readmitted_patients,
            ap.total_patients,
            CASE 
                WHEN ap.total_patients > 0 THEN ROUND((COALESCE(rp.readmitted_count, 0)::DECIMAL / ap.total_patients) * 100, 2)
                ELSE 0
            END as readmission_rate
        FROM all_patients ap
        CROSS JOIN readmitted_patients rp
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )

def get_average_admission_time():
    query = """
        WITH admission_durations AS (
            SELECT 
                a.admID,
                a.createdAt as admission_start,
                COALESCE(a.endTime, CURRENT_TIMESTAMP) as admission_end,
                EXTRACT(EPOCH FROM (COALESCE(a.endTime, CURRENT_TIMESTAMP) - a.createdAt)) / 3600 as hours_admitted,
                EXTRACT(EPOCH FROM (COALESCE(a.endTime, CURRENT_TIMESTAMP) - a.createdAt)) / 86400 as days_admitted
            FROM admission a
            WHERE a.createdAt IS NOT NULL
        )
        SELECT 
            COUNT(*) as total_admissions,
            ROUND(AVG(hours_admitted), 2) as avg_hours,
            ROUND(AVG(days_admitted), 2) as avg_days,
            ROUND(MIN(hours_admitted), 2) as min_hours,
            ROUND(MAX(hours_admitted), 2) as max_hours
        FROM admission_durations
        WHERE hours_admitted > 0
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_one=True,
        fetch_dict=True
    )

def get_admission_time_by_department():
    query = """
        WITH latest_bedinfo AS (
            SELECT DISTINCT ON (bedID)
                bedID,
                roomID,
                status,
                startTimestamp
            FROM bedInfo
            ORDER BY bedID, startTimestamp DESC
        ),
        admission_durations AS (
            SELECT 
                a.admID,
                a.createdAt as admission_start,
                COALESCE(a.endTime, CURRENT_TIMESTAMP) as admission_end,
                d.name as department_name,
                EXTRACT(EPOCH FROM (COALESCE(a.endTime, CURRENT_TIMESTAMP) - a.createdAt)) / 3600 as hours_admitted
            FROM admission a
            JOIN bedInfo bi ON a.admID = bi.asgAdmID
            JOIN room r ON bi.roomID = r.roomID
            JOIN department d ON r.departID = d.departID
            WHERE a.createdAt IS NOT NULL
        )
        SELECT 
            department_name,
            COUNT(*) as admission_count,
            ROUND(AVG(hours_admitted), 2) as avg_hours,
            ROUND(AVG(hours_admitted) / 24, 2) as avg_days
        FROM admission_durations
        WHERE hours_admitted > 0
        GROUP BY department_name
        ORDER BY avg_hours DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def get_daily_waiting_time_trend(days=30):
    query = """
        SELECT 
            DATE(a.date) as appointment_date,
            COUNT(*) as total_appointments,
            AVG(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as avg_waiting_minutes,
            MIN(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as min_waiting_minutes,
            MAX(EXTRACT(EPOCH FROM (a.enterTime - a.reserveTime)) / 60) as max_waiting_minutes
        FROM appointment a
        WHERE a.enterTime IS NOT NULL 
        AND a.reserveTime IS NOT NULL
        AND a.status = 'Completed'
        AND a.date >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY DATE(a.date)
        ORDER BY appointment_date DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (days,),
        fetch_all=True,
        fetch_dict=True
    )