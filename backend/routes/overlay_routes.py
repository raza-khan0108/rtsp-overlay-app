from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
import sys
import os

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.database import overlays_collection

overlay_bp = Blueprint('overlays', __name__)

# CREATE
@overlay_bp.route('/overlays', methods=['POST'])
def create_overlay():
    """Create a new overlay"""
    try:
        data = request.json
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        if 'content' not in data:
            return jsonify({"error": "Content field is required"}), 400
        
        overlay_doc = {
            "content": data.get("content", ""),
            "type": data.get("type", "text"),
            "position": {
                "x": int(data.get("x", 0)),
                "y": int(data.get("y", 0))
            },
            "size": {
                "width": int(data.get("width", 100)),
                "height": int(data.get("height", 50))
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = overlays_collection.insert_one(overlay_doc)
        
        return jsonify({
            "message": "Overlay created successfully",
            "id": str(result.inserted_id),
            "overlay": {
                "id": str(result.inserted_id),
                "content": overlay_doc["content"],
                "type": overlay_doc["type"],
                "position": overlay_doc["position"],
                "size": overlay_doc["size"]
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ ALL
@overlay_bp.route('/overlays', methods=['GET'])
def get_all_overlays():
    """Retrieve all overlays"""
    try:
        overlays = list(overlays_collection.find())
        
        for overlay in overlays:
            overlay['_id'] = str(overlay['_id'])
            overlay['id'] = overlay.pop('_id')
        
        return jsonify({
            "count": len(overlays),
            "overlays": overlays
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# READ ONE
@overlay_bp.route('/overlays/<overlay_id>', methods=['GET'])
def get_overlay(overlay_id):
    """Retrieve a specific overlay by ID"""
    try:
        if not ObjectId.is_valid(overlay_id):
            return jsonify({"error": "Invalid overlay ID format"}), 400
        
        overlay = overlays_collection.find_one({"_id": ObjectId(overlay_id)})
        
        if overlay:
            overlay['_id'] = str(overlay['_id'])
            overlay['id'] = overlay.pop('_id')
            
            return jsonify(overlay), 200
        else:
            return jsonify({"error": "Overlay not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# UPDATE
@overlay_bp.route('/overlays/<overlay_id>', methods=['PUT'])
def update_overlay(overlay_id):
    """Update an existing overlay"""
    try:
        if not ObjectId.is_valid(overlay_id):
            return jsonify({"error": "Invalid overlay ID format"}), 400
        
        data = request.json
        
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        update_fields = {}
        
        if 'content' in data:
            update_fields['content'] = data['content']
        
        if 'type' in data:
            update_fields['type'] = data['type']
        
        if 'x' in data or 'y' in data:
            existing_overlay = overlays_collection.find_one({"_id": ObjectId(overlay_id)})
            if existing_overlay:
                current_position = existing_overlay.get('position', {})
                update_fields['position'] = {
                    "x": int(data.get('x', current_position.get('x', 0))),
                    "y": int(data.get('y', current_position.get('y', 0)))
                }
        
        if 'width' in data or 'height' in data:
            existing_overlay = overlays_collection.find_one({"_id": ObjectId(overlay_id)})
            if existing_overlay:
                current_size = existing_overlay.get('size', {})
                update_fields['size'] = {
                    "width": int(data.get('width', current_size.get('width', 100))),
                    "height": int(data.get('height', current_size.get('height', 50)))
                }
        
        update_fields['updated_at'] = datetime.utcnow()
        
        result = overlays_collection.update_one(
            {"_id": ObjectId(overlay_id)},
            {"$set": update_fields}
        )
        
        if result.matched_count:
            updated_overlay = overlays_collection.find_one({"_id": ObjectId(overlay_id)})
            updated_overlay['_id'] = str(updated_overlay['_id'])
            updated_overlay['id'] = updated_overlay.pop('_id')
            
            return jsonify({
                "message": "Overlay updated successfully",
                "overlay": updated_overlay
            }), 200
        else:
            return jsonify({"error": "Overlay not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE
@overlay_bp.route('/overlays/<overlay_id>', methods=['DELETE'])
def delete_overlay(overlay_id):
    """Delete an overlay by ID"""
    try:
        if not ObjectId.is_valid(overlay_id):
            return jsonify({"error": "Invalid overlay ID format"}), 400
        
        result = overlays_collection.delete_one({"_id": ObjectId(overlay_id)})
        
        if result.deleted_count:
            return jsonify({
                "message": "Overlay deleted successfully",
                "deleted_id": overlay_id
            }), 200
        else:
            return jsonify({"error": "Overlay not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
