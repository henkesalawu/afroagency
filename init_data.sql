- Create Dancers Table
CREATE TABLE IF NOT EXISTS dancers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(20),
    website VARCHAR(255)
);

-- Insert Sample Data into Dancers Table
INSERT INTO dancers (name, age, gender, phone, website)
VALUES
    ('Jessie Dance', 25, 'Female', '555-0123', 'http://jessdance.com'),
    ('Michael Moves', 30, 'Male', '555-0456', 'http://michae.com');

-- Create Events Table
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    date DATE NOT NULL
);

-- Insert Sample Data into Events Table
INSERT INTO events (name, address, date)
VALUES
    ('Afronation', '123 Main Street, City, Country', '2025-07-15'),
    ('Dance Beats', '456 Oak Avenue, NY, Country', '2024-11-01');