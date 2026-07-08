from app.database.queries.icd_queries import *


def get_all_icd_paginated(page=1, per_page=20):
    offset = (page - 1) * per_page
    items = get_all_icd(per_page, offset)
    total = get_icd_count()
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_icd_by_id_service(icd_id):
    return get_icd_by_id(icd_id)

def create_icd(data):
    return insert_icd(data)

def update_icd_service(icd_id, data):
    return update_icd(icd_id, data)

def delete_icd_service(icd_id):
    return delete_icd(icd_id)

def search_icd_service(search_term):
    return search_icd(search_term)


def get_all_icdm_paginated(page=1, per_page=20):
    offset = (page - 1) * per_page
    items = get_all_icdm(per_page, offset)
    total = get_icdm_count()
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_icdm_by_id_service(icdm_id):
    return get_icdm_by_id(icdm_id)

def create_icdm(data):
    return insert_icdm(data)

def update_icdm_service(icdm_id, data):
    return update_icdm(icdm_id, data)

def delete_icdm_service(icdm_id):
    return delete_icdm(icdm_id)

def search_icdm_service(search_term):
    return search_icdm(search_term)


def get_all_icdt_paginated(page=1, per_page=20):
    offset = (page - 1) * per_page
    items = get_all_icdt(per_page, offset)
    total = get_icdt_count()
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_icdt_by_id_service(icdt_id):
    return get_icdt_by_id(icdt_id)

def create_icdt(data):
    return insert_icdt(data)

def update_icdt_service(icdt_id, data):
    return update_icdt(icdt_id, data)

def delete_icdt_service(icdt_id):
    return delete_icdt(icdt_id)

def search_icdt_service(search_term):
    return search_icdt(search_term)


def get_all_icds_paginated(page=1, per_page=20):
    offset = (page - 1) * per_page
    items = get_all_icds(per_page, offset)
    total = get_icds_count()
    return {
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    }

def get_icds_by_id_service(icds_id):
    return get_icds_by_id(icds_id)

def create_icds(data):
    return insert_icds(data)

def update_icds_service(icds_id, data):
    return update_icds(icds_id, data)

def delete_icds_service(icds_id):
    return delete_icds(icds_id)

def search_icds_service(search_term):
    return search_icds(search_term)


def search_all_codes(search_term, code_type='all'):
    if not search_term or len(search_term) < 2:
        return []
    
    if code_type == 'icd':
        return search_icd(search_term)
    elif code_type == 'icdm':
        return search_icdm(search_term)
    elif code_type == 'icdt':
        return search_icdt(search_term)
    elif code_type == 'icds':
        return search_icds(search_term)
    else:
        results = []
        results.extend(search_icd(search_term))
        results.extend(search_icdm(search_term))
        results.extend(search_icdt(search_term))
        results.extend(search_icds(search_term))
        return results

def get_icd_dropdown():
    return get_all_icd_for_dropdown()

def get_all_signtypes_service():
    return get_all_signtypes()

def get_signtype_by_id_service(signtype_id):
    return get_signtype_by_id(signtype_id)

def create_signtype_service(data):
    if not data.get('name'):
        raise ValueError("Sign type name is required")
    return create_signtype(data)

def update_signtype_service(signtype_id, data):
    if not data.get('name'):
        raise ValueError("Sign type name is required")
    existing = get_signtype_by_id(signtype_id)
    if not existing:
        raise ValueError("Sign type not found")
    return update_signtype(signtype_id, data)

def delete_signtype_service(signtype_id):
    existing = get_signtype_by_id(signtype_id)
    if not existing:
        raise ValueError("Sign type not found")
    return delete_signtype(signtype_id)

def get_all_parameters_service():
    return get_all_parameters()

def get_parameter_by_id_service(parameter_id):
    return get_parameter_by_id(parameter_id)

def create_parameter_service(data):
    if not data.get('name'):
        raise ValueError("Parameter name is required")
    return create_parameter(data)

def update_parameter_service(parameter_id, data):
    if not data.get('name'):
        raise ValueError("Parameter name is required")
    existing = get_parameter_by_id(parameter_id)
    if not existing:
        raise ValueError("Parameter not found")
    return update_parameter(parameter_id, data)

def delete_parameter_service(parameter_id):
    existing = get_parameter_by_id(parameter_id)
    if not existing:
        raise ValueError("Parameter not found")
    return delete_parameter(parameter_id)

def get_all_equipment_service():
    return get_all_equipment()

def get_equipment_by_id_service(equip_id):
    return get_equipment_by_id(equip_id)

def create_equipment_service(data):
    if not data.get('name'):
        raise ValueError("Equipment name is required")
    return create_equipment(data)

def update_equipment_service(equip_id, data):
    if not data.get('name'):
        raise ValueError("Equipment name is required")
    existing = get_equipment_by_id(equip_id)
    if not existing:
        raise ValueError("Equipment not found")
    return update_equipment(equip_id, data)

def delete_equipment_service(equip_id):
    existing = get_equipment_by_id(equip_id)
    if not existing:
        raise ValueError("Equipment not found")
    return delete_equipment(equip_id)

def get_all_beds_service():
    return get_all_beds()

def get_bed_by_id_service(bed_id):
    return get_bed_by_id(bed_id)

def create_bed_service(data):
    return create_bed(data)

def update_bed_service(bed_id, data):
    existing = get_bed_by_id(bed_id)
    if not existing:
        raise ValueError("Bed not found")
    return update_bed(bed_id, data)

def delete_bed_service(bed_id):
    existing = get_bed_by_id(bed_id)
    if not existing:
        raise ValueError("Bed not found")
    return delete_bed(bed_id)

def get_all_signtypes_for_dropdown():
    return get_all_signtypes()

def get_all_bedinfo_service():
    return get_all_bedinfo()

def get_bedinfo_by_id_service(biID):
    return get_bedinfo_by_id(biID)

def create_bedinfo_service(data):
    if not data.get('bedID'):
        raise ValueError("Bed is required")
    if not data.get('roomID'):
        raise ValueError("Room is required")
    return create_bedinfo(data)

def update_bedinfo_service(biID, data):
    existing = get_bedinfo_by_id(biID)
    if not existing:
        raise ValueError("Bed info record not found")
    if not data.get('bedID'):
        raise ValueError("Bed is required")
    if not data.get('roomID'):
        raise ValueError("Room is required")
    return update_bedinfo(biID, data)

def delete_bedinfo_service(biID):
    existing = get_bedinfo_by_id(biID)
    if not existing:
        raise ValueError("Bed info record not found")
    return delete_bedinfo(biID)

def get_all_beds_for_dropdown_service():
    return get_all_beds_for_dropdown()

def get_all_admissions_for_dropdown_service():
    return get_all_admissions_for_dropdown()

def get_all_rooms_for_dropdown_service():
    return get_all_rooms_for_dropdown()