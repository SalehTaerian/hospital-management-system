from flask import Blueprint, request, jsonify, render_template
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