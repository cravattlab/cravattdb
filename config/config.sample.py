import yaml

UPLOAD_FOLDER = 'uploads'
CONVERT_URL = 'http://cravattwork.scripps.edu:5001'

#Flask-Security
SECRET_KEY = 'super-secret'

# Database settings
with open('config/database.yml', 'r') as f:
    database_settings = yaml.load(f)

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@postgres/{}'.format(
    database_settings['database']['environment']['DB_USER'],
    database_settings['database']['environment']['DB_PASS'],
    database_settings['database']['environment']['DB_NAME']
)