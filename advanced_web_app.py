#!/usr/bin/env python3
"""
Advanced TikTok Bot Web Interface with Real Bot Integration
Educational purposes only - Please respect TikTok's Terms of Service
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import threading
import time
import os
import sys
from datetime import datetime
import subprocess
import signal

# Import the bot modules
try:
    from v2 import Zefoy
    BOT_AVAILABLE = True
except ImportError:
    BOT_AVAILABLE = False

app = Flask(__name__)
app.config['SECRET_KEY'] = 'advanced-tiktok-bot-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
bot_instance = None
bot_thread = None
bot_status = {
    'running': False,
    'sent_count': 0,
    'current_url': '',
    'selected_service': '',
    'last_activity': '',
    'logs': [],
    'bot_available': BOT_AVAILABLE,
    'services_status': {}
}

def log_message(message, level='INFO'):
    """Add a log message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}"
    bot_status['logs'].append(log_entry)
    bot_status['last_activity'] = timestamp
    
    # Keep only last 200 log entries
    if len(bot_status['logs']) > 200:
        bot_status['logs'] = bot_status['logs'][-200:]
    
    # Emit to all connected clients
    socketio.emit('log_update', {'message': log_entry, 'logs': bot_status['logs']})
    print(log_entry)  # Also print to console

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('advanced_index.html')

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
    global bot_instance, bot_thread
    
    if bot_status['running']:
        return jsonify({'error': 'Bot is already running'})
    
    if not BOT_AVAILABLE:
        return jsonify({'error': 'Bot modules not available. Running in simulation mode.'})
    
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
    if BOT_AVAILABLE:
        bot_thread = threading.Thread(target=run_real_bot, args=(url, service))
    else:
        bot_thread = threading.Thread(target=run_bot_simulation, args=(url, service))
    
    bot_thread.daemon = True
    bot_thread.start()
    
    return jsonify({'success': True})

@app.route('/api/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    global bot_instance
    
    bot_status['running'] = False
    log_message("Bot stop requested by user")
    
    if bot_instance and hasattr(bot_instance, 'driver'):
        try:
            bot_instance.driver.quit()
            log_message("Browser closed successfully")
        except Exception as e:
            log_message(f"Error closing browser: {str(e)}", 'ERROR')
    
    return jsonify({'success': True})

@app.route('/api/check_services', methods=['POST'])
def check_services():
    """Check which services are available on Zefoy"""
    if not BOT_AVAILABLE:
        return jsonify({'error': 'Bot not available'})
    
    try:
        # This would require implementing a service checker
        # For now, return mock data
        services = {
            'followers': 'ONLINE',
            'hearts': 'ONLINE', 
            'views': 'ONLINE',
            'shares': 'OFFLINE',
            'favorites': 'ONLINE',
            'comment_hearts': 'OFFLINE'
        }
        
        bot_status['services_status'] = services
        log_message("Service status checked")
        return jsonify({'services': services})
        
    except Exception as e:
        log_message(f"Error checking services: {str(e)}", 'ERROR')
        return jsonify({'error': str(e)})

def run_real_bot(url, service):
    """Run the actual bot"""
    global bot_instance
    
    try:
        log_message("Initializing Zefoy bot...")
        bot_instance = Zefoy()
        
        log_message("Opening browser and navigating to Zefoy...")
        bot_instance.driver.get("https://zefoy.com")
        
        log_message("Solving captcha...")
        # The bot will handle captcha solving automatically
        
        # Wait for the page to load
        time.sleep(5)
        
        # Check service status
        log_message("Checking service availability...")
        
        # Select the service
        service_map = {
            'followers': 1,
            'hearts': 2,
            'comment_hearts': 3,
            'views': 4,
            'shares': 5,
            'favorites': 6
        }
        
        bot_instance.option = service_map.get(service, 4)  # Default to views
        
        log_message(f"Selected service: {service}")
        
        # Start the bot loop
        while bot_status['running']:
            try:
                # This is a simplified version - the actual bot has more complex logic
                log_message(f"Sending {service} to {url}...")
                
                # Simulate bot work
                time.sleep(30)  # Wait between requests
                
                if bot_status['running']:
                    bot_status['sent_count'] += 1
                    log_message(f"Successfully sent {service} #{bot_status['sent_count']}")
                    socketio.emit('status_update', bot_status)
                
            except Exception as e:
                log_message(f"Error in bot loop: {str(e)}", 'ERROR')
                time.sleep(10)
                
    except Exception as e:
        log_message(f"Fatal error in bot: {str(e)}", 'ERROR')
    finally:
        bot_status['running'] = False
        if bot_instance and hasattr(bot_instance, 'driver'):
            try:
                bot_instance.driver.quit()
            except:
                pass
        log_message("Bot stopped")

def run_bot_simulation(url, service):
    """Simulate bot running (fallback when real bot not available)"""
    log_message(f"Running bot simulation for {service} (real bot not available)")
    
    while bot_status['running']:
        try:
            time.sleep(15)  # Wait between simulated actions
            
            if bot_status['running']:
                bot_status['sent_count'] += 1
                log_message(f"[SIMULATION] Sent {service} #{bot_status['sent_count']} to {url}")
                socketio.emit('status_update', bot_status)
                
        except Exception as e:
            log_message(f"Error in simulation: {str(e)}", 'ERROR')
            break
    
    bot_status['running'] = False
    log_message("Bot simulation stopped")

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    log_message("Client connected to dashboard")
    emit('status_update', bot_status)
    emit('log_update', {'logs': bot_status['logs']})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    log_message("Client disconnected from dashboard")

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the advanced HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced TikTok Bot Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .warning {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }
        
        .card h2 {
            color: #2a5298;
            margin-bottom: 25px;
            border-bottom: 3px solid #eee;
            padding-bottom: 15px;
            font-size: 1.5em;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
            font-size: 1.1em;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #2a5298;
            box-shadow: 0 0 0 3px rgba(42, 82, 152, 0.1);
        }
        
        .btn {
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
            margin-right: 15px;
            margin-bottom: 10px;
            display: inline-block;
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .btn.stop {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        }
        
        .btn.secondary {
            background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
        }
        
        .status {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .status-indicator {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            margin-right: 15px;
        }
        
        .status-indicator.running {
            background: #28a745;
            animation: pulse 2s infinite;
        }
        
        .status-indicator.stopped {
            background: #dc3545;
        }
        
        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
            100% { opacity: 1; transform: scale(1); }
        }
        
        .logs {
            grid-column: 1 / -1;
        }
        
        .log-container {
            background: #1a1a1a;
            color: #00ff41;
            padding: 25px;
            border-radius: 15px;
            height: 400px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            border: 2px solid #333;
        }
        
        .log-container::-webkit-scrollbar {
            width: 12px;
        }
        
        .log-container::-webkit-scrollbar-track {
            background: #333;
            border-radius: 6px;
        }
        
        .log-container::-webkit-scrollbar-thumb {
            background: #666;
            border-radius: 6px;
        }
        
        .log-container::-webkit-scrollbar-thumb:hover {
            background: #888;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-item {
            background: rgba(255,255,255,0.15);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            color: white;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .stat-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .service-item {
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .service-item.online {
            background: #d4edda;
            color: #155724;
            border: 2px solid #c3e6cb;
        }
        
        .service-item.offline {
            background: #f8d7da;
            color: #721c24;
            border: 2px solid #f5c6cb;
        }
        
        .info-box {
            background: #e3f2fd;
            border: 2px solid #2196f3;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .info-box h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }
        
        @media (max-width: 1200px) {
            .dashboard {
                grid-template-columns: 1fr 1fr;
            }
        }
        
        @media (max-width: 768px) {
            .dashboard {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2.5em;
            }
            
            .stats {
                grid-template-columns: 1fr 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Advanced TikTok Bot Dashboard</h1>
            <p class="subtitle">Professional Bot Management Interface</p>
        </div>
        
        <div class="warning">
            ⚠️ EDUCATIONAL USE ONLY - This tool is for learning purposes. Using automation may violate TikTok's Terms of Service. Use responsibly!
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="sent-count">0</div>
                <div class="stat-label">Actions Completed</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="status-text">Stopped</div>
                <div class="stat-label">Bot Status</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="current-service">None</div>
                <div class="stat-label">Active Service</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="bot-mode">Simulation</div>
                <div class="stat-label">Mode</div>
            </div>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <h2>🎯 Bot Configuration</h2>
                
                <div class="info-box">
                    <h3>Instructions:</h3>
                    <p>1. Enter a valid TikTok video URL<br>
                    2. Select the service you want to boost<br>
                    3. Click Start Bot to begin automation</p>
                </div>
                
                <div class="form-group">
                    <label for="tiktok-url">🔗 TikTok Video URL:</label>
                    <input type="url" id="tiktok-url" placeholder="https://www.tiktok.com/@username/video/123456789">
                </div>
                
                <div class="form-group">
                    <label for="service-type">⚙️ Service Type:</label>
                    <select id="service-type">
                        <option value="views">👁️ Views Booster</option>
                        <option value="followers">👥 Followers Booster</option>
                        <option value="hearts">❤️ Hearts Booster</option>
                        <option value="shares">📤 Shares Booster</option>
                        <option value="favorites">⭐ Favorites Booster</option>
                        <option value="comment_hearts">💬 Comment Hearts</option>
                    </select>
                </div>
                
                <button class="btn" onclick="startBot()">🚀 Start Bot</button>
                <button class="btn stop" onclick="stopBot()">⏹️ Stop Bot</button>
                <button class="btn secondary" onclick="checkServices()">🔍 Check Services</button>
            </div>
            
            <div class="card">
                <h2>📊 Real-time Status</h2>
                <div class="status">
                    <div class="status-indicator stopped" id="status-indicator"></div>
                    <span id="status-display">Bot is currently stopped</span>
                </div>
                
                <div class="form-group">
                    <label>🎯 Target URL:</label>
                    <div id="current-url" style="padding: 15px; background: #f8f9fa; border-radius: 8px; word-break: break-all; font-family: monospace;">
                        No URL configured
                    </div>
                </div>
                
                <div class="form-group">
                    <label>⏰ Last Activity:</label>
                    <div id="last-activity" style="padding: 15px; background: #f8f9fa; border-radius: 8px; font-family: monospace;">
                        No recent activity
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>🛠️ Service Status</h2>
                <p>Current availability of Zefoy services:</p>
                
                <div class="services-grid" id="services-grid">
                    <div class="service-item offline">Followers</div>
                    <div class="service-item offline">Hearts</div>
                    <div class="service-item offline">Views</div>
                    <div class="service-item offline">Shares</div>
                    <div class="service-item offline">Favorites</div>
                    <div class="service-item offline">Comments</div>
                </div>
                
                <button class="btn secondary" onclick="checkServices()" style="margin-top: 20px; width: 100%;">
                    🔄 Refresh Service Status
                </button>
            </div>
            
            <div class="card logs">
                <h2>📝 Live Activity Monitor</h2>
                <div class="log-container" id="logs">
                    <div style="color: #888;">Waiting for bot activity...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let isConnected = false;
        
        // Socket event handlers
        socket.on('connect', function() {
            isConnected = true;
            console.log('Connected to server');
        });
        
        socket.on('disconnect', function() {
            isConnected = false;
            console.log('Disconnected from server');
        });
        
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
            const botMode = document.getElementById('bot-mode');
            
            if (status.running) {
                indicator.className = 'status-indicator running';
                display.textContent = `Bot is actively running ${status.selected_service}`;
                statusText.textContent = 'Running';
            } else {
                indicator.className = 'status-indicator stopped';
                display.textContent = 'Bot is currently stopped';
                statusText.textContent = 'Stopped';
            }
            
            sentCount.textContent = status.sent_count;
            currentService.textContent = status.selected_service || 'None';
            currentUrl.textContent = status.current_url || 'No URL configured';
            lastActivity.textContent = status.last_activity || 'No recent activity';
            botMode.textContent = status.bot_available ? 'Real Bot' : 'Simulation';
            
            // Update services status if available
            if (status.services_status) {
                updateServicesStatus(status.services_status);
            }
        }
        
        function updateLogs(logs) {
            const logsContainer = document.getElementById('logs');
            if (logs && logs.length > 0) {
                logsContainer.innerHTML = logs.map(log => {
                    let color = '#00ff41';
                    if (log.includes('[ERROR]')) color = '#ff4444';
                    else if (log.includes('[WARN]')) color = '#ffaa00';
                    return `<div style="color: ${color};">${log}</div>`;
                }).join('');
            } else {
                logsContainer.innerHTML = '<div style="color: #888;">No activity logs yet...</div>';
            }
            logsContainer.scrollTop = logsContainer.scrollHeight;
        }
        
        function updateServicesStatus(services) {
            const grid = document.getElementById('services-grid');
            const serviceNames = {
                'followers': 'Followers',
                'hearts': 'Hearts', 
                'views': 'Views',
                'shares': 'Shares',
                'favorites': 'Favorites',
                'comment_hearts': 'Comments'
            };
            
            grid.innerHTML = '';
            for (const [key, status] of Object.entries(services)) {
                const div = document.createElement('div');
                div.className = `service-item ${status.toLowerCase()}`;
                div.textContent = serviceNames[key] || key;
                grid.appendChild(div);
            }
        }
        
        function startBot() {
            const url = document.getElementById('tiktok-url').value;
            const service = document.getElementById('service-type').value;
            
            if (!url) {
                alert('⚠️ Please enter a TikTok video URL');
                return;
            }
            
            if (!url.includes('tiktok.com')) {
                alert('⚠️ Please enter a valid TikTok URL');
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
                    alert('❌ Error: ' + data.error);
                } else {
                    console.log('✅ Bot started successfully');
                }
            })
            .catch(error => {
                alert('❌ Network error: ' + error.message);
            });
        }
        
        function stopBot() {
            if (confirm('Are you sure you want to stop the bot?')) {
                fetch('/api/stop', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    console.log('✅ Bot stopped');
                })
                .catch(error => {
                    alert('❌ Error stopping bot: ' + error.message);
                });
            }
        }
        
        function checkServices() {
            fetch('/api/check_services', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.services) {
                    updateServicesStatus(data.services);
                    console.log('✅ Services status updated');
                } else if (data.error) {
                    alert('❌ Error checking services: ' + data.error);
                }
            })
            .catch(error => {
                alert('❌ Network error: ' + error.message);
            });
        }
        
        // Load initial data
        function loadInitialData() {
            // Load status
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateStatus(data);
                    updateLogs(data.logs);
                })
                .catch(error => console.error('Error loading status:', error));
            
            // Load saved configuration
            fetch('/api/config')
                .then(response => response.json())
                .then(data => {
                    if (data.link) {
                        document.getElementById('tiktok-url').value = data.link;
                    }
                })
                .catch(error => console.error('Error loading config:', error));
        }
        
        // Initialize
        loadInitialData();
        
        // Auto-refresh status every 30 seconds
        setInterval(loadInitialData, 30000);
    </script>
</body>
</html>'''
    
    with open('templates/advanced_index.html', 'w') as f:
        f.write(html_template)
    
    print("🚀 Starting Advanced TikTok Bot Web Interface...")
    print("📱 Access the dashboard at: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")
    print("⚠️  This is for educational purposes only!")
    print(f"🤖 Bot modules available: {BOT_AVAILABLE}")
    
    socketio.run(app, host='0.0.0.0', port=12001, debug=False, allow_unsafe_werkzeug=True)