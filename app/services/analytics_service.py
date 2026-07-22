from app.database.queries.analytics_queries import *

def get_disease_abundance_service():
    return get_disease_abundance()

def get_disease_medicine_effectiveness_service(disease_id=None):
    return get_disease_medicine_effectiveness(disease_id)

def get_disease_details_service(disease_id):
    return get_disease_details(disease_id)

def get_top_diseases_service(limit=10):
    return get_top_diseases(limit)

def get_medicine_effectiveness_summary_service():
    return get_medicine_effectiveness_summary()

def get_disease_timeline_service(disease_id):
    return get_disease_timeline(disease_id)

def get_overall_statistics_service():
    return get_overall_statistics()

from app.database.queries.analytics_queries import *

# ... existing functions ...

def get_average_waiting_time_service():
    return get_average_waiting_time()

def get_bed_occupancy_rate_service():
    return get_bed_occupancy_rate()

def get_readmission_rate_30_days_service():
    return get_readmission_rate_30_days()

def get_average_admission_time_service():
    return get_average_admission_time()

def get_admission_time_by_department_service():
    return get_admission_time_by_department()

def get_daily_waiting_time_trend_service(days=30):
    return get_daily_waiting_time_trend(days)