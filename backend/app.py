from flask import Flask
from models.models import db, MRData, Discussion
from api.api import bp
from datetime import datetime
from flask_cors import CORS
from flask_migrate import Migrate
from api.api import fetch_data

def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    app.register_blueprint(bp, url_prefix='/')

    # Create the database and tables
    with app.app_context():
        db.create_all()
        fetch_data()

        # mr5 = MRData(
        # title="Merge Request 5",
        # author="Emma Davis",
        # service_type="Service 2",
        # defect_in_file_line="app.py: line 50",
        # defect_description="Add unit tests for module X",
        # defect_type="Testing",
        # defect_severity="Medium",
        # create_date=datetime.now(),
        # resolve_date=datetime.now(),
        # detected_by="Emma Davis",
        # resolved_by="Emma Davis"
        # )

        # discussion1 = Discussion(
        #     defect_type_label="Testing",
        #     defect_severity="Medium",
        #     detail="Discussing test coverage for module X"
        # )

        # discussion2 = Discussion(
        #     defect_type_label="Unit Testing",
        #     defect_severity="Medium",
        #     detail="Discussing specific unit test cases"
        # )

        # mr5.discussions.append(discussion1)
        # mr5.discussions.append(discussion2)

        # db.session.add(mr5)
        # db.session.commit()

    return app

app = create_app('config.Config')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)













