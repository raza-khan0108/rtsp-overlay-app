from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import routes and utilities
from routes.overlay_routes import overlay_bp
from utils.video_stream import generate_frames, generate_frames_with_overlays

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(overlay_bp, url_prefix='/api')


@app.route('/')
def index():
    """API Root - List available endpoints"""
    return jsonify({
        "message": "RTSP Streaming API with Overlay Management",
        "version": "1.0",
        "endpoints": {
            "stream": "/stream?url=<rtsp_url>",
            "stream_with_overlays": "/stream-overlay?url=<rtsp_url>",
            "overlays": {
                "list": "GET /api/overlays",
                "get": "GET /api/overlays/<id>",
                "create": "POST /api/overlays",
                "update": "PUT /api/overlays/<id>",
                "delete": "DELETE /api/overlays/<id>"
            }
        }
    })


@app.route('/stream')
def stream():
    """
    Stream RTSP video without overlays
    Query parameter: url (RTSP URL)
    """
    rtsp_url = request.args.get('url', '')
    
    if not rtsp_url:
        return jsonify({"error": "RTSP URL required. Use ?url=<rtsp_url>"}), 400
    
    return Response(
        generate_frames(rtsp_url),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/stream-overlay')
def stream_with_overlay():
    """
    Stream RTSP video with overlays applied
    Query parameter: url (RTSP URL)
    """
    rtsp_url = request.args.get('url', '')
    
    if not rtsp_url:
        return jsonify({"error": "RTSP URL required. Use ?url=<rtsp_url>"}), 400
    
    return Response(
        generate_frames_with_overlays(rtsp_url),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "RTSP Streaming API"
    })


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    print("\n" + "="*50)
    print("🚀 Starting RTSP Streaming Server")
    print("="*50)
    print(f"📡 Server running on: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📚 API Documentation: http://{host}:{port}/")
    print("="*50 + "\n")
    
    app.run(debug=debug, host=host, port=port)
