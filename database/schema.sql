-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS case_updates CASCADE;
DROP TABLE IF EXISTS cases CASCADE;
DROP TABLE IF EXISTS officers CASCADE;
DROP TABLE IF EXISTS citizens CASCADE;

-- Citizens Table (NO national_id)
CREATE TABLE citizens (
    citizen_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Officers Table (NO badge changes - officers need badge numbers)
CREATE TABLE officers (
    officer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    badge_number VARCHAR(20) UNIQUE NOT NULL,
    rank VARCHAR(50) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    station VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cases Table (same)
CREATE TABLE cases (
    case_id SERIAL PRIMARY KEY,
    citizen_id INTEGER NOT NULL,
    officer_id INTEGER,
    crime_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Under Investigation', 'Resolved', 'Closed')),
    reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    FOREIGN KEY (citizen_id) REFERENCES citizens(citizen_id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES officers(officer_id) ON DELETE SET NULL
);

-- Case Updates Table (same)
CREATE TABLE case_updates (
    update_id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL,
    officer_id INTEGER NOT NULL,
    update_note TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES officers(officer_id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX idx_cases_citizen ON cases(citizen_id);
CREATE INDEX idx_cases_officer ON cases(officer_id);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_location ON cases(location);
CREATE INDEX idx_case_updates_case ON case_updates(case_id);