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
        db.drop_all()
        db.create_all()
        fetch_data()

    return app

app = create_app('config.Config')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)













