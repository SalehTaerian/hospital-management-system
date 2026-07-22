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