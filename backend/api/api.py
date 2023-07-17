
from flask import jsonify, Blueprint
from controller.controller import fetch_merge_requests, get_merge_requests, get_defects

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

bp = Blueprint('controller', __name__)

def fetch_data():
    fetch_merge_requests() #DELETE THIS LINE AFTER RUNNING ONCE
    scheduler = BackgroundScheduler()

# Schedule the function to run every day at 00:00 (midnight)
    scheduler.add_job(
    func=fetch_merge_requests,
    trigger=IntervalTrigger(days=1),
    id='fetch_job',
    name='Fetch merge requests from GitLab every day',
    replace_existing=True)

    # Start the scheduler
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

@bp.route('/', methods=['GET'])
def home():
   return jsonify({'message': 'MR Data API'})

@bp.route('/merge_requests', methods=['GET'])
def api_get_merge_requests():
    return get_merge_requests()

@bp.route('/defects', methods=['GET'])
def api_get_defects():
    return get_defects()