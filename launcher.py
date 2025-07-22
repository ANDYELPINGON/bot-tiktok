#!/usr/bin/env python3
"""
TikTok Bot Launcher
Simple script to manage the bot applications
"""

import subprocess
import sys
import time
import signal
import os

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎵 TikTok Bot Launcher 🎵                  ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  🚀 Basic Dashboard:    Port 12000                           ║
    ║  🔧 Advanced Dashboard: Port 12001                           ║
    ║                                                              ║
    ║  📱 Access URLs:                                             ║
    ║  • Basic:    https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev ║
    ║  • Advanced: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev ║
    ║                                                              ║
    ║  ⚠️  Educational purposes only!                              ║
    ║  Please respect TikTok's Terms of Service                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def main():
    print_banner()
    
    print("\n🔧 Available options:")
    print("1. 🚀 Start Basic Dashboard (Port 12000)")
    print("2. 🔧 Start Advanced Dashboard (Port 12001)")
    print("3. 🚀🔧 Start Both Dashboards")
    print("4. 📊 Check Status")
    print("5. ⏹️  Stop All")
    print("6. 🔄 Restart All")
    print("7. 📝 View Logs")
    print("8. ❌ Exit")
    
    while True:
        try:
            choice = input("\n👉 Select option (1-8): ").strip()
            
            if choice == '1':
                start_basic()
            elif choice == '2':
                start_advanced()
            elif choice == '3':
                start_both()
            elif choice == '4':
                check_status()
            elif choice == '5':
                stop_all()
            elif choice == '6':
                restart_all()
            elif choice == '7':
                view_logs()
            elif choice == '8':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please choose 1-8.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def start_basic():
    print("🚀 Starting Basic Dashboard...")
    subprocess.Popen([sys.executable, 'web_app.py'], 
                    stdout=open('web_app.log', 'w'), 
                    stderr=subprocess.STDOUT)
    time.sleep(2)
    print("✅ Basic Dashboard started on port 12000")
    print("📱 Access: https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")

def start_advanced():
    print("🔧 Starting Advanced Dashboard...")
    subprocess.Popen([sys.executable, 'advanced_web_app.py'], 
                    stdout=open('advanced_web_app.log', 'w'), 
                    stderr=subprocess.STDOUT)
    time.sleep(2)
    print("✅ Advanced Dashboard started on port 12001")
    print("📱 Access: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")

def start_both():
    print("🚀🔧 Starting both dashboards...")
    start_basic()
    time.sleep(1)
    start_advanced()
    print("✅ Both dashboards are now running!")

def check_status():
    print("📊 Checking application status...")
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    
    basic_running = 'web_app.py' in result.stdout
    advanced_running = 'advanced_web_app.py' in result.stdout
    
    print(f"🚀 Basic Dashboard:    {'✅ Running' if basic_running else '❌ Stopped'}")
    print(f"🔧 Advanced Dashboard: {'✅ Running' if advanced_running else '❌ Stopped'}")
    
    if basic_running or advanced_running:
        print("\n📱 Access URLs:")
        if basic_running:
            print("• Basic:    https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")
        if advanced_running:
            print("• Advanced: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev")

def stop_all():
    print("⏹️  Stopping all applications...")
    subprocess.run(['pkill', '-f', 'web_app.py'], capture_output=True)
    subprocess.run(['pkill', '-f', 'advanced_web_app.py'], capture_output=True)
    time.sleep(2)
    print("✅ All applications stopped")

def restart_all():
    print("🔄 Restarting all applications...")
    stop_all()
    time.sleep(2)
    start_both()
    print("✅ All applications restarted")

def view_logs():
    print("📝 Available logs:")
    print("1. Basic Dashboard Log")
    print("2. Advanced Dashboard Log")
    
    choice = input("Select log to view (1-2): ").strip()
    
    if choice == '1':
        if os.path.exists('web_app.log'):
            print("\n--- Basic Dashboard Log ---")
            with open('web_app.log', 'r') as f:
                print(f.read()[-2000:])  # Last 2000 characters
        else:
            print("❌ Basic dashboard log not found")
    elif choice == '2':
        if os.path.exists('advanced_web_app.log'):
            print("\n--- Advanced Dashboard Log ---")
            with open('advanced_web_app.log', 'r') as f:
                print(f.read()[-2000:])  # Last 2000 characters
        else:
            print("❌ Advanced dashboard log not found")
    else:
        print("❌ Invalid choice")

if __name__ == '__main__':
    main()