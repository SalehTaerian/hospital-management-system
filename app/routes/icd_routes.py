from flask import Blueprint, request, jsonify, render_template, session
from app.services.icd_service import *

icd_bp = Blueprint('icd', __name__, url_prefix='/icd')

@icd_bp.route('/manage')
def manage_icd():
    return render_template('icd/manage.html')

@icd_bp.route('/api/icd', methods=['GET'])
def api_get_icd():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    search = request.args.get('search', '')
    
    if search:
        results = search_icd_service(search)
        return jsonify({'success': True, 'data': results, 'total': len(results)})
    
    result = get_all_icd_paginated(page, per_page)
    return jsonify({
        'success': True,
        'data': result['items'],
        'total': result['total'],
        'page': result['page'],
        'pages': result['pages']
    })

@icd_bp.route('/api/icd', methods=['POST'])
def api_create_icd():
    data = request.get_json()
    icd_id = create_icd(data)
    return jsonify({'success': True, 'message': 'Created', 'id': icd_id})

@icd_bp.route('/api/icd/<int:icd_id>', methods=['PUT'])
def api_update_icd(icd_id):
    data = request.get_json()
    update_icd_service(icd_id, data)
    return jsonify({'success': True, 'message': 'Updated'})

@icd_bp.route('/api/icd/<int:icd_id>', methods=['DELETE'])
def api_delete_icd(icd_id):
    delete_icd_service(icd_id)
    return jsonify({'success': True, 'message': 'Deleted'})

@icd_bp.route('/api/icdm', methods=['GET'])
def api_get_icdm():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    search = request.args.get('search', '')
    
    if search:
        results = search_icdm_service(search)
        return jsonify({'success': True, 'data': results, 'total': len(results)})
    
    result = get_all_icdm_paginated(page, per_page)
    return jsonify({
        'success': True,
        'data': result['items'],
        'total': result['total'],
        'page': result['page'],
        'pages': result['pages']
    })

@icd_bp.route('/api/icdm', methods=['POST'])
def api_create_icdm():
    data = request.get_json()
    icdm_id = create_icdm(data)
    return jsonify({'success': True, 'message': 'Created', 'id': icdm_id})

@icd_bp.route('/api/icdm/<int:icdm_id>', methods=['PUT'])
def api_update_icdm(icdm_id):
    data = request.get_json()
    update_icdm_service(icdm_id, data)
    return jsonify({'success': True, 'message': 'Updated'})

@icd_bp.route('/api/icdm/<int:icdm_id>', methods=['DELETE'])
def api_delete_icdm(icdm_id):
    delete_icdm_service(icdm_id)
    return jsonify({'success': True, 'message': 'Deleted'})

@icd_bp.route('/api/icdt', methods=['GET'])
def api_get_icdt():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    search = request.args.get('search', '')
    
    if search:
        results = search_icdt_service(search)
        return jsonify({'success': True, 'data': results, 'total': len(results)})
    
    result = get_all_icdt_paginated(page, per_page)
    return jsonify({
        'success': True,
        'data': result['items'],
        'total': result['total'],
        'page': result['page'],
        'pages': result['pages']
    })

@icd_bp.route('/api/icdt', methods=['POST'])
def api_create_icdt():
    data = request.get_json()
    icdt_id = create_icdt(data)
    return jsonify({'success': True, 'message': 'Created', 'id': icdt_id})

@icd_bp.route('/api/icdt/<int:icdt_id>', methods=['PUT'])
def api_update_icdt(icdt_id):
    data = request.get_json()
    update_icdt_service(icdt_id, data)
    return jsonify({'success': True, 'message': 'Updated'})

@icd_bp.route('/api/icdt/<int:icdt_id>', methods=['DELETE'])
def api_delete_icdt(icdt_id):
    delete_icdt_service(icdt_id)
    return jsonify({'success': True, 'message': 'Deleted'})

@icd_bp.route('/api/icds', methods=['GET'])
def api_get_icds():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 100, type=int)
    search = request.args.get('search', '')
    
    if search:
        results = search_icds_service(search)
        return jsonify({'success': True, 'data': results, 'total': len(results)})
    
    result = get_all_icds_paginated(page, per_page)
    return jsonify({
        'success': True,
        'data': result['items'],
        'total': result['total'],
        'page': result['page'],
        'pages': result['pages']
    })

@icd_bp.route('/api/icds', methods=['POST'])
def api_create_icds():
    data = request.get_json()
    icds_id = create_icds(data)
    return jsonify({'success': True, 'message': 'Created', 'id': icds_id})

@icd_bp.route('/api/icds/<int:icds_id>', methods=['PUT'])
def api_update_icds(icds_id):
    data = request.get_json()
    update_icds_service(icds_id, data)
    return jsonify({'success': True, 'message': 'Updated'})

@icd_bp.route('/api/icds/<int:icds_id>', methods=['DELETE'])
def api_delete_icds(icds_id):
    delete_icds_service(icds_id)
    return jsonify({'success': True, 'message': 'Deleted'})

@icd_bp.route('/api/dropdown/icd', methods=['GET'])
def api_get_icd_dropdown():
    results = get_icd_dropdown()
    return jsonify({'success': True, 'data': results})

@icd_bp.route('/api/icd/<int:icd_id>', methods=['GET'])
def api_get_icd_by_id(icd_id):
    result = get_icd_by_id_service(icd_id)
    return jsonify({'success': True, 'data': result})

@icd_bp.route('/api/icdm/<int:icdm_id>', methods=['GET'])
def api_get_icdm_by_id(icdm_id):
    result = get_icdm_by_id_service(icdm_id)
    return jsonify({'success': True, 'data': result})

@icd_bp.route('/api/icdt/<int:icdt_id>', methods=['GET'])
def api_get_icdt_by_id(icdt_id):
    result = get_icdt_by_id_service(icdt_id)
    return jsonify({'success': True, 'data': result})

@icd_bp.route('/api/icds/<int:icds_id>', methods=['GET'])
def api_get_icds_by_id(icds_id):
    result = get_icds_by_id_service(icds_id)
    return jsonify({'success': True, 'data': result})

@icd_bp.route('/api/signtypes', methods=['GET'])
def api_get_signtypes():
    results = get_all_signtypes_service()
    return jsonify({'success': True, 'data': results})

@icd_bp.route('/api/signtypes/<int:signtype_id>', methods=['GET'])
def api_get_signtype(signtype_id):
    try:
        result = get_signtype_by_id_service(signtype_id)
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@icd_bp.route('/api/signtypes', methods=['POST'])
def api_create_signtype():
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        signtype_id = create_signtype_service(data)
        return jsonify({
            'success': True,
            'message': 'Sign type created successfully',
            'id': signtype_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/signtypes/<int:signtype_id>', methods=['PUT'])
def api_update_signtype(signtype_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        result = update_signtype_service(signtype_id, data)
        return jsonify({
            'success': True,
            'message': 'Sign type updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/signtypes/<int:signtype_id>', methods=['DELETE'])
def api_delete_signtype(signtype_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        result = delete_signtype_service(signtype_id)
        return jsonify({
            'success': True,
            'message': 'Sign type deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/parameters', methods=['GET'])
def api_get_parameters():
    results = get_all_parameters_service()
    return jsonify({'success': True, 'data': results})

@icd_bp.route('/api/parameters/<int:parameter_id>', methods=['GET'])
def api_get_parameter(parameter_id):
    try:
        result = get_parameter_by_id_service(parameter_id)
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@icd_bp.route('/api/parameters', methods=['POST'])
def api_create_parameter():
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        parameter_id = create_parameter_service(data)
        return jsonify({
            'success': True,
            'message': 'Parameter created successfully',
            'id': parameter_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/parameters/<int:parameter_id>', methods=['PUT'])
def api_update_parameter(parameter_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        result = update_parameter_service(parameter_id, data)
        return jsonify({
            'success': True,
            'message': 'Parameter updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/parameters/<int:parameter_id>', methods=['DELETE'])
def api_delete_parameter(parameter_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        result = delete_parameter_service(parameter_id)
        return jsonify({
            'success': True,
            'message': 'Parameter deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    
@icd_bp.route('/api/equipment', methods=['GET'])
def api_get_equipment():
    results = get_all_equipment_service()
    return jsonify({'success': True, 'data': results})

@icd_bp.route('/api/equipment/<int:equip_id>', methods=['GET'])
def api_get_equipment_by_id(equip_id):
    try:
        result = get_equipment_by_id_service(equip_id)
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@icd_bp.route('/api/equipment', methods=['POST'])
def api_create_equipment():
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        equip_id = create_equipment_service(data)
        return jsonify({
            'success': True,
            'message': 'Equipment created successfully',
            'id': equip_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/equipment/<int:equip_id>', methods=['PUT'])
def api_update_equipment(equip_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        result = update_equipment_service(equip_id, data)
        return jsonify({
            'success': True,
            'message': 'Equipment updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/equipment/<int:equip_id>', methods=['DELETE'])
def api_delete_equipment(equip_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        result = delete_equipment_service(equip_id)
        return jsonify({
            'success': True,
            'message': 'Equipment deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/beds', methods=['GET'])
def api_get_beds():
    results = get_all_beds_service()
    return jsonify({'success': True, 'data': results})

@icd_bp.route('/api/beds/<int:bed_id>', methods=['GET'])
def api_get_bed_by_id(bed_id):
    try:
        result = get_bed_by_id_service(bed_id)
        return jsonify({'success': True, 'data': result})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@icd_bp.route('/api/beds', methods=['POST'])
def api_create_bed():
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        bed_id = create_bed_service(data)
        return jsonify({
            'success': True,
            'message': 'Bed created successfully',
            'id': bed_id
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/beds/<int:bed_id>', methods=['PUT'])
def api_update_bed(bed_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        data = request.get_json()
        result = update_bed_service(bed_id, data)
        return jsonify({
            'success': True,
            'message': 'Bed updated successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/beds/<int:bed_id>', methods=['DELETE'])
def api_delete_bed(bed_id):
    if session.get('user_role') != 'officeStaff':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        result = delete_bed_service(bed_id)
        return jsonify({
            'success': True,
            'message': 'Bed deleted successfully',
            'id': result
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@icd_bp.route('/api/signtypes/dropdown', methods=['GET'])
def api_get_signtypes_dropdown():
    results = get_all_signtypes_for_dropdown()
    return jsonify({'success': True, 'data': results})