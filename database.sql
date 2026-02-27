CREATE DATABASE agri_db;
USE agri_db;

CREATE TABLE farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    land_size FLOAT
);

CREATE TABLE crops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT,
    crop_name VARCHAR(100),
    sowing_date DATE,
    FOREIGN KEY (farmer_id) REFERENCES farmers(id)
);
CREATE TABLE recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soil_type VARCHAR(100),
    rainfall FLOAT,
    temperature FLOAT,
    suggested_crop VARCHAR(100)
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);