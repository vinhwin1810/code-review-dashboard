import json
import sys
sys.path.append('/Users/vinhpham/Desktop/code-review-dashboard/backend')
import unittest
from app import create_app
from datetime import datetime
from models.models import db, MRData, Discussion
from config import TestConfig

class TestGetMergeRequests(unittest.TestCase):
    def create_app(self):
        app = create_app(TestConfig)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            mr2 = MRData(
                title="Merge Request 5",
                author="Emma Davis",
                service_type="Service 2",
                defect_in_file_line="app.py: line 50",
                defect_description="Add unit tests for module X",
                defect_type="Testing",
                defect_severity="Medium",
                create_date=datetime.now(),
                resolve_date=datetime.now(),
                detected_by="Emma Davis",
                resolved_by="Emma Davis"
            )

            discussion1 = Discussion(
                defect_type_label="Testing",
                defect_severity="Medium",
                detail="Discussing test coverage for module X"
            )

            discussion2 = Discussion(
                defect_type_label="Unit Testing",
                defect_severity="Medium",
                detail="Discussing specific unit test cases"
            )

            mr2.discussions.append(discussion1)
            mr2.discussions.append(discussion2)

            db.session.add(mr2)
            db.session.commit()

        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_merge_requests(self):
        # Make the GET request
        response = self.client.get('/merge_requests')

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)  # We added one MR in the setUp
        self.assertEqual(data[0]['title'], 'Merge Request 5')
        self.assertEqual(len(data[0]['discussions']), 2)  # We added two discussions
        self.assertEqual(data[0]['discussions'][0]['defect_type_label'], 'Testing')
    
    def test_get_merge_request_discussions(self):
    # Make the GET request
        response = self.client.get('/merge_requests')

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data[0]['discussions']), 2)  # We added two discussions
        self.assertEqual(data[0]['discussions'][0]['defect_type_label'], 'Testing')
        self.assertEqual(data[0]['discussions'][0]['defect_severity'], 'Medium')
        self.assertEqual(data[0]['discussions'][0]['detail'], 'Discussing test coverage for module X')

    def test_get_defects(self):
    # Make the GET request
        response = self.client.get('/defects?interval=Month&category=Author')  # Update this with the correct route

        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

if __name__ == '__main__':
    unittest.main()
