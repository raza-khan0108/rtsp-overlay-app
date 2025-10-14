import cv2
from models.database import overlays_collection

def apply_overlays(frame, overlays):
    """
    Apply text and logo overlays to video frame
    """
    for overlay in overlays:
        try:
            content = overlay.get('content', '')
            overlay_type = overlay.get('type', 'text')
            position = overlay.get('position', {'x': 0, 'y': 0})
            size = overlay.get('size', {'width': 100, 'height': 50})
            
            x = position.get('x', 0)
            y = position.get('y', 0)
            
            if overlay_type == 'text':
                # Add text overlay
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                thickness = 2
                color = (255, 255, 255)  # White color
                
                # Add background rectangle for better visibility
                (text_width, text_height), _ = cv2.getTextSize(content, font, font_scale, thickness)
                cv2.rectangle(frame, (x, y - text_height - 10), (x + text_width, y), (0, 0, 0), -1)
                
                # Add text
                cv2.putText(frame, content, (x, y - 5), font, font_scale, color, thickness, cv2.LINE_AA)
                
            elif overlay_type == 'logo':
                # For logo, you would load and overlay an image
                # This is a placeholder - implement if needed
                pass
                
        except Exception as e:
            print(f"Error applying overlay: {e}")
            continue
    
    return frame


def generate_frames(rtsp_url):
    """
    Generate video frames from RTSP stream
    """
    camera = cv2.VideoCapture(rtsp_url)
    
    if not camera.isOpened():
        print(f"Error: Could not open RTSP stream: {rtsp_url}")
        return
    
    try:
        while True:
            success, frame = camera.read()
            
            if not success:
                print("Error: Failed to read frame from stream")
                break
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            
            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
    except Exception as e:
        print(f"Error in generate_frames: {e}")
    finally:
        camera.release()


def generate_frames_with_overlays(rtsp_url):
    """
    Generate video frames with overlays applied
    """
    camera = cv2.VideoCapture(rtsp_url)
    
    if not camera.isOpened():
        print(f"Error: Could not open RTSP stream: {rtsp_url}")
        return
    
    try:
        while True:
            success, frame = camera.read()
            
            if not success:
                print("Error: Failed to read frame from stream")
                break
            
            # Fetch overlays from database
            try:
                overlays = list(overlays_collection.find())
                if overlays:
                    frame = apply_overlays(frame, overlays)
            except Exception as e:
                print(f"Error fetching overlays: {e}")
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            
            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
    except Exception as e:
        print(f"Error in generate_frames_with_overlays: {e}")
    finally:
        camera.release()
