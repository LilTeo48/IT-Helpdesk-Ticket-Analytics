
CREATE TABLE IF NOT EXISTS helpdesk_tickets (
    ticket_id INTEGER PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    technician VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    resolution_hours NUMERIC(10, 2),

    CONSTRAINT valid_priority
        CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),

    CONSTRAINT valid_status
        CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),

    CONSTRAINT valid_resolution_date
        CHECK (resolved_at IS NULL OR resolved_at >= created_at),

    CONSTRAINT valid_resolution_hours
        CHECK (resolution_hours IS NULL OR resolution_hours >= 0)
);
