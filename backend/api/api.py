from apscheduler.schedulers.background import BackgroundScheduler
from flask import jsonify, request, Blueprint
from controller.controller import fetch_merge_requests, get_merge_requests, get_defects, get_merge_request_discussions

# Create the database and tables
bp = Blueprint('controller', __name__)

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@bp.route('/', methods=['GET'])
def home():
   return jsonify({'message': 'MR Data API'})

scheduler.add_job(fetch_merge_requests, 'interval', days=1)

@bp.route('/merge_requests', methods=['GET'])
def api_get_merge_requests():
    return get_merge_requests()

@bp.route('/defects', methods=['GET'])
def api_get_defects():
    return get_defects()