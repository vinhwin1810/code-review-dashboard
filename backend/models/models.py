from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MRData(db.Model):
    __tablename__ = 'MR_data'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    service_type = db.Column(db.String(50))
    defect_in_file_line = db.Column(db.String(50))
    defect_description = db.Column(db.String(200))
    defect_type = db.Column(db.String(50))
    defect_severity = db.Column(db.String(50))
    create_date = db.Column(db.DateTime)
    resolve_date = db.Column(db.DateTime)
    detected_by = db.Column(db.String(50))
    resolved_by = db.Column(db.String(50))
    discussions = db.relationship('Discussion', backref='merge_request', lazy=True)

    def __repr__(self):
        return f"<MRData(id='{self.id}', title='{self.title}', author='{self.author}', " \
               f"service_type='{self.service_type}', defect_in_file_line='{self.defect_in_file_line}', " \
               f"defect_description='{self.defect_description}', defect_type='{self.defect_type}', " \
               f"defect_severity='{self.defect_severity}', create_date='{self.create_date}', " \
               f"resolve_date='{self.resolve_date}', detected_by='{self.detected_by}', " \
               f"resolved_by='{self.resolved_by}')>"

class Discussion(db.Model):
    __tablename__ = 'discussions'
    id = db.Column(db.Integer, primary_key=True)
    merge_request_id = db.Column(db.Integer, db.ForeignKey('MR_data.id'))
    defect_type_label = db.Column(db.String(50))
    defect_severity = db.Column(db.String(50))
    detail = db.Column(db.String(1000))
