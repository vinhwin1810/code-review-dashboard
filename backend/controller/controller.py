from flask import jsonify, request, Blueprint
from models.models import MRData, Discussion

# Create the database and tables
bp = Blueprint('controller', __name__)

@bp.route('/', methods=['GET'])
def home():
    return "<h1>MR Data</h1><p>This site is a prototype API for MR Data.</p>"

@bp.route('/defects/trend', methods=['GET'])
def get_defect_trend():
    # Query the MRData table to retrieve the defects and their create dates
    defects = MRData.query.all()

    # Process the data to calculate the defect trend based on the desired interval
    defect_trend_data = {
        'year': {},
        'quarter': {},
        'month': {},
        'week': {}
    }

    for defect in defects:
        # Extract the year, quarter, month, and week from the create_date
        year = defect.create_date.year
        quarter = (defect.create_date.month - 1) // 3 + 1
        month = defect.create_date.month
        week = defect.create_date.isocalendar()[1]

        # Count the defects for each interval
        if year in defect_trend_data['year']:
            defect_trend_data['year'][year] += 1
        else:
            defect_trend_data['year'][year] = 1

        if quarter in defect_trend_data['quarter']:
            defect_trend_data['quarter'][quarter] += 1
        else:
            defect_trend_data['quarter'][quarter] = 1

        if month in defect_trend_data['month']:
            defect_trend_data['month'][month] += 1
        else:
            defect_trend_data['month'][month] = 1

        if week in defect_trend_data['week']:
            defect_trend_data['week'][week] += 1
        else:
            defect_trend_data['week'][week] = 1

    # Return the defect trend data as a JSON response
    return jsonify(defect_trend_data)


@bp.route('/defects/categories', methods=['GET'])
def get_defect_categories():
    # Query the MRData table to retrieve defect categories
    defect_categories = MRData.query.with_entities(
        MRData.author, MRData.detected_by, MRData.defect_type, MRData.defect_severity).all()

    # Process the data to calculate defect categories based on the desired interval
    defect_categories_data = {
        'year': {},
        'quarter': {},
        'month': {},
        'week': {}
    }

    for author, detected_by, defect_type, defect_severity in defect_categories:
        # Group the defect categories by author, detected by, defect type, and defect severity
        if author not in defect_categories_data['year']:
            defect_categories_data['year'][author] = {}
        if detected_by not in defect_categories_data['year'][author]:
            defect_categories_data['year'][author][detected_by] = {}
        if defect_type not in defect_categories_data['year'][author][detected_by]:
            defect_categories_data['year'][author][detected_by][defect_type] = {}
        if defect_severity not in defect_categories_data['year'][author][detected_by][defect_type]:
            defect_categories_data['year'][author][detected_by][defect_type][defect_severity] = 0

        # Count the defects for each interval and category
        defect_categories_data['year'][author][detected_by][defect_type][defect_severity] += 1

    # Return the defect categories data as a JSON response
    return jsonify(defect_categories_data)

@bp.route('/merge-requests', methods=['GET'])
def get_merge_requests():
    # Query the MRData table to retrieve all merge requests
    merge_requests = MRData.query.all()

    # Convert the merge requests to a JSON representation
    merge_request_data = []
    for mr in merge_requests:
        merge_request_data.append({
            'id': mr.id,
            'title': mr.title,
            'author': mr.author,
            'service_type': mr.service_type,
            'defect_in_file_line': mr.defect_in_file_line,
            'defect_description': mr.defect_description,
            'defect_type': mr.defect_type,
            'defect_severity': mr.defect_severity,
            'create_date': mr.create_date,
            'resolve_date': mr.resolve_date,
            'detected_by': mr.detected_by,
            'resolved_by': mr.resolved_by,
        })

    return jsonify(merge_request_data)


@bp.route('/merge-requests/<mr_id>/discussions', methods=['GET'])
def get_merge_request_discussions(mr_id):
    # Query the MRData table to retrieve the specified merge request
    merge_request = MRData.query.filter_by(id=mr_id).first()

    if merge_request is None:
        return jsonify({'error': 'Merge request not found'})

    # Extract the discussions from the merge request
    discussions = extract_discussions(merge_request)

    # Convert the discussions to a JSON representation
    discussions_data = []
    for discussion in discussions:
        discussions_data.append({
            'defect_type_label': discussion.defect_type_label,
            'defect_severity': discussion.defect_severity,
            'detail': discussion.detail,
        })

    return jsonify(discussions_data)

def extract_discussions(merge_request):
    discussions = []
    for discussion in merge_request.discussions:
        discussions.append(Discussion(
            defect_type_label=discussion.defect_type_label,
            defect_severity=discussion.defect_severity,
            detail=discussion.detail
        ))
    return discussions


