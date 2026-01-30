from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from app import create_app, db
from app.models import User, DoctorProfile, PatientProfile

app = create_app()

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'DoctorProfile': DoctorProfile, 'PatientProfile': PatientProfile}

if __name__ == '__main__':
    app.run(debug=True, port=5000)
