from sqlalchemy import func, extract
from models.models import MRData

def group_by_author(query):
    return query.group_by(MRData.author)

def group_by_defect_type(query):
    return query.group_by(MRData.defect_type)

def group_by_defect_severity(query):
    return query.group_by(MRData.defect_severity)

def group_by_detected_by(query):
    return query.group_by(MRData.detected_by)

group_by_functions = {
    'Author': group_by_author,
    'Defect Type': group_by_defect_type,
    'Defect Severity': group_by_defect_severity,
    'Detected by': group_by_detected_by,
}

def interval_year(query):
    return query, func.count(MRData.id), extract('year', MRData.create_date)

def interval_quarter(query):
    return query, func.count(MRData.id), extract('quarter', MRData.create_date)

def interval_month(query):
    return query, func.count(MRData.id), extract('month', MRData.create_date)

def interval_week(query):
    return query, func.count(MRData.id), extract('week', MRData.create_date)

interval_functions = {
    'Year': interval_year,
    'Quarter': interval_quarter,
    'Month': interval_month,
    'Week': interval_week,
}

def extract_info_from_title(title):
    # Assuming the title is in the format "[Service] General information of merge request"
    parts = title.split('] ')
    service = parts[0][1:]  # Remove the opening bracket
    general_info = parts[1]
    return service, general_info

def extract_info_from_discussion(discussion):
    # Assuming the discussion is in the format "[Defect Type Label] [Defect Severity] Detail of discussion"
    parts = discussion.split('] ')
    defect_type_label = parts[0][1:]  # Remove the opening bracket
    defect_severity, detail = parts[1].split('] ')
    return defect_type_label, defect_severity, detail