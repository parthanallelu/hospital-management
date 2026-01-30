import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Smart Medical System",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Smart Medical Appointment & History System")
st.caption("Google Hackathon • Python-only Frontend")

menu = ["Login", "Register", "Upload Medical History", "View Patient History", "Add Prescription"]
choice = st.sidebar.selectbox("Select Module", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("📝 User Registration")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["patient", "doctor", "hospital"])

    if st.button("Register"):
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }
        )
        st.success(response.json()["message"])


# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"email": email, "password": password}
        )

        if response.status_code == 200:
            data = response.json()
            st.success(f"Welcome! Role: {data['role']}")
            st.session_state["user_id"] = data["user_id"]
            st.session_state["role"] = data["role"]
        else:
            st.error("Invalid credentials")


# ---------------- UPLOAD MEDICAL HISTORY ----------------
elif choice == "Upload Medical History":
    st.subheader("📄 Upload Medical History (Patient)")

    patient_id = st.number_input("Patient ID", min_value=1)
    description = st.text_area("Problem Description")
    file = st.file_uploader("Upload Medical Report")

    if st.button("Upload"):
        if file:
            files = {"file": file}
            data = {
                "patient_id": patient_id,
                "description": description
            }
            response = requests.post(
                f"{BACKEND_URL}/upload_history",
                data=data,
                files=files
            )
            st.success(response.json()["message"])
        else:
            st.warning("Please upload a file")


# ---------------- VIEW PATIENT HISTORY ----------------
elif choice == "View Patient History":
    st.subheader("👨‍⚕️ View Patient Medical History")

    patient_id = st.number_input("Patient ID", min_value=1)

    if st.button("View History"):
        response = requests.get(f"{BACKEND_URL}/view_history/{patient_id}")
        records = response.json()

        if records:
            for r in records:
                st.info(f"📝 {r['problem']} | 📎 {r['document']}")
        else:
            st.warning("No records found")


# ---------------- ADD PRESCRIPTION ----------------
elif choice == "Add Prescription":
    st.subheader("💊 Doctor Prescription")

    doctor_id = st.number_input("Doctor ID", min_value=1)
    patient_id = st.number_input("Patient ID", min_value=1)
    medicine = st.text_input("Medicine Name")
    dosage = st.text_input("Dosage")
    instructions = st.text_input("Instructions")

    if st.button("Add Prescription"):
        response = requests.post(
            f"{BACKEND_URL}/add_prescription",
            json={
                "doctor_id": doctor_id,
                "patient_id": patient_id,
                "medicine_name": medicine,
                "dosage": dosage,
                "instructions": instructions
            }
        )
        st.success(response.json()["message"])
