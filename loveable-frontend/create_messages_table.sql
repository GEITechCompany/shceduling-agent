-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    content TEXT NOT NULL,
    client_id UUID REFERENCES clients(id),
    agent_id UUID REFERENCES agents(id),
    status VARCHAR(50) DEFAULT 'sent',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Enable Row Level Security
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policy to allow clients to read their own messages
CREATE POLICY "Clients can read their own messages"
    ON messages FOR SELECT
    USING (auth.uid() = client_id);

-- Create policy to allow clients to insert their own messages
CREATE POLICY "Clients can insert their own messages"
    ON messages FOR INSERT
    WITH CHECK (auth.uid() = client_id);

-- Create policy to allow agents to read messages assigned to them
CREATE POLICY "Agents can read their assigned messages"
    ON messages FOR SELECT
    USING (auth.uid() = agent_id);

-- Create policy to allow agents to update their assigned messages
CREATE POLICY "Agents can update their assigned messages"
    ON messages FOR UPDATE
    USING (auth.uid() = agent_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_messages_updated_at
    BEFORE UPDATE ON messages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 