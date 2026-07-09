from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.billing_service import *
from app.services.auth_service import is_logged_in

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

def patient_login_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'patient'

def office_staff_required():
    if not is_logged_in():
        return False
    return session.get('user_role') == 'officeStaff'

@billing_bp.route('/patient')
def patient_billing():
    if not patient_login_required():
        return redirect('/patient-login')
    
    return render_template('patient/billing.html')

@billing_bp.route('/staff')
def staff_billing():
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('staff/billing.html')

@billing_bp.route('/staff/patient/<int:patient_id>')
def staff_patient_billing(patient_id):
    if not office_staff_required():
        return redirect('/staff-login')
    
    return render_template('staff/patient_billing.html', patient_id=patient_id)

@billing_bp.route('/api/invoices/patient', methods=['GET'])
def api_get_patient_invoices():
    if not patient_login_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    patient_id = session.get('user_id')
    invoices = get_patient_invoices_service(patient_id)
    return jsonify({'success': True, 'data': invoices})

@billing_bp.route('/api/invoices/patient/<int:patient_id>', methods=['GET'])
def api_get_patient_invoices_by_id(patient_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    invoices = get_patient_invoices_service(patient_id)
    return jsonify({'success': True, 'data': invoices})

@billing_bp.route('/api/invoices/all', methods=['GET'])
def api_get_all_invoices():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    invoices = get_all_invoices_service()
    return jsonify({'success': True, 'data': invoices})

@billing_bp.route('/api/invoices/<int:invoice_id>', methods=['GET'])
def api_get_invoice_details(invoice_id):
    if not is_logged_in():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    user_role = session.get('user_role')
    patient_id = None
    
    if user_role == 'patient':
        patient_id = session.get('user_id')
    
    try:
        invoice = get_invoice_details_service(invoice_id, patient_id)
        return jsonify({'success': True, 'data': invoice})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@billing_bp.route('/api/invoices/<int:invoice_id>/pay', methods=['POST'])
def api_mark_invoice_paid(invoice_id):
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    try:
        result = mark_invoice_paid_service(invoice_id)
        return jsonify({
            'success': True,
            'message': 'Invoice marked as paid',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@billing_bp.route('/api/allitems', methods=['GET'])
def api_get_allitems():
    if not office_staff_required():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    items = get_all_allitems_service()
    return jsonify({'success': True, 'data': items})