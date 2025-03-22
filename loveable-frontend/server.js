const express = require('express');
const path = require('path');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
const port = 5001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// Scheduling agent process
let schedulingAgent = null;
let isProcessingMessage = false;

// Start scheduling agent
function startSchedulingAgent() {
    if (schedulingAgent) {
        return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
        schedulingAgent = spawn('python3', ['../scheduling_agent.py'], {
            stdio: ['pipe', 'pipe', 'pipe'],
            env: {
                ...process.env,
                PYTHONUNBUFFERED: '1'
            }
        });

        let initialized = false;

        schedulingAgent.stdout.on('data', (data) => {
            const output = data.toString();
            console.log(`Scheduling Agent: ${output}`);
            
            if (!initialized && output.includes('Welcome to the AI Scheduling Assistant')) {
                initialized = true;
                resolve();
            }
        });

        schedulingAgent.stderr.on('data', (data) => {
            console.error(`Scheduling Agent Error: ${data}`);
        });

        schedulingAgent.on('close', (code) => {
            console.log(`Scheduling Agent process exited with code ${code}`);
            schedulingAgent = null;
            if (!initialized) {
                reject(new Error('Scheduling agent failed to start'));
            }
        });

        // Timeout for initialization
        setTimeout(() => {
            if (!initialized) {
                reject(new Error('Timeout waiting for scheduling agent to start'));
            }
        }, 10000);
    });
}

// Chat API endpoint
app.post('/api/chat', async (req, res) => {
    try {
        const { message } = req.body;
        
        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        // Wait if another message is being processed
        while (isProcessingMessage) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        isProcessingMessage = true;

        if (!schedulingAgent) {
            await startSchedulingAgent();
        }

        // Send message to scheduling agent
        schedulingAgent.stdin.write(message + '\n');

        // Wait for response
        const response = await new Promise((resolve, reject) => {
            let output = '';
            let responseReceived = false;
            
            const timeout = setTimeout(() => {
                if (!responseReceived) {
                    isProcessingMessage = false;
                    reject(new Error('Timeout waiting for scheduling agent response'));
                }
            }, 30000);

            const messageHandler = (data) => {
                const text = data.toString();
                if (text.includes('What would you like to do?') || text.includes('> ')) {
                    return;
                }
                output = text.trim();
                responseReceived = true;
                clearTimeout(timeout);
                schedulingAgent.stdout.removeListener('data', messageHandler);
                resolve(output);
            };

            schedulingAgent.stdout.on('data', messageHandler);
        });

        isProcessingMessage = false;
        res.json({ response });

    } catch (error) {
        isProcessingMessage = false;
        console.error('Error:', error);
        res.status(500).json({ 
            error: 'Failed to process request',
            message: error.message 
        });
    }
});

// Start server
app.listen(port, async () => {
    console.log(`API Server is running on http://localhost:${port}`);
    try {
        await startSchedulingAgent();
        console.log('Scheduling agent started successfully');
    } catch (error) {
        console.error('Failed to start scheduling agent:', error);
    }
}); 