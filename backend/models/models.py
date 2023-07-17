from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MRData(db.Model):
    __tablename__ = 'MR_data'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    service_type = db.Column(db.String(50))
    discussions = db.relationship('Discussion', backref='merge_request', lazy=True)

class Discussion(db.Model):
    __tablename__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    merge_request_id = db.Column(db.Integer, db.ForeignKey('MR_data.id'))
    defect_type_label = db.Column(db.String(50))
    defect_severity = db.Column(db.String(50))
    detail = db.Column(db.String(1000))
    create_date = db.Column(db.DateTime)
    resolve_date = db.Column(db.DateTime)
    detected_by = db.Column(db.String(50))
    resolved_by = db.Column(db.String(50))
