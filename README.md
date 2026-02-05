# 🎥 RTSP Overlay Streaming Application

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![React](https://img.shields.io/badge/React-16%2B-blue)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)

A powerful, web-based tool that allows you to stream live video from RTSP sources (security cameras, drones, etc.) and add custom, real-time text overlays directly in the browser.

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🚀 Features

* **Live RTSP Streaming**: Low-latency streaming of RTSP feeds via MJPEG conversion.
* **Custom Overlays**: Create text labels, timestamps, watermarks, and status indicators.
* **Drag & Position**: Place overlays anywhere on the video frame using X/Y coordinates.
* **Real-Time Rendering**: Changes to overlays are applied instantly to the video stream.
* **Persistent Storage**: Save overlay configurations to MongoDB.
* **Multi-Overlay Support**: Manage multiple text elements on a single stream simultaneously.

---

## 🛠 Tech Stack

**Backend**
* **Python 3.8+**
* **Flask**: Web server and API handling.
* **OpenCV**: Real-time video processing and text rendering.
* **PyMongo**: Database interaction.

**Frontend**
* **Node.js 16+**
* **React.js**: User interface.
* **Axios**: API communication.

**Database**
* **MongoDB Atlas**: Cloud-based NoSQL database for storing overlay configurations.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
1.  **Python 3.8+** ([Download](https://www.python.org/downloads/))
2.  **Node.js 16+** ([Download](https://nodejs.org/))
3.  **MongoDB Atlas Account** (Free tier is sufficient)
4.  **Git**

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/rtsp-overlay-streaming-app.git
cd rtsp-overlay-streaming-app
```

### 2. Backend Setup

Navigate to the backend folder and set up the Python environment.

```bash
cd backend

# Create virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

Open a new terminal, navigate to the frontend folder, and install dependencies.

```bash
cd frontend
npm install
```

---

## 🔧 Configuration

You must configure the backend environment variables to connect to your database.

1. Navigate to the `backend` directory.
2. Create a file named `.env`.
3. Paste the following configuration, replacing the values with your MongoDB credentials:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here

# MongoDB Atlas Configuration
MONGO_USERNAME=your_mongodb_username
MONGO_PASSWORD=your_mongodb_password
MONGO_CLUSTER=cluster0.xxxxx.mongodb.net
DB_NAME=rtsp_overlay_db

# Server Configuration
HOST=0.0.0.0
PORT=5000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000
```

> **Note:** Ensure your IP address is whitelisted in your MongoDB Atlas Network Access settings.

---

## ▶️ Running the Application

You need to run the Backend and Frontend in separate terminal windows.

**Terminal 1: Backend**

```bash
cd backend
# Ensure venv is activated
python app.py
```

*Server will start at `http://0.0.0.0:5000*`

**Terminal 2: Frontend**

```bash
cd frontend
npm start
```

*Browser should automatically open `http://localhost:3000*`

---

## 📡 API Documentation

The application exposes a RESTful API for managing overlays and streaming.

| Method | Endpoint | Description |
| --- | --- | --- |
| **GET** | `/stream` | Stream raw RTSP video (requires `?url=...`). |
| **GET** | `/stream-overlay` | Stream video with applied overlays. |
| **GET** | `/api/overlays` | Get all configured overlays. |
| **POST** | `/api/overlays` | Create a new overlay. |
| **PUT** | `/api/overlays/<id>` | Update an existing overlay. |
| **DELETE** | `/api/overlays/<id>` | Delete an overlay. |

> For detailed API usage, request bodies, and examples, please refer to [API_DOCUMENTATION.md](https://www.google.com/search?q=API_DOCUMENTATION.md).

---

## 📂 Project Structure

```
rtsp-overlay-streaming-app/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── app.py           # Entry point
│   ├── requirements.txt # Python dependencies
│   └── .env             # Config file
├── frontend/
│   ├── src/             # React source code
│   ├── public/          # Static assets
│   └── package.json     # Node dependencies
├── API_DOCUMENTATION.md # Detailed API docs
├── README.md            # Project overview
└── LICENSE              # MIT License
```

---

## ❓ Troubleshooting

* **Video not playing?**
* Verify the RTSP URL is correct and accessible.
* Test the URL in VLC Media Player first.
* Ensure the backend server is running without errors.

* **"Error connecting to MongoDB"?**
* Check your `.env` credentials.
* Ensure your IP is whitelisted in MongoDB Atlas.

* **Overlays not showing?**
* Ensure you are using the `/stream-overlay` endpoint (handled automatically by the frontend).
* Check if the overlay coordinates (X, Y) are within the video frame.

---

## 🗺️ Roadmap

Future features planned for v1.1+:

* [ ] 🎨 Custom text colors and fonts.
* [ ] 🖼️ Image/Logo overlay support.
* [ ] 🔐 User authentication.
* [ ] ⚡ Animated overlays.
* [ ] 📱 Mobile responsive layout.

---

## 👥 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**Raza Khan**

* Email: razawarsi828@gmail.com
* Project Link: https://github.com/yourusername/rtsp-overlay-streaming-app
