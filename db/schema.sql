CREATE DATABASE IF NOT EXISTS hospital_bot;
USE hospital_bot;

CREATE TABLE IF NOT EXISTS intents (
  intent_id INT AUTO_INCREMENT PRIMARY KEY, tag VARCHAR(50) UNIQUE);
CREATE TABLE IF NOT EXISTS patterns (
  id INT AUTO_INCREMENT PRIMARY KEY, intent_id INT, pattern TEXT,
  FOREIGN KEY (intent_id) REFERENCES intents(intent_id));
CREATE TABLE IF NOT EXISTS responses (
  id INT AUTO_INCREMENT PRIMARY KEY, intent_id INT, response TEXT,
  FOREIGN KEY (intent_id) REFERENCES intents(intent_id));

CREATE TABLE IF NOT EXISTS departments (
  dept_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(80) UNIQUE);
CREATE TABLE IF NOT EXISTS doctors (
  doctor_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), dept_id INT,
  consult_fee DECIMAL(8,2), available_days VARCHAR(50),
  FOREIGN KEY (dept_id) REFERENCES departments(dept_id));
CREATE TABLE IF NOT EXISTS patients (
  patient_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100),
  phone VARCHAR(15) UNIQUE);
CREATE TABLE IF NOT EXISTS appointments (
  appt_id INT AUTO_INCREMENT PRIMARY KEY, patient_id INT, doctor_id INT,
  appt_date DATE, appt_time TIME,
  status ENUM('booked','cancelled','completed') DEFAULT 'booked',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  -- only 'booked' rows take part in the unique key, so cancelled slots can be rebooked
  active_slot TIME GENERATED ALWAYS AS (IF(status='booked', appt_time, NULL)) STORED,
  UNIQUE KEY no_double_booking (doctor_id, appt_date, active_slot),
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
  FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id));

CREATE TABLE IF NOT EXISTS messages (
  msg_id INT AUTO_INCREMENT PRIMARY KEY, session_id VARCHAR(40),
  user_text TEXT, predicted_intent VARCHAR(50), confidence FLOAT,
  bot_reply TEXT, feedback TINYINT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
