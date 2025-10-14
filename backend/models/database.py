from pymongo import MongoClient
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
MONGO_USERNAME = os.getenv('MONGO_USERNAME', '')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', '')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER', '')
DB_NAME = os.getenv('DB_NAME', 'rtsp_overlay_db')

try:
    # Option 1: If using Atlas with username/password (RECOMMENDED)
    if MONGO_USERNAME and MONGO_PASSWORD and MONGO_CLUSTER:
        # Escape username and password to handle special characters
        escaped_username = quote_plus(MONGO_USERNAME)
        escaped_password = quote_plus(MONGO_PASSWORD)
        
        # Build MongoDB Atlas URI
        MONGO_URI = f"mongodb+srv://{escaped_username}:{escaped_password}@{MONGO_CLUSTER}/{DB_NAME}?retryWrites=true&w=majority"
    else:
        # Option 2: Use full URI from environment (fallback)
        MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    
    # Create MongoDB client
    client = MongoClient(MONGO_URI)
    
    # Select database
    db = client[DB_NAME]
    
    # Collections
    overlays_collection = db['overlays']
    
    # Test connection
    client.server_info()  # Will raise an exception if cannot connect
    print(f"✅ Connected to MongoDB: {DB_NAME}")
    
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    raise
