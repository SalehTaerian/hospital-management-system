from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.services.analytics_service import *
from app.services.auth_service import is_logged_in

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

def is_authenticated():
    return is_logged_in()

@analytics_bp.route('/')
def index():
    if not is_authenticated():
        return redirect('/patient-login')
    return render_template('analytics/index.html')

@analytics_bp.route('/diseases')
def diseases():
    if not is_authenticated():
        return redirect('/patient-login')
    return render_template('analytics/diseases.html')

@analytics_bp.route('/disease/<int:disease_id>')
def disease_detail(disease_id):
    if not is_authenticated():
        return redirect('/patient-login')
    return render_template('analytics/disease_detail.html', disease_id=disease_id)

@analytics_bp.route('/api/disease/abundance', methods=['GET'])
def api_get_disease_abundance():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_disease_abundance_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/disease/medicines', methods=['GET'])
def api_get_disease_medicines():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    disease_id = request.args.get('disease_id', type=int)
    data = get_disease_medicine_effectiveness_service(disease_id)
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/disease/<int:disease_id>/details', methods=['GET'])
def api_get_disease_details(disease_id):
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_disease_details_service(disease_id)
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/top/diseases', methods=['GET'])
def api_get_top_diseases():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    limit = request.args.get('limit', 10, type=int)
    data = get_top_diseases_service(limit)
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/medicine/summary', methods=['GET'])
def api_get_medicine_summary():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_medicine_effectiveness_summary_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/disease/<int:disease_id>/timeline', methods=['GET'])
def api_get_disease_timeline(disease_id):
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_disease_timeline_service(disease_id)
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/stats', methods=['GET'])
def api_get_stats():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_overall_statistics_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/waiting-time', methods=['GET'])
def api_get_average_waiting_time():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_average_waiting_time_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/bed-occupancy', methods=['GET'])
def api_get_bed_occupancy():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_bed_occupancy_rate_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/readmission-rate', methods=['GET'])
def api_get_readmission_rate():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_readmission_rate_30_days_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/admission-time', methods=['GET'])
def api_get_average_admission_time():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_average_admission_time_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/admission-time/departments', methods=['GET'])
def api_get_admission_time_by_department():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = get_admission_time_by_department_service()
    return jsonify({'success': True, 'data': data})

@analytics_bp.route('/api/waiting-time/trend', methods=['GET'])
def api_get_waiting_time_trend():
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    days = request.args.get('days', 30, type=int)
    data = get_daily_waiting_time_trend_service(days)
    return jsonify({'success': True, 'data': data})