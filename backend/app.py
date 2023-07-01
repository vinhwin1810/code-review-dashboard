from flask import Flask
from models.models import db, MRData, Discussion
from controller.controller import bp
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Counterstrike123@localhost/MR_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

app.register_blueprint(bp, url_prefix='/')

# Create the database and tables
with app.app_context():
    db.create_all()
    # mr1 = MRData(
    # title="Merge Request 1",
    # author="John Doe",
    # service_type="Service 1",
    # defect_in_file_line="app.py: line 10",
    # defect_description="Fix a bug in the login functionality",
    # defect_type="Bug",
    # defect_severity="High",
    # create_date=datetime.now(),
    # resolve_date=datetime.now(),
    # detected_by="Jane Smith",
    # resolved_by="John Doe"
    # )

    # # Create discussions for the merge request
    # discussion1 = Discussion(
    #     defect_type_label="Security",
    #     defect_severity="Medium",
    #     detail="Discussing security implications of the bug fix"
    # )

    # discussion2 = Discussion(
    #     defect_type_label="Testing",
    #     defect_severity="Low",
    #     detail="Discussing testing approach for the bug fix"
    # )

    # # Associate the discussions with the merge request
    # mr1.discussions.append(discussion1)
    # mr1.discussions.append(discussion2)

    # # Add the merge request and discussions to the database
    # db.session.add(mr1)
    # db.session.commit()

with app.app_context():
    session = db.session

    # Query the MRData table to retrieve all records
    all_records = session.query(MRData).all()

    if all_records:
        # Records were found
        print("Data in MRData table:")
        for record in all_records:
            print(record)
    else:
        # No records found
        print("No data in MRData table.")

if __name__ == '__main__':
    app.run()











