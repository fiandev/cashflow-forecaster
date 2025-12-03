const ngrok = require('@ngrok/ngrok');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const BACKEND_PORT = 5000;
const FRONTEND_PORT = 5173;

let backendProcess;
let frontendProcess;
let backendTunnel;
let frontendTunnel;

async function startDevWithNgrok() {
    try {
        console.log('🚀 Starting ngrok tunnels...');

        // Start backend ngrok tunnel
        backendTunnel = await ngrok.connect({
            addr: BACKEND_PORT,
            authtoken: process.env.NGROK_AUTHTOKEN // Use authtoken from env if available
        });
        const backendNgrokUrl = backendTunnel.url();
        console.log(`Backend Ngrok URL: ${backendNgrokUrl}`);

        // Start frontend ngrok tunnel
        frontendTunnel = await ngrok.connect({
            addr: FRONTEND_PORT,
            authtoken: process.env.NGROK_AUTHTOKEN // Use authtoken from env if available
        });
        const frontendNgrokUrl = frontendTunnel.url();
        console.log(`Frontend Ngrok URL: ${frontendNgrokUrl}`);

        // Update frontend/.env with backend ngrok URL
        const envPath = path.resolve(__dirname, '../.env');
        let envContent = '';
        
        if (fs.existsSync(envPath)) {
            envContent = fs.readFileSync(envPath, 'utf8');
        }

        // Remove existing VITE_API_BASE_URL if present to avoid duplicates
        const newEnvContent = envContent.replace(/^VITE_API_BASE_URL=.*$/m, '') + `\nVITE_API_BASE_URL=${backendNgrokUrl}`;
        
        fs.writeFileSync(envPath, newEnvContent.trim());
        console.log(`Updated ${envPath} with VITE_API_BASE_URL=${backendNgrokUrl}`);

        // Start Backend (Python Flask)
        console.log('Starting Backend (Python Flask)...');
        
        // 1. Setup/Check Virtual Environment
        const backendDir = path.resolve(__dirname, '../../backend');
        const venvPath = path.join(backendDir, 'venv');
        const pythonExecutable = path.join(venvPath, 'bin', 'python');
        const pipExecutable = path.join(venvPath, 'bin', 'pip');

        if (!fs.existsSync(venvPath)) {
            console.log('Creating Python virtual environment...');
            const { execSync } = require('child_process');
            try {
                execSync('python3 -m venv venv', { cwd: backendDir, stdio: 'inherit' });
            } catch (e) {
                 console.error('Failed to create venv:', e);
                 cleanup();
            }
        }

        // 2. Install Dependencies
        console.log('Installing/Checking backend dependencies...');
        const { execSync } = require('child_process');
        try {
            execSync(`${pipExecutable} install -r requirements.txt`, { cwd: backendDir, stdio: 'inherit' });
        } catch (e) {
             console.error('Failed to install dependencies:', e);
             cleanup();
        }

        // 2.5 Initialize Database (Match Docker behavior)
        console.log('Initializing database (init_db.py)...');
        try {
            execSync(`${pythonExecutable} init_db.py`, { cwd: backendDir, stdio: 'inherit' });
        } catch (e) {
             console.error('Failed to initialize database:', e);
             cleanup();
        }

        // 3. Run App using venv python
        backendProcess = spawn(pythonExecutable, ['app.py'], {
            cwd: backendDir,
            stdio: 'inherit'
        });
        backendProcess.on('error', (err) => {
            console.error('Failed to start backend process:', err);
            cleanup();
        });
        backendProcess.on('exit', (code) => {
            console.log(`Backend process exited with code ${code}`);
            if (code !== 0) cleanup();
        });

        // Start Frontend (Bun Vite)
        console.log('Starting Frontend (Bun Vite)...');
        frontendProcess = spawn('bun', ['run', 'dev'], {
            cwd: path.resolve(__dirname, '..'), //frontend directory
            stdio: 'inherit' // Pipe output to parent process
        });
        frontendProcess.on('error', (err) => {
            console.error('Failed to start frontend process:', err);
            cleanup();
        });
        frontendProcess.on('exit', (code) => {
            console.log(`Frontend process exited with code ${code}`);
            if (code !== 0) cleanup();
        });

        console.log('\n----------------------------------------------------------------');
        console.log('✅ DEV ENVIRONMENT READY WITH NGROK');
        console.log('----------------------------------------------------------------');
        console.log('📱 Access from your Phone/Public Internet:');
        console.log(`   👉 Frontend: ${frontendNgrokUrl}`);
        console.log(`   👉 Backend:  ${backendNgrokUrl}`);
        console.log('');
        console.log('💻 Local Access:');
        console.log(`   👉 Frontend: http://localhost:${FRONTEND_PORT}`);
        console.log(`   👉 Backend:  http://localhost:${BACKEND_PORT}`);
        console.log('----------------------------------------------------------------');
        console.log('⌨️  Press Ctrl+C to stop everything.');
        console.log('----------------------------------------------------------------');

    } catch (error) {
        console.error('An error occurred:', error);
        cleanup();
    }
}

function cleanup() {
    console.log('\n🛑 Stopping all services...');
    if (frontendProcess) {
        console.log('Killing frontend process...');
        frontendProcess.kill('SIGINT');
    }
    if (backendProcess) {
        console.log('Killing backend process...');
        backendProcess.kill('SIGINT');
    }
    if (backendTunnel) {
        console.log('Closing backend ngrok tunnel...');
        backendTunnel.close();
    }
    if (frontendTunnel) {
        console.log('Closing frontend ngrok tunnel...');
        frontendTunnel.close();
    }
    
    console.log('Services stopped. Note: VITE_API_BASE_URL in .env is left as is.');
    process.exit();
}

// Listen for Ctrl+C
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

startDevWithNgrok();
