#!/usr/bin/env python3
"""
TikTok Bot Web Interface
Educational purposes only - Please respect TikTok's Terms of Service
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tiktok-bot-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables to track bot status
bot_status = {
    'running': False,
    'sent_count': 0,
    'current_url': '',
    'selected_service': '',
    'last_activity': '',
    'logs': []
}

def log_message(message):
    """Add a log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    bot_status['logs'].append(log_entry)
    bot_status['last_activity'] = timestamp
    
    # Keep only last 100 log entries
    if len(bot_status['logs']) > 100:
        bot_status['logs'] = bot_status['logs'][-100:]
    
    # Emit to all connected clients
    socketio.emit('log_update', {'message': log_entry, 'logs': bot_status['logs']})

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current bot status"""
    return jsonify(bot_status)

@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Handle configuration"""
    config_file = 'config.json'
    
    if request.method == 'GET':
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return jsonify(config)
        except FileNotFoundError:
            return jsonify({'link': ''})
    
    elif request.method == 'POST':
        config = request.json
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
        log_message(f"Configuration updated: {config.get('link', 'No URL')}")
        return jsonify({'success': True})

@app.route('/api/start', methods=['POST'])
def start_bot():
    """Start the bot"""
    if bot_status['running']:
        return jsonify({'error': 'Bot is already running'})
    
    data = request.json
    url = data.get('url', '')
    service = data.get('service', 'views')
    
    if not url:
        return jsonify({'error': 'URL is required'})
    
    bot_status['running'] = True
    bot_status['current_url'] = url
    bot_status['selected_service'] = service
    bot_status['sent_count'] = 0
    
    log_message(f"Starting bot for {service} on URL: {url}")
    
    # Start bot in a separate thread
    thread = threading.Thread(target=run_bot_simulation, args=(url, service))
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    bot_status['running'] = False
    log_message("Bot stopped by user")
    return jsonify({'success': True})

def run_bot_simulation(url, service):
    """Simulate bot running (for demo purposes)"""
    log_message(f"Bot simulation started for {service}")
    
    while bot_status['running']:
        try:
            # Simulate bot activity
            time.sleep(10)  # Wait 10 seconds between actions
            
            if bot_status['running']:
                bot_status['sent_count'] += 1
                log_message(f"Simulated {service} sent #{bot_status['sent_count']} to {url}")
                
                # Emit status update
                socketio.emit('status_update', bot_status)
                
        except Exception as e:
            log_message(f"Error in bot simulation: {str(e)}")
            break
    
    bot_status['running'] = False
    log_message("Bot simulation stopped")

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status_update', bot_status)
    emit('log_update', {'logs': bot_status['logs']})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Bot Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .warning {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-right: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn.stop {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }
        
        .status {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        
        .status-indicator.running {
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        
        .status-indicator.stopped {
            background: #f44336;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .logs {
            grid-column: 1 / -1;
        }
        
        .log-container {
            background: #1a1a1a;
            color: #00ff00;
            padding: 20px;
            border-radius: 10px;
            height: 300px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .log-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .log-container::-webkit-scrollbar-track {
            background: #333;
        }
        
        .log-container::-webkit-scrollbar-thumb {
            background: #666;
            border-radius: 4px;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            color: white;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 TikTok Bot Dashboard</h1>
            <p>Educational Demo - Please respect TikTok's Terms of Service</p>
        </div>
        
        <div class="warning">
            ⚠️ This is for educational purposes only. Using automation tools may violate TikTok's Terms of Service.
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="sent-count">0</div>
                <div class="stat-label">Actions Sent</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="status-text">Stopped</div>
                <div class="stat-label">Status</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="current-service">None</div>
                <div class="stat-label">Service</div>
            </div>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>🎯 Bot Configuration</h2>
                <div class="form-group">
                    <label for="tiktok-url">TikTok URL:</label>
                    <input type="url" id="tiktok-url" placeholder="https://www.tiktok.com/@username/video/123456789">
                </div>
                
                <div class="form-group">
                    <label for="service-type">Service Type:</label>
                    <select id="service-type">
                        <option value="views">👁️ Views</option>
                        <option value="followers">👥 Followers</option>
                        <option value="hearts">❤️ Hearts</option>
                        <option value="shares">📤 Shares</option>
                        <option value="favorites">⭐ Favorites</option>
                        <option value="comment_hearts">💬 Comment Hearts</option>
                    </select>
                </div>
                
                <button class="btn" onclick="startBot()">🚀 Start Bot</button>
                <button class="btn stop" onclick="stopBot()">⏹️ Stop Bot</button>
            </div>
            
            <div class="card">
                <h2>📊 Bot Status</h2>
                <div class="status">
                    <div class="status-indicator stopped" id="status-indicator"></div>
                    <span id="status-display">Bot is stopped</span>
                </div>
                
                <div class="form-group">
                    <label>Current URL:</label>
                    <div id="current-url" style="padding: 10px; background: #f5f5f5; border-radius: 5px; word-break: break-all;">
                        No URL set
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Last Activity:</label>
                    <div id="last-activity" style="padding: 10px; background: #f5f5f5; border-radius: 5px;">
                        Never
                    </div>
                </div>
            </div>
            
            <div class="card logs">
                <h2>📝 Activity Logs</h2>
                <div class="log-container" id="logs">
                    <div>Waiting for activity...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        
        // Socket event handlers
        socket.on('status_update', function(data) {
            updateStatus(data);
        });
        
        socket.on('log_update', function(data) {
            updateLogs(data.logs);
        });
        
        function updateStatus(status) {
            const indicator = document.getElementById('status-indicator');
            const display = document.getElementById('status-display');
            const sentCount = document.getElementById('sent-count');
            const statusText = document.getElementById('status-text');
            const currentService = document.getElementById('current-service');
            const currentUrl = document.getElementById('current-url');
            const lastActivity = document.getElementById('last-activity');
            
            if (status.running) {
                indicator.className = 'status-indicator running';
                display.textContent = 'Bot is running';
                statusText.textContent = 'Running';
            } else {
                indicator.className = 'status-indicator stopped';
                display.textContent = 'Bot is stopped';
                statusText.textContent = 'Stopped';
            }
            
            sentCount.textContent = status.sent_count;
            currentService.textContent = status.selected_service || 'None';
            currentUrl.textContent = status.current_url || 'No URL set';
            lastActivity.textContent = status.last_activity || 'Never';
        }
        
        function updateLogs(logs) {
            const logsContainer = document.getElementById('logs');
            logsContainer.innerHTML = logs.map(log => `<div>${log}</div>`).join('');
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }
        
        function startBot() {
            const url = document.getElementById('tiktok-url').value;
            const service = document.getElementById('service-type').value;
            
            if (!url) {
                alert('Please enter a TikTok URL');
                return;
            }
            
            fetch('/api/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    url: url,
                    service: service
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                }
            });
        }
        
        function stopBot() {
            fetch('/api/stop', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log('Bot stopped');
            });
        }
        
        // Load initial status
        fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                updateStatus(data);
                updateLogs(data.logs);
            });
        
        // Load saved configuration
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                if (data.link) {
                    document.getElementById('tiktok-url').value = data.link;
                }
            });
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    print("🚀 Starting TikTok Bot Web Interface...")
    print("📱 Access the dashboard at: https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")
    print("⚠️  This is for educational purposes only!")
    
    socketio.run(app, host='0.0.0.0', port=12000, debug=False, allow_unsafe_werkzeug=True)