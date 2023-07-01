from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MRData(db.Model):
    __tablename__ = 'MR_data'
    drg_definition = db.Column(db.String(50))
    provider_id = db.Column(db.String(50), primary_key=True)
    provider_name = db.Column(db.String(50))
    provider_street_address = db.Column(db.String(50))
    provider_city = db.Column(db.String(50))
    provider_state = db.Column(db.String(50))
    provider_zip_code = db.Column(db.String(50))
    hospital_referral_region_description = db.Column(db.String(50))
    total_discharges = db.Column(db.String(50))
    average_covered_charges = db.Column(db.String(50))
    average_total_payments = db.Column(db.String(50))
    average_medicare_payments = db.Column(db.String(50))

    def __repr__(self):
        return f"<MRData(provider_id='{self.provider_id}', drg_definition='{self.drg_definition}', provider_name='{self.provider_name}', provider_street_address='{self.provider_street_address}', provider_city='{self.provider_city}', provider_state='{self.provider_state}', provider_zip_code='{self.provider_zip_code}', hospital_referral_region_description='{self.hospital_referral_region_description}', total_discharges='{self.total_discharges}', average_covered_charges='{self.average_covered_charges}', average_total_payments='{self.average_total_payments}', average_medicare_payments='{self.average_medicare_payments}')>"
