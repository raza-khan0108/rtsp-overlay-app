import React from 'react';
import VideoPlayer from './components/VideoPlayer';
import OverlayManager from './components/OverlayManager';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="app-header">
        <h1>🎥 RTSP Livestream with Overlay Manager</h1>
        <p>Stream RTSP video and manage custom overlays in real-time</p>
      </header>
      
      <main className="app-content">
        <VideoPlayer />
        <OverlayManager />
      </main>
      
      <footer className="app-footer">
        <p>Built with React + Flask + MongoDB</p>
      </footer>
    </div>
  );
}

export default App;
