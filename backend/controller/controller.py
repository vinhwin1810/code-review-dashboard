import os

from flask import jsonify, request
from models.models import MRData, Discussion, db
from datetime import datetime
from dateutil.parser import isoparse
from .helper import extract_info_from_title
from sqlalchemy import func
import requests

gitlab_url = os.getenv('GITLAB_URL')
gitlab_token = os.getenv('GITLAB_TOKEN')
headers = {"Private-Token": gitlab_token}

def fetch_merge_requests():

    project_ids = ["358"]

    for project_id in project_ids:
        page = 1
        while True:  # Loop for pagination
            mr_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests"
            params = {"scope": "all", "per_page": 100, "page": page}
            response = requests.get(mr_url, headers=headers, params=params, timeout=1000)
            merge_requests = response.json()

            if not merge_requests:  # No more merge requests, exit pagination loop
                break

            for mr in merge_requests:
                process_merge_request(mr, project_id, headers)
            
            page += 1  # Increment the page for the next loop iteration

        db.session.commit()

def process_merge_request(mr, project_id, headers):
    print(mr["iid"])
    service_type, general_info = extract_info_from_title(mr["title"])
    merge_request = MRData(
        title=general_info,
        author=mr["author"]["name"],
        service_type=service_type,
    )
    db.session.add(merge_request)

    # Fetch discussions for the merge request
    discussions_url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr['iid']}/discussions?per_page=100"
    discussions_response = requests.get(discussions_url, headers=headers)
    discussions = discussions_response.json()

    for discussion in discussions:
        process_discussion(discussion, merge_request)

def process_discussion(discussion, merge_request):
    info = discussion['notes'][0]
    body = discussion["notes"][0]["body"]
    
    if '~"CD::' in body and '~"DS::' in body:
        print(body)
        tmp = body.split('"')
        if not tmp:
            return
        
        description = "".join(tmp[4:])
        defect_type = tmp[1]
        defect_severity = tmp[3]
        created_date = info.get("created_at")
        resolved_date = info.get("updated_at") if info.get("resolved") else None
        detected_by = info["author"]["username"]
        resolved_by_info = info.get("resolved_by")
        resolved_by = resolved_by_info.get("username") if resolved_by_info else None

        note_data = Discussion(
            merge_request=merge_request,
            defect_type_label=defect_type,
            defect_severity=defect_severity,
            detail=description,
            create_date=isoparse(created_date),
            resolve_date=isoparse(resolved_date) if resolved_date else None,
            detected_by=detected_by,
            resolved_by=resolved_by or "none"
        )
        db.session.add(note_data)
        # Commit the changes to the database
        db.session.commit()


def get_merge_requests():
    try:
        merge_requests = MRData.query.all()
        output = []
        for mr in merge_requests:
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
            interval_range = func.year(Discussion.create_date)
        elif interval == 'Quarter':
            interval_range = func.concat(func.year(Discussion.create_date), '-', 
                                        func.ceil(func.month(Discussion.create_date) / 3))
        elif interval == 'Month':
            interval_range = func.concat(func.year(Discussion.create_date), '-', 
                                        func.month(Discussion.create_date))
        else:  # interval == 'Week'
            interval_range = func.concat(func.year(Discussion.create_date), '-',
                                        func.week(Discussion.create_date))
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

