# 🎵 TikTok Bot Web Interface

## 🚀 Live Demo

Your TikTok bot is now running with two web interfaces:

### 📱 Access URLs:
- **Basic Dashboard**: https://work-1-qazbknukhcfpkhdv.prod-runtime.all-hands.dev
- **Advanced Dashboard**: https://work-2-qazbknukhcfpkhdv.prod-runtime.all-hands.dev

## 🎯 Features

### Basic Dashboard (Port 12000)
- Simple, clean interface
- Bot configuration and control
- Real-time status monitoring
- Activity logs
- Service selection (Views, Followers, Hearts, etc.)

### Advanced Dashboard (Port 12001)
- Professional interface with enhanced features
- Real-time WebSocket updates
- Service availability checker
- Detailed statistics
- Enhanced logging with color coding
- Better mobile responsiveness

## 🛠️ How to Use

1. **Open the Dashboard**: Click on either URL above
2. **Enter TikTok URL**: Paste a valid TikTok video URL
3. **Select Service**: Choose what you want to boost (Views, Followers, etc.)
4. **Start Bot**: Click the "Start Bot" button
5. **Monitor Progress**: Watch the real-time logs and statistics

## ⚙️ Available Services

- 👁️ **Views**: Increase video view count
- 👥 **Followers**: Boost follower count
- ❤️ **Hearts**: Add likes to videos
- 📤 **Shares**: Increase share count
- ⭐ **Favorites**: Add to favorites
- 💬 **Comment Hearts**: Like comments

## 📊 Management

### Using the Launcher Script
```bash
python launcher.py
```

### Manual Control
```bash
# Start basic dashboard
python web_app.py

# Start advanced dashboard  
python advanced_web_app.py

# Check running processes
ps aux | grep python

# Stop all
pkill -f web_app.py
pkill -f advanced_web_app.py
```

## 🔧 Technical Details

### Dependencies
- Flask (Web framework)
- Flask-SocketIO (Real-time updates)
- Selenium (Browser automation)
- Requests (HTTP requests)
- Colorama (Terminal colors)

### Architecture
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Backend**: Python Flask with WebSocket support
- **Bot Engine**: Selenium-based automation
- **Real-time Updates**: Socket.IO for live status

### File Structure
```
bot-tiktok/
├── web_app.py              # Basic web interface
├── advanced_web_app.py     # Advanced web interface
├── launcher.py             # Management script
├── templates/
│   ├── index.html          # Basic dashboard template
│   └── advanced_index.html # Advanced dashboard template
├── v2.py                   # Main bot script
├── config.json             # Configuration file
└── requirements.txt        # Python dependencies
```

## ⚠️ Important Warnings

### Legal & Ethical Use
- **Educational Purpose Only**: This tool is for learning about web automation
- **Terms of Service**: Using automation may violate TikTok's ToS
- **Rate Limiting**: Respect platform limits to avoid bans
- **Responsible Use**: Don't abuse the system or harm others

### Security Considerations
- **Local Use Only**: Don't expose to public internet
- **Captcha Solving**: May require manual intervention
- **Browser Resources**: Uses significant system resources
- **Network Traffic**: Generates automated requests

## 🐛 Troubleshooting

### Common Issues

1. **Bot Not Starting**
   - Check if Chrome/Chromium is installed
   - Verify all dependencies are installed
   - Check firewall settings

2. **Captcha Problems**
   - The bot includes automatic captcha solving
   - May require manual intervention occasionally
   - Check browser console for errors

3. **Connection Issues**
   - Ensure ports 12000/12001 are available
   - Check network connectivity
   - Verify URL accessibility

4. **Performance Issues**
   - Close unnecessary browser tabs
   - Monitor system resources
   - Restart the application if needed

### Logs Location
- Basic Dashboard: `web_app.log`
- Advanced Dashboard: `advanced_web_app.log`

## 🔄 Updates & Maintenance

### Regular Maintenance
- Monitor log files for errors
- Update dependencies regularly
- Check for bot script updates
- Clear browser cache if needed

### Performance Optimization
- Use headless mode for better performance
- Implement proper error handling
- Add request delays to avoid rate limiting
- Monitor memory usage

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Ensure proper network connectivity
4. Review TikTok's current policies

## 🎉 Enjoy!

Your TikTok bot is now live and ready to use! Remember to use it responsibly and respect platform guidelines.

---
*Last updated: 2025-07-22*