from app.database.connection import DatabaseConnection
from datetime import datetime

def get_patient_invoices(patient_id):
    query = """
        SELECT 
            i.invID,
            i.issueDate,
            i.totalAmount,
            i.insuranceShare,
            i.patientShare,
            i.isPaid,
            COUNT(ii.itemID) as item_count,
            STRING_AGG(DISTINCT ai.itemType, ', ') as item_types
        FROM invoice i
        LEFT JOIN invoiceItem ii ON i.invID = ii.itemID
        LEFT JOIN allItems ai ON ii.invoiceID = ai.itemID
        WHERE i.pID = %s
        GROUP BY i.invID, i.issueDate, i.totalAmount, i.insuranceShare, i.patientShare, i.isPaid
        ORDER BY i.issueDate DESC
    """
    return DatabaseConnection.execute_query(
        query,
        (patient_id,),
        fetch_all=True,
        fetch_dict=True
    )

def get_invoice_details(invoice_id, patient_id=None):
    query = """
        SELECT 
            i.invID,
            i.issueDate,
            i.totalAmount,
            i.insuranceShare,
            i.patientShare,
            i.isPaid,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            ii.itemID,
            ai.itemType,
            ai.description as item_description,
            CASE 
                WHEN ai.itemType = 'appointment' THEN (SELECT CONCAT(date, ' ', time)::TEXT FROM appointment WHERE appoID = i.appoID)
                WHEN ai.itemType = 'surgery' THEN (SELECT surgeryDate::TEXT FROM surgery WHERE surgeryID = i.surgeryID)
                WHEN ai.itemType = 'admission' THEN (SELECT createdAt::TEXT FROM admission WHERE admID = i.admID)
                WHEN ai.itemType = 'medicine' THEN (SELECT name::TEXT FROM request WHERE reqID = i.reqID)
                WHEN ai.itemType = 'test' THEN (SELECT name::TEXT FROM request WHERE reqID = i.reqID)
                ELSE NULL::TEXT
            END as item_reference
        FROM invoice i
        JOIN patient p ON i.pID = p.pID
        LEFT JOIN invoiceItem ii ON i.invID = ii.itemID
        LEFT JOIN allItems ai ON ii.invoiceID = ai.itemID
        WHERE i.invID = %s
    """
    params = [invoice_id]
    
    if patient_id:
        query += " AND i.pID = %s"
        params.append(patient_id)
    
    results = DatabaseConnection.execute_query(
        query,
        tuple(params),
        fetch_all=True,
        fetch_dict=True
    )
    
    if not results:
        return None
    
    invoice = {
        'invID': results[0]['invid'],
        'issueDate': results[0]['issuedate'],
        'totalAmount': results[0]['totalamount'],
        'insuranceShare': results[0]['insuranceshare'],
        'patientShare': results[0]['patientshare'],
        'isPaid': results[0]['ispaid'],
        'patient_name': results[0]['patient_name'],
        'nationalCode': results[0]['nationalcode'],
        'items': []
    }
    
    for row in results:
        if row['itemid']:
            invoice['items'].append({
                'itemID': row['itemid'],
                'itemType': row['itemtype'],
                'description': row['item_description'],
                'reference': row['item_reference']
            })
    
    return invoice

def get_all_invoices():
    query = """
        SELECT 
            i.invID,
            i.issueDate,
            i.totalAmount,
            i.insuranceShare,
            i.patientShare,
            i.isPaid,
            p.firstName || ' ' || p.lastName as patient_name,
            p.nationalCode,
            COUNT(ii.itemID) as item_count
        FROM invoice i
        JOIN patient p ON i.pID = p.pID
        LEFT JOIN invoiceItem ii ON i.invID = ii.itemID
        GROUP BY i.invID, i.issueDate, i.totalAmount, i.insuranceShare, i.patientShare, i.isPaid, p.firstName, p.lastName, p.nationalCode
        ORDER BY i.issueDate DESC
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )

def mark_invoice_paid(invoice_id):
    query = """
        UPDATE invoice
        SET isPaid = TRUE
        WHERE invID = %s
        RETURNING invID
    """
    result = DatabaseConnection.execute_query(
        query,
        (invoice_id,),
        fetch_one=True,
        commit=True
    )
    return result[0] if result else None

def get_all_allitems():
    query = """
        SELECT 
            itemID,
            itemType,
            description
        FROM allItems
        ORDER BY itemType
    """
    return DatabaseConnection.execute_query(
        query,
        fetch_all=True,
        fetch_dict=True
    )