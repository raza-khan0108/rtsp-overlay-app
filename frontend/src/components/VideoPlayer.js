import React, { useState } from 'react';
import './VideoPlayer.css';

const VideoPlayer = () => {
  const [rtspUrl, setRtspUrl] = useState('');
  const [streamUrl, setStreamUrl] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = () => {
    if (rtspUrl.trim()) {
      setStreamUrl(`http://localhost:5000/stream?url=${encodeURIComponent(rtspUrl)}`);
      setIsPlaying(true);
    } else {
      alert('Please enter a valid RTSP URL');
    }
  };

  const handleStop = () => {
    setStreamUrl('');
    setIsPlaying(false);
  };

  return (
    <div className="video-player-container">
      <h2>RTSP Livestream Player</h2>
      
      <div className="controls">
        <input 
          type="text" 
          placeholder="Enter RTSP URL (e.g., rtsp://example.com/stream)"
          value={rtspUrl}
          onChange={(e) => setRtspUrl(e.target.value)}
          className="rtsp-input"
          disabled={isPlaying}
        />
        
        <div className="button-group">
          <button onClick={handlePlay} disabled={isPlaying} className="btn-play">
            Play Stream
          </button>
          <button onClick={handleStop} disabled={!isPlaying} className="btn-stop">
            Stop Stream
          </button>
        </div>
      </div>

      {streamUrl && (
        <div className="video-container">
          <img 
            src={streamUrl} 
            alt="RTSP Stream" 
            className="video-stream"
          />
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;
