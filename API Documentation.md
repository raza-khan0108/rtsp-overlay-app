# RTSP Overlay Streaming API Documentation

## Overview

The RTSP Overlay Streaming API provides endpoints for streaming RTSP video with customizable text overlays. Built with Flask and MongoDB, this RESTful API allows users to create, read, update, and delete overlay configurations that appear on live video streams.

**Base URL**: `http://localhost:5000`

**API Version**: 1.0

**Last Updated**: October 15, 2025

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints Overview](#endpoints-overview)
3. [Streaming Endpoints](#streaming-endpoints)
4. [Overlay CRUD Endpoints](#overlay-crud-endpoints)
5. [Error Handling](#error-handling)
6. [Code Examples](#code-examples)
7. [Rate Limits](#rate-limits)
8. [Support](#support)

---

## Authentication

Currently, this API does not require authentication. All endpoints are publicly accessible.

> **⚠️ Note**: Token-based authentication will be implemented in future versions for production use.

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API root - List all available endpoints |
| GET | `/health` | Health check endpoint |
| GET | `/stream` | Stream RTSP video without overlays |
| GET | `/stream-overlay` | Stream RTSP video with overlays |
| POST | `/api/overlays` | Create a new overlay |
| GET | `/api/overlays` | Retrieve all overlays |
| GET | `/api/overlays/<id>` | Retrieve a specific overlay |
| PUT | `/api/overlays/<id>` | Update an existing overlay |
| DELETE | `/api/overlays/<id>` | Delete an overlay |

---

## Streaming Endpoints

### 1. Get API Information

**Endpoint**: `GET /`

**Description**: Returns information about available API endpoints.

**Request**:
```http
GET http://localhost:5000/
```

**Response** (200 OK):
```json
{
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
}
```

---

### 2. Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API service is running.

**Request**:
```http
GET http://localhost:5000/health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "RTSP Streaming API"
}
```

---

### 3. Stream RTSP Video (No Overlays)

**Endpoint**: `GET /stream`

**Description**: Streams RTSP video without any overlays applied.

**Query Parameters**:
- `url` (required): The RTSP stream URL to play

**Request**:
```http
GET http://localhost:5000/stream?url=rtsp://example.com/stream
```

**Response**: Continuous MJPEG stream (multipart/x-mixed-replace)

**Example using HTML**:
```html
<img src="http://localhost:5000/stream?url=rtsp://example.com/stream" alt="RTSP Stream" />
```

**Example using JavaScript**:
```javascript
const rtspUrl = encodeURIComponent("rtsp://example.com/stream");
const streamUrl = `http://localhost:5000/stream?url=${rtspUrl}`;
document.getElementById('video').src = streamUrl;
```

**Error Response** (400 Bad Request):
```json
{
  "error": "RTSP URL required. Use ?url=<rtsp_url>"
}
```

---

### 4. Stream RTSP Video (With Overlays)

**Endpoint**: `GET /stream-overlay`

**Description**: Streams RTSP video with all configured overlays applied in real-time.

**Query Parameters**:
- `url` (required): The RTSP stream URL to play

**Request**:
```http
GET http://localhost:5000/stream-overlay?url=rtsp://example.com/stream
```

**Response**: Continuous MJPEG stream with overlays rendered on each frame

**Example using HTML**:
```html
<img src="http://localhost:5000/stream-overlay?url=rtsp://example.com/stream" alt="RTSP Stream with Overlays" />
```

**How it works**:
1. Backend fetches all overlays from MongoDB
2. OpenCV captures each frame from RTSP stream
3. Text overlays are rendered on the frame
4. Frame is encoded as JPEG and sent to browser
5. Process repeats 30 times per second for smooth video

**Notes**:
- Overlays are fetched from MongoDB for each frame
- Text appears in **yellow color** with **black background** for visibility
- Position is calculated from top-left corner (0, 0)
- Overlay changes are reflected in real-time

---

## Overlay CRUD Endpoints

### 5. Create Overlay

**Endpoint**: `POST /api/overlays`

**Description**: Creates a new overlay configuration and saves it to MongoDB.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "content": "LIVE STREAM",
  "type": "text",
  "x": 100,
  "y": 50,
  "width": 200,
  "height": 100
}
```

**Request Body Parameters**:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| content | string | ✅ Yes | - | Text to display or logo path |
| type | string | No | "text" | Overlay type: "text" or "logo" |
| x | integer | No | 0 | X position in pixels from left |
| y | integer | No | 0 | Y position in pixels from top |
| width | integer | No | 100 | Width in pixels |
| height | integer | No | 50 | Height in pixels |

**Response** (201 Created):
```json
{
  "message": "Overlay created successfully",
  "id": "671234abc5678def90123456",
  "overlay": {
    "id": "671234abc5678def90123456",
    "content": "LIVE STREAM",
    "type": "text",
    "position": {
      "x": 100,
      "y": 50
    },
    "size": {
      "width": 200,
      "height": 100
    }
  }
}
```

**Error Responses**:

*400 Bad Request* - Missing required fields:
```json
{
  "error": "Content field is required"
}
```

*400 Bad Request* - Invalid data:
```json
{
  "error": "Request body is required"
}
```

*500 Internal Server Error*:
```json
{
  "error": "Database connection failed"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{
    "content": "LIVE STREAM",
    "type": "text",
    "x": 100,
    "y": 50,
    "width": 200,
    "height": 100
  }'
```

**PowerShell Example**:
```powershell
$body = @{
    content = "LIVE STREAM"
    type = "text"
    x = 100
    y = 50
    width = 200
    height = 100
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/overlays" -Method POST -Body $body -ContentType "application/json"
```

---

### 6. Get All Overlays

**Endpoint**: `GET /api/overlays`

**Description**: Retrieves all overlay configurations from the database.

**Request**:
```http
GET http://localhost:5000/api/overlays
```

**Response** (200 OK):
```json
{
  "count": 2,
  "overlays": [
    {
      "id": "671234abc5678def90123456",
      "content": "LIVE STREAM",
      "type": "text",
      "position": {
        "x": 100,
        "y": 50
      },
      "size": {
        "width": 200,
        "height": 100
      },
      "created_at": "2025-10-14T18:30:00.000Z",
      "updated_at": "2025-10-14T18:30:00.000Z"
    },
    {
      "id": "671234abc5678def90123457",
      "content": "Camera 01",
      "type": "text",
      "position": {
        "x": 20,
        "y": 500
      },
      "size": {
        "width": 150,
        "height": 60
      },
      "created_at": "2025-10-14T18:35:00.000Z",
      "updated_at": "2025-10-14T18:35:00.000Z"
    }
  ]
}
```

**Empty Response** (200 OK):
```json
{
  "count": 0,
  "overlays": []
}
```

**cURL Example**:
```bash
curl http://localhost:5000/api/overlays
```

**PowerShell Example**:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/overlays" -Method GET
```

---

### 7. Get Single Overlay

**Endpoint**: `GET /api/overlays/<overlay_id>`

**Description**: Retrieves a specific overlay by its MongoDB ObjectId.

**URL Parameters**:
- `overlay_id` (required): MongoDB ObjectId (24-character hexadecimal string)

**Request**:
```http
GET http://localhost:5000/api/overlays/671234abc5678def90123456
```

**Response** (200 OK):
```json
{
  "id": "671234abc5678def90123456",
  "content": "LIVE STREAM",
  "type": "text",
  "position": {
    "x": 100,
    "y": 50
  },
  "size": {
    "width": 200,
    "height": 100
  },
  "created_at": "2025-10-14T18:30:00.000Z",
  "updated_at": "2025-10-14T18:30:00.000Z"
}
```

**Error Responses**:

*400 Bad Request* - Invalid ID format:
```json
{
  "error": "Invalid overlay ID format"
}
```

*404 Not Found*:
```json
{
  "error": "Overlay not found"
}
```

**cURL Example**:
```bash
curl http://localhost:5000/api/overlays/671234abc5678def90123456
```

---

### 8. Update Overlay

**Endpoint**: `PUT /api/overlays/<overlay_id>`

**Description**: Updates an existing overlay's properties. Supports partial updates - only provided fields are modified.

**URL Parameters**:
- `overlay_id` (required): MongoDB ObjectId

**Request Headers**:
```
Content-Type: application/json
```

**Request Body** (all fields optional):
```json
{
  "content": "UPDATED TEXT",
  "x": 150,
  "y": 75
}
```

**Request Body Parameters** (all optional):

| Parameter | Type | Description |
|-----------|------|-------------|
| content | string | Updated text or logo path |
| type | string | "text" or "logo" |
| x | integer | New X position in pixels |
| y | integer | New Y position in pixels |
| width | integer | New width in pixels |
| height | integer | New height in pixels |

**Response** (200 OK):
```json
{
  "message": "Overlay updated successfully",
  "overlay": {
    "id": "671234abc5678def90123456",
    "content": "UPDATED TEXT",
    "type": "text",
    "position": {
      "x": 150,
      "y": 75
    },
    "size": {
      "width": 200,
      "height": 100
    },
    "created_at": "2025-10-14T18:30:00.000Z",
    "updated_at": "2025-10-14T19:00:00.000Z"
  }
}
```

**Error Responses**:

*400 Bad Request* - Missing body:
```json
{
  "error": "Request body is required"
}
```

*400 Bad Request* - Invalid ID:
```json
{
  "error": "Invalid overlay ID format"
}
```

*404 Not Found*:
```json
{
  "error": "Overlay not found"
}
```

**cURL Example**:
```bash
curl -X PUT http://localhost:5000/api/overlays/671234abc5678def90123456 \
  -H "Content-Type: application/json" \
  -d '{
    "content": "UPDATED TEXT",
    "x": 150,
    "y": 75
  }'
```

**PowerShell Example**:
```powershell
$body = @{
    content = "UPDATED TEXT"
    x = 150
    y = 75
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/overlays/671234abc5678def90123456" -Method PUT -Body $body -ContentType "application/json"
```

---

### 9. Delete Overlay

**Endpoint**: `DELETE /api/overlays/<overlay_id>`

**Description**: Permanently deletes an overlay from the database. This action cannot be undone.

**URL Parameters**:
- `overlay_id` (required): MongoDB ObjectId

**Request**:
```http
DELETE http://localhost:5000/api/overlays/671234abc5678def90123456
```

**Response** (200 OK):
```json
{
  "message": "Overlay deleted successfully",
  "deleted_id": "671234abc5678def90123456"
}
```

**Error Responses**:

*400 Bad Request* - Invalid ID:
```json
{
  "error": "Invalid overlay ID format"
}
```

*404 Not Found*:
```json
{
  "error": "Overlay not found"
}
```

**cURL Example**:
```bash
curl -X DELETE http://localhost:5000/api/overlays/671234abc5678def90123456
```

**PowerShell Example**:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/overlays/671234abc5678def90123456" -Method DELETE
```

---

## Error Handling

All API endpoints follow standard HTTP status codes:

| Status Code | Meaning | Description | Example |
|-------------|---------|-------------|---------|
| 200 | OK | Request successful | GET overlay successful |
| 201 | Created | Resource created successfully | POST overlay created |
| 400 | Bad Request | Invalid request parameters | Missing required field |
| 404 | Not Found | Resource not found | Overlay ID doesn't exist |
| 500 | Internal Server Error | Server-side error | Database connection failed |

### Error Response Format

All error responses follow this structure:

```json
{
  "error": "Descriptive error message"
}
```

### Common Error Scenarios

**1. Invalid RTSP URL**
```json
{
  "error": "RTSP URL required. Use ?url=<rtsp_url>"
}
```

**2. Invalid MongoDB ObjectId**
```json
{
  "error": "Invalid overlay ID format"
}
```

**3. Missing Required Fields**
```json
{
  "error": "Content field is required"
}
```

**4. Resource Not Found**
```json
{
  "error": "Overlay not found"
}
```

**5. Database Connection Error**
```json
{
  "error": "Database connection failed"
}
```

---

## Code Examples

### Python (using requests library)

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# ========== CREATE OVERLAY ==========
def create_overlay():
    overlay_data = {
        "content": "LIVE STREAM",
        "type": "text",
        "x": 100,
        "y": 50,
        "width": 200,
        "height": 100
    }

    response = requests.post(
        f"{BASE_URL}/api/overlays",
        headers={"Content-Type": "application/json"},
        json=overlay_data
    )

    if response.status_code == 201:
        result = response.json()
        print(f"✅ Overlay created with ID: {result['id']}")
        return result['id']
    else:
        print(f"❌ Error: {response.json()}")
        return None

# ========== GET ALL OVERLAYS ==========
def get_all_overlays():
    response = requests.get(f"{BASE_URL}/api/overlays")

    if response.status_code == 200:
        data = response.json()
        print(f"📋 Total overlays: {data['count']}")

        for overlay in data['overlays']:
            print(f"  - {overlay['content']} at ({overlay['position']['x']}, {overlay['position']['y']})")

        return data['overlays']
    else:
        print(f"❌ Error: {response.json()}")
        return []

# ========== GET SINGLE OVERLAY ==========
def get_overlay(overlay_id):
    response = requests.get(f"{BASE_URL}/api/overlays/{overlay_id}")

    if response.status_code == 200:
        overlay = response.json()
        print(f"✅ Overlay: {overlay['content']}")
        return overlay
    else:
        print(f"❌ Error: {response.json()}")
        return None

# ========== UPDATE OVERLAY ==========
def update_overlay(overlay_id):
    update_data = {
        "content": "UPDATED LIVE",
        "x": 150,
        "y": 75
    }

    response = requests.put(
        f"{BASE_URL}/api/overlays/{overlay_id}",
        headers={"Content-Type": "application/json"},
        json=update_data
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Overlay updated: {result['overlay']['content']}")
        return result['overlay']
    else:
        print(f"❌ Error: {response.json()}")
        return None

# ========== DELETE OVERLAY ==========
def delete_overlay(overlay_id):
    response = requests.delete(f"{BASE_URL}/api/overlays/{overlay_id}")

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Overlay deleted: {result['deleted_id']}")
        return True
    else:
        print(f"❌ Error: {response.json()}")
        return False

# ========== EXAMPLE USAGE ==========
if __name__ == "__main__":
    # Create overlay
    overlay_id = create_overlay()

    # Get all overlays
    get_all_overlays()

    # Get single overlay
    if overlay_id:
        get_overlay(overlay_id)

        # Update overlay
        update_overlay(overlay_id)

        # Delete overlay
        delete_overlay(overlay_id)
```

---

### JavaScript (using fetch API)

```javascript
const BASE_URL = "http://localhost:5000";

// ========== CREATE OVERLAY ==========
async function createOverlay() {
  const overlayData = {
    content: "LIVE STREAM",
    type: "text",
    x: 100,
    y: 50,
    width: 200,
    height: 100
  };

  try {
    const response = await fetch(`${BASE_URL}/api/overlays`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(overlayData)
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`✅ Overlay created with ID: ${data.id}`);
      return data.id;
    } else {
      console.error(`❌ Error: ${data.error}`);
      return null;
    }
  } catch (error) {
    console.error(`❌ Network error: ${error.message}`);
    return null;
  }
}

// ========== GET ALL OVERLAYS ==========
async function getAllOverlays() {
  try {
    const response = await fetch(`${BASE_URL}/api/overlays`);
    const data = await response.json();

    if (response.ok) {
      console.log(`📋 Total overlays: ${data.count}`);

      data.overlays.forEach(overlay => {
        console.log(`  - ${overlay.content} at (${overlay.position.x}, ${overlay.position.y})`);
      });

      return data.overlays;
    } else {
      console.error(`❌ Error: ${data.error}`);
      return [];
    }
  } catch (error) {
    console.error(`❌ Network error: ${error.message}`);
    return [];
  }
}

// ========== GET SINGLE OVERLAY ==========
async function getOverlay(overlayId) {
  try {
    const response = await fetch(`${BASE_URL}/api/overlays/${overlayId}`);
    const data = await response.json();

    if (response.ok) {
      console.log(`✅ Overlay: ${data.content}`);
      return data;
    } else {
      console.error(`❌ Error: ${data.error}`);
      return null;
    }
  } catch (error) {
    console.error(`❌ Network error: ${error.message}`);
    return null;
  }
}

// ========== UPDATE OVERLAY ==========
async function updateOverlay(overlayId) {
  const updateData = {
    content: "UPDATED LIVE",
    x: 150,
    y: 75
  };

  try {
    const response = await fetch(`${BASE_URL}/api/overlays/${overlayId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(updateData)
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`✅ Overlay updated: ${data.overlay.content}`);
      return data.overlay;
    } else {
      console.error(`❌ Error: ${data.error}`);
      return null;
    }
  } catch (error) {
    console.error(`❌ Network error: ${error.message}`);
    return null;
  }
}

// ========== DELETE OVERLAY ==========
async function deleteOverlay(overlayId) {
  try {
    const response = await fetch(`${BASE_URL}/api/overlays/${overlayId}`, {
      method: "DELETE"
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`✅ Overlay deleted: ${data.deleted_id}`);
      return true;
    } else {
      console.error(`❌ Error: ${data.error}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ Network error: ${error.message}`);
    return false;
  }
}

// ========== EXAMPLE USAGE ==========
async function runExamples() {
  // Create overlay
  const overlayId = await createOverlay();

  // Get all overlays
  await getAllOverlays();

  // Get single overlay
  if (overlayId) {
    await getOverlay(overlayId);

    // Update overlay
    await updateOverlay(overlayId);

    // Delete overlay
    await deleteOverlay(overlayId);
  }
}

// Run examples
runExamples();
```

---

### PowerShell

```powershell
$BASE_URL = "http://localhost:5000"

# ========== CREATE OVERLAY ==========
function Create-Overlay {
    $body = @{
        content = "LIVE STREAM"
        type = "text"
        x = 100
        y = 50
        width = 200
        height = 100
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/overlays" -Method POST -Body $body -ContentType "application/json"
        Write-Host "✅ Overlay created with ID: $($response.id)" -ForegroundColor Green
        return $response.id
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# ========== GET ALL OVERLAYS ==========
function Get-AllOverlays {
    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/overlays" -Method GET
        Write-Host "📋 Total overlays: $($response.count)" -ForegroundColor Cyan

        foreach ($overlay in $response.overlays) {
            Write-Host "  - $($overlay.content) at ($($overlay.position.x), $($overlay.position.y))"
        }

        return $response.overlays
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return @()
    }
}

# ========== GET SINGLE OVERLAY ==========
function Get-Overlay {
    param([string]$OverlayId)

    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/overlays/$OverlayId" -Method GET
        Write-Host "✅ Overlay: $($response.content)" -ForegroundColor Green
        return $response
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# ========== UPDATE OVERLAY ==========
function Update-Overlay {
    param([string]$OverlayId)

    $body = @{
        content = "UPDATED LIVE"
        x = 150
        y = 75
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/overlays/$OverlayId" -Method PUT -Body $body -ContentType "application/json"
        Write-Host "✅ Overlay updated: $($response.overlay.content)" -ForegroundColor Green
        return $response.overlay
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# ========== DELETE OVERLAY ==========
function Remove-Overlay {
    param([string]$OverlayId)

    try {
        $response = Invoke-RestMethod -Uri "$BASE_URL/api/overlays/$OverlayId" -Method DELETE
        Write-Host "✅ Overlay deleted: $($response.deleted_id)" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# ========== EXAMPLE USAGE ==========
Write-Host "Starting API Examples..." -ForegroundColor Yellow
Write-Host ""

# Create overlay
$overlayId = Create-Overlay

# Get all overlays
Get-AllOverlays

# Get single overlay
if ($overlayId) {
    Get-Overlay -OverlayId $overlayId

    # Update overlay
    Update-Overlay -OverlayId $overlayId

    # Delete overlay
    Remove-Overlay -OverlayId $overlayId
}
```

---

### cURL Commands

```bash
# ========== CREATE OVERLAY ==========
curl -X POST http://localhost:5000/api/overlays \
  -H "Content-Type: application/json" \
  -d '{
    "content": "LIVE STREAM",
    "type": "text",
    "x": 100,
    "y": 50,
    "width": 200,
    "height": 100
  }'

# ========== GET ALL OVERLAYS ==========
curl http://localhost:5000/api/overlays

# ========== GET SINGLE OVERLAY ==========
curl http://localhost:5000/api/overlays/671234abc5678def90123456

# ========== UPDATE OVERLAY ==========
curl -X PUT http://localhost:5000/api/overlays/671234abc5678def90123456 \
  -H "Content-Type: application/json" \
  -d '{
    "content": "UPDATED LIVE",
    "x": 150,
    "y": 75
  }'

# ========== DELETE OVERLAY ==========
curl -X DELETE http://localhost:5000/api/overlays/671234abc5678def90123456

# ========== HEALTH CHECK ==========
curl http://localhost:5000/health

# ========== STREAM RTSP (No Overlays) ==========
curl "http://localhost:5000/stream?url=rtsp://example.com/stream" -o stream.mjpeg

# ========== STREAM RTSP (With Overlays) ==========
curl "http://localhost:5000/stream-overlay?url=rtsp://example.com/stream" -o stream_overlay.mjpeg
```

---

## Rate Limits

### Current Status
**No rate limits implemented** in the current version (v1.0).

### Planned Implementation (Future Versions)

| Limit Type | Value | Applies To |
|------------|-------|------------|
| Requests per minute | 100 | Per IP address |
| Requests per hour | 1000 | Per IP address |
| Concurrent streams | 5 | Per IP address |
| Streaming endpoints | Unlimited | Excluded from rate limits |

### Rate Limit Headers (Future)
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1634567890
```

### Rate Limit Exceeded Response (Future)
```json
{
  "error": "Rate limit exceeded. Please try again in 60 seconds.",
  "retry_after": 60
}
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. RTSP Stream Not Playing

**Problem**: Video stream doesn't load or shows error

**Possible Causes**:
- Invalid RTSP URL
- RTSP server is down or unreachable
- Firewall blocking RTSP traffic
- OpenCV not properly installed

**Solutions**:
```bash
# Test RTSP URL manually
curl -v "rtsp://example.com/stream"

# Check if OpenCV is installed
python -c "import cv2; print(cv2.__version__)"

# Verify backend is running
curl http://localhost:5000/health
```

#### 2. Overlays Not Appearing on Video

**Problem**: Video plays but overlays are not visible

**Possible Causes**:
- Using `/stream` endpoint instead of `/stream-overlay`
- No overlays created in database
- Overlay position outside video frame
- Text color blends with background

**Solutions**:
- Use `/stream-overlay?url=...` endpoint
- Create test overlay with visible position
- Adjust overlay position to (100, 100)
- Text is rendered in yellow - should be visible

#### 3. MongoDB Connection Failed

**Problem**: API returns database errors

**Possible Causes**:
- MongoDB not running
- Incorrect connection string in `.env`
- Network issues with MongoDB Atlas

**Solutions**:
```bash
# Test MongoDB connection
python -c "from models.database import db; print('Connected!')"

# Check .env file
cat backend/.env

# Verify MongoDB Atlas whitelist includes your IP
```

#### 4. CORS Errors in Browser

**Problem**: Frontend can't access backend API

**Possible Causes**:
- Flask-CORS not installed
- Frontend running on different port
- Browser blocking cross-origin requests

**Solutions**:
```bash
# Install Flask-CORS
pip install flask-cors

# Verify CORS is enabled in app.py
grep "CORS" backend/app.py

# Check backend URL in frontend code
```

#### 5. 404 Not Found for Overlays

**Problem**: Cannot find overlay by ID

**Possible Causes**:
- Invalid MongoDB ObjectId format
- Overlay was deleted
- Wrong overlay ID

**Solutions**:
- Verify ID is 24-character hex string
- List all overlays: `GET /api/overlays`
- Check if overlay exists in database

---

## Best Practices

### 1. API Usage

- **Always URL-encode RTSP URLs** when passing as query parameters
- **Store overlay IDs** returned from CREATE operations
- **Handle errors gracefully** with try-catch blocks
- **Validate data** before sending to API
- **Use meaningful overlay content** for better identification

### 2. Performance Optimization

- **Limit number of overlays** to 5-10 for smooth streaming
- **Use simple text overlays** rather than complex graphics
- **Position overlays strategically** to avoid overlap
- **Close unused streams** to free resources
- **Cache overlay data** in frontend to reduce API calls

### 3. Security Considerations

- **Never expose MongoDB credentials** in frontend code
- **Validate RTSP URLs** before streaming
- **Implement authentication** for production use
- **Use HTTPS** in production environment
- **Sanitize user input** for overlay content

### 4. Development Tips

- **Test with free RTSP streams** (rtsp.stream, Wowza test streams)
- **Use Postman** for API testing
- **Enable debug mode** during development
- **Check backend logs** for error messages
- **Version control** your `.env.example` file

---

## API Versioning

### Current Version: 1.0

**Base URL**: `http://localhost:5000`

### Future Versioning Strategy

Future API versions will use URL versioning:

- Version 1.x: `http://localhost:5000/api/v1/overlays`
- Version 2.x: `http://localhost:5000/api/v2/overlays`

### Breaking Changes Policy

- **Major version** (2.0): Breaking changes, incompatible with v1
- **Minor version** (1.1): New features, backward compatible
- **Patch version** (1.0.1): Bug fixes, fully compatible

---

## Changelog

### Version 1.0 (October 2025)

**Initial Release**

**Features**:
- ✅ RTSP streaming without overlays
- ✅ RTSP streaming with overlays
- ✅ CRUD operations for overlays (Create, Read, Update, Delete)
- ✅ MongoDB integration for overlay storage
- ✅ Real-time overlay rendering using OpenCV
- ✅ RESTful API design
- ✅ CORS support for frontend integration
- ✅ Health check endpoint
- ✅ Comprehensive error handling

**Known Limitations**:
- No authentication/authorization
- No rate limiting
- Logo overlays not fully implemented
- Single video codec support (MJPEG)
- No overlay animation support

**Upcoming in v1.1** (Planned):
- User authentication with JWT tokens
- Rate limiting implementation
- WebSocket support for real-time updates
- Overlay animation effects
- Multiple video codec support (H.264, HEVC)

---

## Support and Contact

### Getting Help

**Documentation**: This API documentation

**GitHub Repository**: https://github.com/yourusername/rtsp-overlay-streaming-app

**Issues**: Report bugs and feature requests on GitHub Issues

### Contact Information

**Developer**: Raza Khan

**Email**: razawarsi828@gmail.com

**GitHub**: @yourusername

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### License

This project is licensed under the MIT License.

---

## Appendix

### A. MongoDB ObjectId Format

MongoDB uses 12-byte ObjectId values:
- **4 bytes**: Unix timestamp (seconds since epoch)
- **5 bytes**: Random value
- **3 bytes**: Incrementing counter

**Example**: `671234abc5678def90123456` (24 hex characters)

### B. RTSP Protocol Overview

RTSP (Real-Time Streaming Protocol) is used for streaming media:
- **Port**: Usually 554
- **Format**: `rtsp://[username:password@]host[:port]/path`
- **Commands**: PLAY, PAUSE, SETUP, TEARDOWN

**Example URLs**:
- `rtsp://192.168.1.100:554/stream1`
- `rtsp://username:password@camera.local/live`
- `rtsp://stream.example.com:8554/test`

### C. Position Coordinate System

Overlay positions use pixel coordinates:

```
(0,0) ────────────────────────► X axis
  │
  │    (100, 50)
  │        ┌─────────────┐
  │        │  Text Here  │
  │        └─────────────┘
  │
  │
  ▼
  Y axis
```

- **Origin**: Top-left corner (0, 0)
- **X axis**: Increases to the right
- **Y axis**: Increases downward
- **Units**: Pixels

### D. Supported Video Formats

| Format | Support | Notes |
|--------|---------|-------|
| RTSP | ✅ Full | Primary streaming protocol |
| MJPEG | ✅ Full | Output format for browser |
| H.264 | ⚠️ Partial | Input only, transcoded to MJPEG |
| RTMP | ❌ Not supported | May be added in future |
| HLS | ❌ Not supported | May be added in future |

---

**Last Updated**: October 15, 2025

**API Version**: 1.0

**Documentation Version**: 1.0.0

---

*Built with ❤️ using Flask, MongoDB, OpenCV, and React*
