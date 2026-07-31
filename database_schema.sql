CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);


CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL
);


CREATE TABLE policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    policy_number VARCHAR(100) UNIQUE NOT NULL,
    policy_type VARCHAR(100) NOT NULL,
    premium_amount FLOAT NOT NULL,
    coverage_amount FLOAT NOT NULL,
    policy_start_date DATE NOT NULL,
    policy_end_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'Active',

    FOREIGN KEY (customer_id)
        REFERENCES customers(id)
);


CREATE TABLE claims (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_id INTEGER NOT NULL,
    claim_amount FLOAT NOT NULL,
    claim_reason VARCHAR(255) NOT NULL,
    claim_date DATE NOT NULL,
    claim_status VARCHAR(30) NOT NULL DEFAULT 'Submitted',

    FOREIGN KEY (policy_id)
        REFERENCES policies(id)
);
