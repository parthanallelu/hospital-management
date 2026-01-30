/* ================================
   DATABASE CREATION
   ================================ */

CREATE DATABASE medical_system;
USE medical_system;


/* ================================
   USERS TABLE
   Stores Patients, Doctors, Hospitals
   ================================ */

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('patient', 'doctor', 'hospital'))
);


/* ================================
   MEDICAL HISTORY TABLE
   ================================ */

CREATE TABLE medical_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    problem_description VARCHAR(300),
    document_path VARCHAR(200),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(user_id)
);


/* ================================
   APPOINTMENTS TABLE
   ================================ */

CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    problem_description VARCHAR(300),
    status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (patient_id) REFERENCES users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES users(user_id)
);


/* ================================
   PRESCRIPTIONS TABLE
   ================================ */

CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    medicine_name VARCHAR(100),
    dosage VARCHAR(100),
    instructions VARCHAR(200),
    issued_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (patient_id) REFERENCES users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES users(user_id)
);


/* ================================
   MEDICINE DELIVERY TABLE
   ================================ */

CREATE TABLE medicine_delivery (
    delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    prescription_id INT NOT NULL,
    delivery_status VARCHAR(30) DEFAULT 'Pending',
    delivery_date DATE,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
);


/* ================================
   SAMPLE DATA INSERTION
   ================================ */

/* USERS */
INSERT INTO users (name, email, password, role) VALUES
('Ashish Trivedi', 'ashish@gmail.com', '1234', 'patient'),
('Dr. Rahul Sharma', 'rahul@gmail.com', 'doctor123', 'doctor'),
('City Hospital', 'hospital@gmail.com', 'hospital123', 'hospital');


/* MEDICAL HISTORY */
INSERT INTO medical_history (patient_id, problem_description, document_path) VALUES
(1, 'Fever and headache', 'fever_report.pdf'),
(1, 'Blood test report', 'blood_test.pdf');


/* APPOINTMENT */
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, problem_description) VALUES
(1, 2, '2026-02-01', '10:30:00', 'High fever for 3 days');


/* PRESCRIPTION */
INSERT INTO prescriptions (patient_id, doctor_id, medicine_name, dosage, instructions) VALUES
(1, 2, 'Paracetamol', 'Morning & Night', 'After food'),
(1, 2, 'Vitamin C', 'Once daily', 'After breakfast');


/* MEDICINE DELIVERY */
INSERT INTO medicine_delivery (prescription_id, delivery_status, delivery_date) VALUES
(1, 'Delivered', '2026-02-01'),
(2, 'Pending', NULL);


/* ================================
   IMPORTANT QUERIES (FOR VIVA)
   ================================ */

/* View Patient Medical History */
SELECT * FROM medical_history WHERE patient_id = 1;

/* Doctor Views Patient Records */
SELECT u.name, m.problem_description, m.document_path
FROM users u
JOIN medical_history m ON u.user_id = m.patient_id;

/* Check Appointments */
SELECT * FROM appointments;

/* View Prescriptions with Delivery Status */
SELECT p.medicine_name, p.dosage, d.delivery_status
FROM prescriptions p
JOIN medicine_delivery d
ON p.prescription_id = d.prescription_id;
