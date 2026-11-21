CREATE DATABASE IF NOT EXISTS campus_study_finder;
USE campus_study_finder;
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Final sprint: tables for each student's courses, preferences, and weekly availability.
CREATE TABLE IF NOT EXISTS user_courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  course_code VARCHAR(30) NOT NULL,
  UNIQUE KEY unique_user_course (user_id, course_code),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS study_preferences (
  user_id INT PRIMARY KEY,
  study_style VARCHAR(30) NOT NULL,
  meeting_type VARCHAR(30) NOT NULL,
  group_size VARCHAR(30) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS user_availability (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  day VARCHAR(12) NOT NULL,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
