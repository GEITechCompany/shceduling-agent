-- Insert a sample client
INSERT INTO clients (name, email, phone, address) VALUES
    ('Anna Wong', 'anna.wong@example.com', '555-0123', '123 Main St'),
    ('John Smith', 'john.smith@example.com', '555-0124', '456 Oak Ave'),
    ('Sarah Johnson', 'sarah.j@example.com', '555-0125', '789 Pine Rd')
ON CONFLICT DO NOTHING; 