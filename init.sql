CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    execution_id UUID NOT NULL,
    priority INTEGER NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    assigned_agent_id UUID,
    assignment_date TIMESTAMP,
    resolution_date TIMESTAMP,
    resolution_time NUMERIC(10, 3),
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
);


CREATE TABLE agents (
    id UUID PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL
);