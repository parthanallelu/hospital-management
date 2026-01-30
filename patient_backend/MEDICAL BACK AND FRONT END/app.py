from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"status": "Medical Backend Running Successfully"}

# -------------------- MYSQL CONFIG --------------------

DB_USER = "root"          # change if different
DB_PASSWORD = "root"      # change to your MySQL password
DB_HOST = "Minion303"
DB_NAME = "medical_system"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "uploads"

db = SQLAlchemy(app)

# -------------------- MODELS --------------------

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))


class MedicalHistory(db.Model):
    __tablename__ = "medical_history"

    history_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    problem_description = db.Column(db.String(300))
    document_path = db.Column(db.String(200))


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer)
    medicine_name = db.Column(db.String(100))
    dosage = db.Column(db.String(100))
    instructions = db.Column(db.String(200))


class MedicineDelivery(db.Model):
    __tablename__ = "medicine_delivery"

    delivery_id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer)
    delivery_status = db.Column(db.String(30))
    delivery_date = db.Column(db.Date)


# -------------------- USER REGISTRATION --------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})


# -------------------- USER LOGIN --------------------

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(
        email=data["email"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({
            "message": "Login successful",
            "user_id": user.user_id,
            "role": user.role
        })

    return jsonify({"error": "Invalid credentials"}), 401


# -------------------- UPLOAD MEDICAL HISTORY --------------------

@app.route("/upload_history", methods=["POST"])
def upload_history():
    patient_id = request.form["patient_id"]
    description = request.form["description"]
    file = request.files["file"]

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    history = MedicalHistory(
        patient_id=patient_id,
        problem_description=description,
        document_path=filename
    )

    db.session.add(history)
    db.session.commit()

    return jsonify({"message": "Medical history uploaded"})


# -------------------- DOCTOR VIEW PATIENT HISTORY --------------------

@app.route("/view_history/<int:patient_id>", methods=["GET"])
def view_history(patient_id):
    records = MedicalHistory.query.filter_by(patient_id=patient_id).all()

    result = []
    for r in records:
        result.append({
            "problem": r.problem_description,
            "document": r.document_path
        })

    return jsonify(result)


# -------------------- ADD PRESCRIPTION --------------------

@app.route("/add_prescription", methods=["POST"])
def add_prescription():
    data = request.json

    prescription = Prescription(
        patient_id=data["patient_id"],
        doctor_id=data["doctor_id"],
        medicine_name=data["medicine_name"],
        dosage=data["dosage"],
        instructions=data["instructions"]
    )

    db.session.add(prescription)
    db.session.commit()

    delivery = MedicineDelivery(
        prescription_id=prescription.prescription_id,
        delivery_status="Pending"
    )

    db.session.add(delivery)
    db.session.commit()

    return jsonify({"message": "Prescription added"})


# -------------------- UPDATE MEDICINE DELIVERY --------------------

@app.route("/update_delivery/<int:prescription_id>", methods=["PUT"])
def update_delivery(prescription_id):
    delivery = MedicineDelivery.query.filter_by(
        prescription_id=prescription_id
    ).first()

    if not delivery:
        return jsonify({"error": "Prescription not found"}), 404

    delivery.delivery_status = "Delivered"
    db.session.commit()

    return jsonify({"message": "Medicine delivered"})


# -------------------- RUN SERVER --------------------

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.mkdir("uploads")

    app.run(debug=True)
