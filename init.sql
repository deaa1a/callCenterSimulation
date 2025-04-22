CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    execution_id UUID NOT NULL,
    priority INTEGER NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    assigned_agent_id UUID,
    assignment_date TIMESTAMP,
    resolution_date TIMESTAMP,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);
