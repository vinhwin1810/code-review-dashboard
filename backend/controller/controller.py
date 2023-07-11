from flask import jsonify, request
from models.models import MRData, Discussion, db
from gitlab import Gitlab
from datetime import datetime
from dateutil.parser import isoparse
from .helper import extract_info_from_title, extract_info_from_discussion
from sqlalchemy import func

def fetch_merge_requests():
    # Create a GitLab client instance
    gitlab_url = 'https://gitlab.com'
    gitlab_token = 'glpat-iKkxcphBJLKyzZdrTYMt'
    gl = Gitlab(gitlab_url, private_token=gitlab_token)

    # Fetch merge requests from the project
    project_id = '47457661'
    project = gl.projects.get(project_id)
    merge_requests = project.mergerequests.list(state='merged')

    for mr in merge_requests:
        # Extract the service type and general information from the title
        service_type, general_info = extract_info_from_title(mr.title)

        merge_request = MRData(
            title=general_info,
            author=mr.author['name'],
            service_type=service_type,
            create_date=isoparse(mr.created_at),
            resolve_date=isoparse(mr.merged_at),
        )
        db.session.add(merge_request)

        # Fetch discussions for the merge request
        discussions = mr.discussions.list()

        for discussion in discussions:
            # Extract the defect type label, defect severity, and detail from the discussion
            defect_type_label, defect_severity, detail = extract_info_from_discussion(discussion)

            discussion = Discussion(
                merge_request=merge_request,
                defect_type_label=defect_type_label,
                defect_severity=defect_severity,
                detail=detail
            )
            db.session.add(discussion)

    # Commit the changes to the database
    db.session.commit()

def get_merge_requests():
    try:
        merge_requests = MRData.query.all()
        output = []
        for mr in merge_requests:
            # Get all discussions associated with the merge request
            discussions = Discussion.query.filter_by(merge_request_id=mr.id).all()
            discussions_output = []
            for discussion in discussions:
                discussions_output.append({
                    'defect_type_label': discussion.defect_type_label,
                    'defect_severity': discussion.defect_severity,
                    'detail': discussion.detail
                })
            output.append({
                'title': mr.title,
                'author': mr.author,
                'service_type': mr.service_type,
                'create_date': mr.create_date.strftime('%Y-%m-%d %H:%M:%S') if mr.create_date else None,
                'resolve_date': mr.resolve_date.strftime('%Y-%m-%d %H:%M:%S') if mr.resolve_date else None,
                'defect_severity': mr.defect_severity,
                'detected_by': mr.detected_by,
                'discussions': discussions_output  # Include discussions here
            })
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_defects():
    try:
        interval = request.args.get('interval', default='Month', type=str)
        category = request.args.get('category', default='Author', type=str)

        if interval not in ['Year', 'Quarter', 'Month', 'Week'] or \
                category not in ['Author', 'Detected by', 'Defect Type', 'Defect Severity', 'Trending', 'Service']:
            return jsonify({'error': 'Invalid interval or category'})

        # Get the current date
        current_date = datetime.now()

        # Define the interval ranges based on the current date
        if interval == 'Year':
            interval_range = func.concat(func.year(MRData.create_date), '-', func.month(MRData.create_date))
        elif interval == 'Quarter' or interval == 'Month':
            interval_range = func.concat(func.year(MRData.create_date), '-', func.week(MRData.create_date))
        else:  # interval == 'Week'
            interval_range = func.concat(func.year(MRData.create_date), '-', func.month(MRData.create_date), '-', func.day(MRData.create_date))

        # Define a default value for group_by_column
        group_by_column = None

        # Build the query to fetch the defect data
        if category == 'Trending':
            query = db.session.query(interval_range.label('interval'), 
                                     func.count().label('count')). \
                filter(MRData.create_date <= current_date). \
                group_by(interval_range)
        else:
            if category == 'Author':
                group_by_column = MRData.author
            elif category == 'Detected by':
                group_by_column = MRData.detected_by
            elif category == 'Defect Type':
                group_by_column = MRData.defect_type
            elif category == 'Defect Severity':
                group_by_column = MRData.defect_severity
            elif category == 'Service':  # This is assuming that service_type is the relevant field for Service category
                group_by_column = MRData.service_type

            # Check if group_by_column is not None
            if group_by_column is None:
                return jsonify({'error': 'Invalid category'})

            query = db.session.query(interval_range.label('interval'), group_by_column.label('category'),
                                     func.count().label('count')). \
                filter(MRData.create_date <= current_date). \
                group_by(interval_range). \
                group_by(group_by_column)

        # Execute the query and fetch the results
        results = query.all()

        # Convert the results into a list of dictionaries
        if category == 'Trending':
            output = [{'interval': r.interval, 'count': r.count} for r in results]
        else:
            output = [{'interval': r.interval, 'category': r.category, 'count': r.count} for r in results]

        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)})

def get_merge_request_discussions(merge_request_id):
    try:
        # Query database for discussions associated with the merge_request_id
        discussions = Discussion.query.filter_by(merge_request_id=merge_request_id).all()
        
        # Serialize the discussions
        output = []
        for discussion in discussions:
            output.append({
                'defect_type_label': discussion.defect_type_label,
                'defect_severity': discussion.defect_severity,
                'detail': discussion.detail,
            })

        return jsonify(output)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
