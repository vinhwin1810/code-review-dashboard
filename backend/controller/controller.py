import os

from flask import jsonify, request
from models.models import MRData, Discussion, db
from gitlab import Gitlab
from datetime import datetime
from dateutil.parser import isoparse
from .helper import extract_info_from_title, extract_info_from_note
from sqlalchemy import func

def fetch_merge_requests():
    # Create a GitLab client instance
    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_TOKEN')
    gl = Gitlab(gitlab_url, private_token=gitlab_token)

    # Fetch merge requests from the project
    project_ids = ["47457661"]
    for project_id in project_ids:
        project = gl.projects.get(project_id)
        merge_requests = project.mergerequests.list(state='merged')

        for mr in merge_requests:
            # Extract the service type and general information from the title
            service_type, general_info = extract_info_from_title(mr.title)
            merge_request = MRData(
                title=general_info,
                author=mr.author['name'],
                service_type=service_type,
            )
            db.session.add(merge_request)

            # Fetch discussions for the merge request
            discussions = mr.discussions.list(all=True)
            for discussion in discussions:
                notes = discussion.attributes.get('notes')

                for note in notes:
                    info = extract_info_from_note(note['body'])

                    if info:
                        print(note)
                        defect_type_label, defect_severity, detail = info
                        note_data = Discussion(
                            merge_request=merge_request,
                            defect_type_label=defect_type_label,
                            defect_severity=defect_severity,
                            detail=note['body'],
                            create_date=isoparse(note['created_at']),
                            resolve_date=discussion.attributes.get('resolved_at'),
                            detected_by=note['author']['username'],
                            resolved_by=discussion.attributes.get('resolved_by')
                        )
                        db.session.add(note_data)

        # Commit the changes to the database
        db.session.commit()


def get_merge_requests():
    try:
        merge_requests = MRData.query.all()
        output = []
        for mr in merge_requests:
            # Get all discussions associated with the merge request
            discussions = Discussion.query.filter_by(merge_request_id=mr.id).all()
            for discussion in discussions:
                output.append({
                'title': mr.title,
                'author': mr.author,
                'service_type': mr.service_type,
                'create_date': discussion.create_date.strftime('%Y-%m-%d %H:%M:%S') if discussion.create_date else None,
                'resolve_date': discussion.resolve_date.strftime('%Y-%m-%d %H:%M:%S') if discussion.resolve_date else None,
                'defect_severity': discussion.defect_severity,
                'detected_by': discussion.detected_by,
                'detail': discussion.detail
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
            interval_range = func.concat(func.year(Discussion.create_date), '-', func.month(Discussion.create_date))
        elif interval == 'Quarter' or interval == 'Month':
            interval_range = func.concat(func.year(Discussion.create_date), '-', func.week(Discussion.create_date))
        else:  # interval == 'Week'
            interval_range = func.concat(func.year(Discussion.create_date), '-', func.month(Discussion.create_date), '-', func.day(Discussion.create_date))

        # Define a default value for group_by_column
        group_by_column = None

        # Build the query to fetch the defect data
        if category == 'Trending':
            query = db.session.query(interval_range.label('interval'), 
                                     func.count().label('count')). \
                filter(Discussion.create_date <= current_date). \
                group_by(interval_range)
        else:
            if category == 'Author':
                group_by_column = MRData.author
            elif category == 'Detected by':
                group_by_column = Discussion.detected_by
            elif category == 'Defect Type':
                group_by_column = Discussion.defect_type_label
            elif category == 'Defect Severity':
                group_by_column = Discussion.defect_severity
            elif category == 'Service':
                group_by_column = MRData.service_type

            # Check if group_by_column is not None
            if group_by_column is None:
                return jsonify({'error': 'Invalid category'})

            query = db.session.query(interval_range.label('interval'), group_by_column.label('category'),
                                    func.count().label('count')). \
                join(Discussion.merge_request). \
                filter(Discussion.create_date <= current_date). \
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

