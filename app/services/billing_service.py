from app.database.queries.billing_queries import *

def get_patient_invoices_service(patient_id):
    return get_patient_invoices(patient_id)

def get_invoice_details_service(invoice_id, patient_id=None):
    invoice = get_invoice_details(invoice_id, patient_id)
    if not invoice:
        raise ValueError("Invoice not found")
    return invoice

def get_all_invoices_service():
    return get_all_invoices()

def mark_invoice_paid_service(invoice_id):
    result = mark_invoice_paid(invoice_id)
    if not result:
        raise ValueError("Invoice not found")
    return result

def get_all_allitems_service():
    return get_all_allitems()