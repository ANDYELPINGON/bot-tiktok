#!/usr/bin/env python3
"""
Quick status check for TikTok Bot Web Interface
"""

import requests
import subprocess
import sys
from datetime import datetime

def check_status():
    print("🔍 TikTok Bot Status Check")
    print("=" * 50)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check processes
    print("📊 Process Status:")
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    
    basic_running = 'web_app.py' in result.stdout
    advanced_running = 'advanced_web_app.py' in result.stdout
    
    print(f"  🚀 Basic Dashboard:    {'✅ Running' if basic_running else '❌ Stopped'}")
    print(f"  🔧 Advanced Dashboard: {'✅ Running' if advanced_running else '❌ Stopped'}")
    print()
    
    # Check HTTP endpoints
    print("🌐 HTTP Status:")
    
    try:
        response = requests.get('http://localhost:12000', timeout=5)
        print(f"  📱 Basic (Port 12000):    ✅ {response.status_code}")
    except Exception as e:
        print(f"  📱 Basic (Port 12000):    ❌ Error: {str(e)[:50]}")
    
    try:
        response = requests.get('http://localhost:12001', timeout=5)
        print(f"  📱 Advanced (Port 12001): ✅ {response.status_code}")
    except Exception as e:
        print(f"  📱 Advanced (Port 12001): ❌ Error: {str(e)[:50]}")
    
    print()
    
    # Show access URLs
    if basic_running or advanced_running:
        print("🔗 Access URLs:")
        if basic_running:
            print("  • Basic:    https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")
        if advanced_running:
            print("  • Advanced: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")
    else:
        print("❌ No applications running. Use 'python launcher.py' to start.")
    
    print()
    print("=" * 50)

if __name__ == '__main__':
    check_status()