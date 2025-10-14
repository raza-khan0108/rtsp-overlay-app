# RTSP Overlay Streaming Application - User Guide

## Welcome! 👋

Thank you for using the **RTSP Overlay Streaming Application**! This guide will help you get started with streaming RTSP video and adding custom overlays to your live streams.

**Version**: 1.0  
**Last Updated**: October 15, 2025  
**Difficulty Level**: Beginner-Friendly

---

## Table of Contents

1. [Introduction](#introduction)
2. [What You Need](#what-you-need)
3. [Installation Guide](#installation-guide)
4. [Getting Started](#getting-started)
5. [Using the Video Player](#using-the-video-player)
6. [Managing Overlays](#managing-overlays)
7. [Common Tasks](#common-tasks)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)
10. [Tips & Best Practices](#tips--best-practices)

---

## Introduction

### What is This Application?

The **RTSP Overlay Streaming Application** is a web-based tool that allows you to:

✅ **Stream live video** from RTSP cameras and sources  
✅ **Add custom text overlays** to your video streams  
✅ **Position and customize** overlay text anywhere on the video  
✅ **Save overlay configurations** for future use  
✅ **Manage multiple overlays** at once  

### Who Is This For?

- 🎥 **Security professionals** monitoring RTSP camera feeds
- 📹 **Video producers** adding watermarks and labels
- 🏢 **Business owners** branding their video streams
- 👨‍💻 **Developers** testing RTSP stream functionality
- 🎓 **Students** learning about video streaming technology

### Key Features

| Feature | Description |
|---------|-------------|
| **Live Streaming** | Watch RTSP streams directly in your browser |
| **Custom Overlays** | Add text labels, timestamps, or watermarks |
| **Drag & Position** | Place overlays anywhere on the video |
| **Save & Edit** | Store overlay configurations in the database |
| **Real-Time Updates** | Changes appear instantly on the stream |
| **Multiple Overlays** | Add as many overlays as needed |

---

## What You Need

### System Requirements

**Minimum Requirements**:
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4 GB
- **Disk Space**: 500 MB free space
- **Internet**: Required for MongoDB Atlas and RTSP streams

**Recommended**:
- **RAM**: 8 GB or more
- **Processor**: Intel Core i5 or equivalent
- **Internet**: Stable broadband connection (5+ Mbps)

### Software Prerequisites

Before installation, you need:

1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
2. **Node.js 16+** - Download from [nodejs.org](https://nodejs.org/)
3. **MongoDB Account** - Free at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
4. **Web Browser** - Chrome, Firefox, Edge, or Safari (latest version)

### Optional Tools

- **Git** - For cloning the repository
- **VLC Media Player** - For testing RTSP URLs
- **Postman** - For API testing (developers only)

---

## Installation Guide

### Step 1: Download the Application

**Option A: Using Git** (Recommended)

Open your terminal/command prompt and run:

```bash
git clone https://github.com/yourusername/rtsp-overlay-streaming-app.git
cd rtsp-overlay-streaming-app
```

**Option B: Download ZIP**

1. Visit the [GitHub repository](https://github.com/yourusername/rtsp-overlay-streaming-app)
2. Click **"Code"** → **"Download ZIP"**
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt in the extracted folder

---

### Step 2: Set Up MongoDB Database

**2.1 Create MongoDB Atlas Account**

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
2. Sign up for a **free account**
3. Create a new **Cluster** (choose free tier)
4. Wait for cluster creation (2-3 minutes)

**2.2 Create Database User**

1. Click **"Database Access"** in the left sidebar
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Set username (e.g., `rtsp_user`) and password
5. Set privileges to **"Atlas admin"** or **"Read and write to any database"**
6. Click **"Add User"**

**2.3 Whitelist Your IP Address**

1. Click **"Network Access"** in the left sidebar
2. Click **"Add IP Address"**
3. Choose **"Allow Access from Anywhere"** (for testing) or add your current IP
4. Click **"Confirm"**

**2.4 Get Connection String**

1. Click **"Database"** in the left sidebar
2. Click **"Connect"** on your cluster
3. Choose **"Connect your application"**
4. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
5. Save this for Step 3

---

### Step 3: Configure Backend

**3.1 Navigate to Backend Folder**

```bash
cd backend
```

**3.2 Create Virtual Environment** (Recommended)

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

**3.3 Install Python Dependencies**

```bash
pip install -r requirements.txt
```

Wait for installation to complete (1-2 minutes).

**3.4 Create Environment Configuration**

Create a file named `.env` in the backend folder:

**On Windows**:
```bash
notepad .env
```

**On macOS/Linux**:
```bash
nano .env
```

Paste this content and **replace with your actual MongoDB credentials**:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# MongoDB Atlas Configuration
MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
MONGO_CLUSTER=cluster0.xxxxx.mongodb.net
DB_NAME=rtsp_overlay_db

# Server Configuration
HOST=0.0.0.0
PORT=5000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Important**: Replace:
- `your_mongodb_username` with your MongoDB username
- `your_mongodb_password` with your MongoDB password
- `cluster0.xxxxx.mongodb.net` with your cluster address

Save and close the file.

**3.5 Test Backend Connection**

```bash
python -c "from models.database import db; print('✅ MongoDB Connected!')"
```

If you see `✅ MongoDB Connected!`, you're ready! If not, check the [Troubleshooting](#troubleshooting) section.

---

### Step 4: Configure Frontend

**4.1 Navigate to Frontend Folder**

Open a **new terminal/command prompt** (keep backend terminal open):

```bash
cd frontend
```

**4.2 Install Node Dependencies**

```bash
npm install
```

Wait for installation to complete (2-5 minutes).

---

### Step 5: Start the Application

**5.1 Start Backend Server** (Terminal 1)

In the backend terminal:

```bash
python app.py
```

You should see:
```
✅ Connected to MongoDB: rtsp_overlay_db

==================================================
🚀 Starting RTSP Streaming Server
==================================================
📡 Server running on: http://0.0.0.0:5000
🔧 Debug mode: True
==================================================
```

**Keep this terminal running!**

**5.2 Start Frontend Server** (Terminal 2)

In the frontend terminal:

```bash
npm start
```

The application will automatically open in your browser at `http://localhost:3000`

If it doesn't open automatically, manually visit: **http://localhost:3000**

---

## Getting Started

### Your First Stream

Let's stream your first RTSP video!

**Step 1: Get a Test RTSP URL**

For testing, use this free RTSP stream:
```
rtsp://rtspstream:tp0LkSy9OgpkXx60-tdgU@zephyr.rtsp.stream/movie
```

Or visit [rtsp.stream](https://rtsp.stream) to get your own free test stream.

**Step 2: Enter the RTSP URL**

1. Look at the top section: **"RTSP Livestream Player"**
2. Find the input field with placeholder text
3. Paste the RTSP URL
4. Click the **"Play Stream"** button (green)

**Step 3: Watch the Stream**

The video should appear below the controls within 2-3 seconds. You'll see the live RTSP stream playing!

**Step 4: Stop the Stream**

Click the **"Stop Stream"** button (red) when you're done watching.

---

## Using the Video Player

### Understanding the Interface

The video player section has three main parts:

```
┌─────────────────────────────────────────────┐
│  RTSP Livestream Player                     │
├─────────────────────────────────────────────┤
│  [Enter RTSP URL here...]                   │
│  [Play Stream]  [Stop Stream]               │
├─────────────────────────────────────────────┤
│                                             │
│           📺 Video Display Area            │
│                                             │
└─────────────────────────────────────────────┘
```

### Controls Explained

| Control | Purpose | When to Use |
|---------|---------|-------------|
| **RTSP URL Input** | Enter the stream address | Before playing |
| **Play Stream** | Start streaming video | When URL is entered |
| **Stop Stream** | Stop streaming video | To end the stream |

### Finding RTSP URLs

**Where to get RTSP URLs**:

1. **Your IP Camera**: Check camera manual or settings page
   - Example: `rtsp://192.168.1.100:554/stream1`

2. **Security DVR/NVR**: Access device web interface
   - Example: `rtsp://admin:password@192.168.1.200:554/ch1`

3. **Test Streams**:
   - rtsp.stream (free test streams)
   - Wowza test stream
   - Big Buck Bunny test stream

4. **Format**: `rtsp://[username:password@]host[:port]/path`

### Video Quality Tips

- **Slow stream?** Check your internet connection
- **Choppy video?** Reduce number of overlays
- **No video?** Verify RTSP URL is correct
- **Black screen?** Check camera is online and accessible

---

## Managing Overlays

### What Are Overlays?

Overlays are **text labels** that appear on top of your video stream. Common uses:

- 🏷️ **Camera labels**: "Camera 01", "Main Entrance"
- 🔴 **Status indicators**: "LIVE", "RECORDING"
- 📍 **Location info**: "New York Office", "Parking Lot"
- ⏰ **Timestamps**: "2025-10-15 12:30:45"
- 🏢 **Watermarks**: Company name, logo text

---

### Creating Your First Overlay

**Step 1: Scroll Down to Overlay Manager**

The Overlay Manager section is below the video player.

**Step 2: Fill in the Form**

```
┌─────────────────────────────────────────────┐
│  Create New Overlay                         │
├─────────────────────────────────────────────┤
│  Content: [LIVE STREAM________________]     │
│  Type: [Text ▼]                             │
│  X Position: [100]  Y Position: [50]        │
│  Width: [200]       Height: [100]           │
│  [Create Overlay]                           │
└─────────────────────────────────────────────┘
```

**Fill these fields**:

- **Content**: The text to display (e.g., "LIVE STREAM")
- **Type**: Choose "Text" (logo support coming soon)
- **X Position**: Distance from left edge in pixels (e.g., 100)
- **Y Position**: Distance from top edge in pixels (e.g., 50)
- **Width**: Width of overlay area (e.g., 200)
- **Height**: Height of overlay area (e.g., 100)

**Step 3: Click "Create Overlay"**

You'll see an alert: **"Overlay created successfully"**

**Step 4: View in Table**

Your new overlay appears in the table below with Edit and Delete buttons.

---

### Understanding Position Coordinates

The screen uses a **coordinate system** like a graph:

```
(0,0) ──────────────────────────► X (Right)
  │
  │    (100, 50)
  │       ┌────────────┐
  │       │ Your Text  │
  │       └────────────┘
  │
  ▼
  Y (Down)
```

**Examples**:

| Position | Location | Use Case |
|----------|----------|----------|
| (0, 0) | Top-left corner | Logo |
| (100, 50) | Near top-left | Title |
| (500, 300) | Center | Main message |
| (20, 500) | Bottom-left | Camera ID |
| (800, 500) | Bottom-right | Timestamp |

**Tips**:
- Start with small numbers (50-200) for top positions
- Use larger numbers (400-600) for bottom positions
- Keep text within video boundaries (usually 640x480 or 1280x720)

---

### Editing Overlays

**Step 1: Find Your Overlay in the Table**

Scroll to **"Existing Overlays"** section.

**Step 2: Click "Edit" Button**

The form above fills with current overlay values.

**Step 3: Modify Fields**

Change any field you want:
- Update text content
- Move position
- Resize overlay

**Step 4: Click "Update Overlay"**

Your changes are saved immediately!

---

### Deleting Overlays

**Step 1: Find the Overlay to Delete**

**Step 2: Click "Delete" Button** (red)

**Step 3: Confirm Deletion**

A confirmation dialog appears.

**Step 4: Click "OK"**

The overlay is permanently removed.

⚠️ **Warning**: Deletion cannot be undone!

---

### Viewing Overlays on Video

To see your overlays on the live stream:

**Option 1: If stream is already playing**
1. Stop the current stream
2. Click "Play Stream" again
3. Overlays now appear on video

**Option 2: Fresh start**
1. Enter RTSP URL
2. Click "Play Stream"
3. Overlays automatically appear

**What you'll see**:
- Text in **bright yellow color**
- **Black background** behind text for readability
- Text positioned exactly where you specified

---

## Common Tasks

### Task 1: Add Camera Labels

**Goal**: Label security cameras with their locations

**Steps**:

1. **Create overlay for Camera 1**:
   - Content: `Camera 01 - Front Door`
   - X: `20`, Y: `20`
   - Click "Create Overlay"

2. **Create overlay for Camera 2**:
   - Content: `Camera 02 - Parking Lot`
   - X: `20`, Y: `20`
   - Click "Create Overlay"

3. **Switch between cameras**: Change RTSP URL and play

**Result**: Each camera shows its label at the top-left corner.

---

### Task 2: Add "LIVE" Indicator

**Goal**: Show recording status

**Steps**:

1. **Create LIVE overlay**:
   - Content: `🔴 LIVE`
   - X: `500`, Y: `30`
   - Width: `150`, Height: `60`

2. **Play stream**: Red dot appears at top-right

**Tip**: Use emoji (🔴, 📹, ⚠️) for visual indicators!

---

### Task 3: Add Watermark

**Goal**: Brand your video stream

**Steps**:

1. **Create watermark**:
   - Content: `© Your Company 2025`
   - X: `800`, Y: `550`
   - Width: `300`, Height: `40`

2. **Play stream**: Watermark appears at bottom-right

**Professional Tip**: Use smaller font by reducing width/height.

---

### Task 4: Multiple Overlays

**Goal**: Add several text elements

**Steps**:

1. **Create title** (top-center):
   - Content: `Security Feed`
   - X: `400`, Y: `20`

2. **Create location** (top-left):
   - Content: `New York Office`
   - X: `20`, Y: `20`

3. **Create timestamp** (bottom-right):
   - Content: `2025-10-15`
   - X: `800`, Y: `550`

4. **Create status** (bottom-left):
   - Content: `🔴 Recording`
   - X: `20`, Y: `550`

**Result**: Professional-looking security feed with all info!

---

### Task 5: Test Different Streams

**Goal**: Try various RTSP sources

**Free Test Streams**:

1. **Big Buck Bunny Movie**:
   ```
   rtsp://rtspstream:tp0LkSy9OgpkXx60-tdgU@zephyr.rtsp.stream/movie
   ```

2. **Wowza Test Stream**:
   ```
   rtsp://807e9439d5ca.entrypoint.cloud.wowza.com:1935/app-rC94792j/068b9c9a_stream2
   ```

3. **Your Own Camera**:
   - Check camera manual for RTSP URL
   - Usually: `rtsp://[camera-ip]:554/[stream-path]`

---

## Troubleshooting

### Problem 1: Application Won't Start

**Symptoms**:
- Error message when running `python app.py`
- Terminal shows import errors

**Solutions**:

✅ **Check Python version**:
```bash
python --version
# Should be 3.8 or higher
```

✅ **Activate virtual environment**:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

✅ **Reinstall dependencies**:
```bash
pip install -r requirements.txt
```

---

### Problem 2: Can't Connect to MongoDB

**Symptoms**:
- "❌ Error connecting to MongoDB"
- Authentication failed errors

**Solutions**:

✅ **Check .env file exists**:
```bash
# Windows
dir backend\.env

# macOS/Linux
ls -la backend/.env
```

✅ **Verify credentials**:
- Open `.env` file
- Check username and password match MongoDB Atlas
- Ensure no extra spaces

✅ **Check IP whitelist**:
- Go to MongoDB Atlas dashboard
- Click "Network Access"
- Ensure your IP is whitelisted
- Or use 0.0.0.0/0 for testing

✅ **Test connection**:
```bash
python -c "from models.database import db; print('Connected!')"
```

---

### Problem 3: Video Won't Play

**Symptoms**:
- Blank video area
- Error message about RTSP URL
- Loading indefinitely

**Solutions**:

✅ **Verify RTSP URL format**:
```
Correct: rtsp://example.com:554/stream
Wrong: http://example.com/stream
Wrong: example.com/stream
```

✅ **Test RTSP URL in VLC**:
1. Open VLC Media Player
2. Media → Open Network Stream
3. Paste your RTSP URL
4. Click Play
5. If it doesn't work in VLC, the URL is invalid

✅ **Check network connection**:
- Ensure internet is working
- Ping the camera IP address
- Check firewall settings

✅ **Try test stream**:
```
rtsp://rtspstream:tp0LkSy9OgpkXx60-tdgU@zephyr.rtsp.stream/movie
```

---

### Problem 4: Overlays Not Showing

**Symptoms**:
- Video plays but no text appears
- Overlays created successfully but invisible

**Solutions**:

✅ **Check endpoint**:
- Make sure backend uses `/stream-overlay` not `/stream`
- Look in browser developer console (F12)
- URL should be: `http://localhost:5000/stream-overlay?url=...`

✅ **Verify overlays exist**:
1. Scroll to Overlay Manager
2. Check "Existing Overlays" table
3. Should show at least one overlay

✅ **Adjust position**:
- Text might be outside visible area
- Try position (100, 100) for testing
- Reduce X and Y values

✅ **Restart stream**:
1. Click "Stop Stream"
2. Wait 2 seconds
3. Click "Play Stream" again

---

### Problem 5: Frontend Won't Load

**Symptoms**:
- Browser shows "Cannot GET /"
- Page won't load at localhost:3000

**Solutions**:

✅ **Check if frontend is running**:
- Look at frontend terminal
- Should say "Compiled successfully!"
- Should be on port 3000

✅ **Restart frontend**:
```bash
# Press Ctrl+C to stop
# Then run again:
npm start
```

✅ **Clear browser cache**:
- Press Ctrl+Shift+Delete
- Clear cache and cookies
- Refresh page (Ctrl+R)

✅ **Try different port**:
```bash
# If port 3000 is busy
PORT=3001 npm start
```

---

### Problem 6: Slow Performance

**Symptoms**:
- Video is choppy or laggy
- Browser freezes
- High CPU usage

**Solutions**:

✅ **Reduce overlays**:
- Delete unused overlays
- Keep maximum 5-10 overlays

✅ **Close other tabs**:
- Close unnecessary browser tabs
- Close other applications

✅ **Check internet speed**:
- Run speed test
- Need at least 5 Mbps
- Use wired connection if possible

✅ **Lower video quality**:
- Use lower resolution RTSP stream
- Check camera settings

---

## FAQ (Frequently Asked Questions)

### General Questions

**Q: Is this application free to use?**  
A: Yes! It's completely free and open-source.

**Q: Do I need programming knowledge?**  
A: No! This user guide is designed for non-technical users. Just follow the steps.

**Q: Can I use this commercially?**  
A: Yes, under the MIT License. Check LICENSE file for details.

**Q: Is my data secure?**  
A: Overlay data is stored in your own MongoDB database. Video streams are processed locally.

---

### Features

**Q: Can I add images as overlays?**  
A: Logo support is coming in version 1.1. Currently only text is supported.

**Q: How many overlays can I create?**  
A: No hard limit, but we recommend 5-10 for best performance.

**Q: Can overlays be animated?**  
A: Not yet. Animation features are planned for future versions.

**Q: Can I change text color?**  
A: Currently text is yellow with black background. Customization coming in v1.1.

**Q: Can I save different overlay sets?**  
A: All overlays are saved automatically. You can create/delete as needed.

---

### Technical Questions

**Q: What video formats are supported?**  
A: RTSP input, MJPEG output for browser display.

**Q: Does it work on mobile devices?**  
A: Desktop browsers only for now. Mobile support planned for future.

**Q: Can multiple users access simultaneously?**  
A: Yes, but they'll share the same overlay database.

**Q: What's the video latency?**  
A: Typically 2-5 seconds depending on network and camera.

**Q: Can I record the stream?**  
A: Not built-in. Use screen recording software or save backend stream.

---

### Troubleshooting FAQ

**Q: Why can't I connect to MongoDB?**  
A: Check your username, password, and IP whitelist in MongoDB Atlas.

**Q: Why is the video black?**  
A: RTSP URL might be wrong, or camera is offline. Test URL in VLC first.

**Q: Why are overlays invisible?**  
A: Check you're using `/stream-overlay` endpoint, not `/stream`.

**Q: How do I reset everything?**  
A: Delete all overlays, stop both servers, and restart.

**Q: Where are logs stored?**  
A: Check backend terminal for error messages. Frontend logs in browser console (F12).

---

## Tips & Best Practices

### Design Tips

✅ **Keep it simple**: Don't overcrowd the video with too many overlays  
✅ **Use contrast**: Yellow text on dark background is most readable  
✅ **Strategic placement**: Top corners for labels, bottom for status  
✅ **Consistent style**: Use similar positions for similar cameras  
✅ **Test visibility**: Check overlays are visible on actual video content  

### Performance Tips

✅ **Limit overlays**: Maximum 5-10 for smooth performance  
✅ **Close unused tabs**: Reduces browser memory usage  
✅ **Use local streams**: Lower latency than internet streams  
✅ **Restart periodically**: If running for hours, restart servers  
✅ **Monitor resources**: Check CPU and memory usage  

### Security Tips

✅ **Change default passwords**: Never use default MongoDB credentials  
✅ **Restrict IP access**: Don't use 0.0.0.0/0 in production  
✅ **Use HTTPS**: Enable SSL for production deployment  
✅ **Backup database**: Regularly export overlay configurations  
✅ **Update regularly**: Keep dependencies up to date  

### Organization Tips

✅ **Name overlays clearly**: Use descriptive content  
✅ **Group by purpose**: Status, location, branding separately  
✅ **Document positions**: Note standard positions for consistency  
✅ **Create templates**: Save common overlay configurations  
✅ **Test before deploy**: Verify on test stream first  

---

## Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| `Ctrl+R` | Refresh page | Any time |
| `F12` | Open developer tools | Troubleshooting |
| `Ctrl+C` | Stop server | In terminal |
| `Ctrl+Shift+Delete` | Clear cache | Browser |
| `Tab` | Navigate form fields | Creating overlay |

---

## Getting Help

### Documentation

- **User Guide**: This document (you're reading it!)
- **API Documentation**: For developers (`API_DOCUMENTATION.md`)
- **README**: Quick start guide (`README.md`)

### Support Channels

📧 **Email**: razawarsi828@gmail.com  
🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/rtsp-overlay-streaming-app/issues)  
💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/rtsp-overlay-streaming-app/discussions)  
⭐ **Star the Project**: Show your support on GitHub!

### Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## Glossary

**RTSP**: Real-Time Streaming Protocol - Used for streaming video  
**Overlay**: Text or image displayed on top of video  
**MongoDB**: Database used to store overlay configurations  
**Flask**: Python web framework powering the backend  
**React**: JavaScript library powering the frontend  
**OpenCV**: Library used for video processing  
**Endpoint**: URL path for accessing API functions  
**Position**: X and Y coordinates for overlay placement  
**Coordinates**: Numeric values describing location on screen  

---

## Quick Reference Card

### Installation Checklist

- ☐ Install Python 3.8+
- ☐ Install Node.js 16+
- ☐ Create MongoDB Atlas account
- ☐ Clone repository
- ☐ Create backend `.env` file
- ☐ Install backend dependencies (`pip install -r requirements.txt`)
- ☐ Install frontend dependencies (`npm install`)
- ☐ Start backend (`python app.py`)
- ☐ Start frontend (`npm start`)
- ☐ Open browser to `localhost:3000`

### Common Commands

```bash
# Start backend
cd backend
python app.py

# Start frontend (new terminal)
cd frontend
npm start

# Stop servers
Ctrl+C

# Check MongoDB connection
python -c "from models.database import db; print('OK')"

# Reinstall dependencies
pip install -r requirements.txt
npm install
```

### Default URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

---

## What's Next?

### Learning Path

1. ✅ Complete installation
2. ✅ Stream your first video
3. ✅ Create basic overlays
4. ✅ Try different positions
5. ✅ Add multiple overlays
6. ✅ Connect real cameras
7. ✅ Customize for your needs

### Advanced Topics

- **API Integration**: Use the REST API programmatically
- **Custom Themes**: Modify frontend styling
- **Production Deployment**: Deploy to cloud servers
- **Automation**: Script overlay creation
- **Integration**: Connect with other systems

### Upcoming Features (v1.1)

- 🎨 **Custom text colors**
- 🖼️ **Image/logo overlays**
- ⚡ **Animated overlays**
- 📱 **Mobile responsive design**
- 🔐 **User authentication**
- 💾 **Overlay templates**
- 📊 **Analytics dashboard**

---

## Thank You! 🎉

Thank you for using the **RTSP Overlay Streaming Application**!

If you found this application useful:
- ⭐ **Star the repository** on GitHub
- 🐛 **Report bugs** to help improve it
- 💡 **Suggest features** for future versions
- 📢 **Share with others** who might benefit
- ✍️ **Write a review** or blog post

**Happy Streaming!** 🎥

---

**Version**: 1.0  
**Author**: Raza Khan  
**Email**: razawarsi828@gmail.com  
**Last Updated**: October 15, 2025

---

*Built with ❤️ using React, Flask, MongoDB, and OpenCV*
