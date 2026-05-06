-- This script runs when PostgreSQL container starts

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data for validation
INSERT INTO users (username, email, password) 
VALUES ('testuser', 'test@example.com', 'testpass123')
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, password) 
VALUES ('admin', 'admin@example.com', 'admin123')
ON CONFLICT (username) DO NOTHING;
