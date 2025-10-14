from datetime import datetime

def create_overlay_document(data):
    return {
        "content": data.get("content", ""),
        "type": data.get("type", "text"),  # text or logo
        "position": {
            "x": data.get("x", 0),
            "y": data.get("y", 0)
        },
        "size": {
            "width": data.get("width", 100),
            "height": data.get("height", 50)
        },
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
