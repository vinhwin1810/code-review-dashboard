from flask import Flask
from models.models import db, MRData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Counterstrike123@localhost/MR_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)

# Create the database and tables
with app.app_context():
    db.create_all()

# Insert a sample record into the table
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
