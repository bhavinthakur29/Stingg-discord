import os
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')

if not MONGODB_URI:
    raise ValueError("MONGODB_URI not found in environment variables!")

def _connect_mongo(relax_tls=False):
    kwargs = {
        "server_api": ServerApi('1'),
        "tlsCAFile": certifi.where(),
        "tlsDisableOCSPEndpointCheck": True,
    }
    if relax_tls:
        kwargs["tlsAllowInvalidCertificates"] = True
        kwargs["tlsAllowInvalidHostnames"] = True
    return MongoClient(MONGODB_URI, **kwargs)

client = None
try:
    client = _connect_mongo(relax_tls=False)
    client.admin.command('ping')
    print("[OK] Connected to MongoDB successfully!")
except Exception as e:
    err_msg = str(e).lower()
    if "ssl" in err_msg or "tls" in err_msg:
        if os.getenv("MONGO_DEV_TLS", "").strip() in ("1", "true", "yes"):
            print("[!] Secure TLS failed. Retrying with relaxed TLS (MONGO_DEV_TLS=1)...")
            try:
                client = _connect_mongo(relax_tls=True)
                client.admin.command('ping')
                print("[OK] Connected to MongoDB (relaxed TLS). Use only for local/dev.")
            except Exception as e2:
                print(f"[FAIL] Error connecting to MongoDB: {e2}")
                client = None
        else:
            print(f"[FAIL] Error connecting to MongoDB: {e}")
            print("   Tip: On Windows, if this is an SSL handshake error, try setting MONGO_DEV_TLS=1 in .env (dev only).")
            client = None
    else:
        print(f"[FAIL] Error connecting to MongoDB: {e}")
        client = None

db = client['discord_bot'] if client else None

def get_db():
    """Get database instance"""
    if db is None:
        raise RuntimeError("MongoDB connection not established")
    return db

def save_prefix(guild_id, prefix):
    """Save prefix to MongoDB"""
    try:
        prefixes_collection = get_db()['prefixes']
        prefixes_collection.update_one(
            {'_id': guild_id},
            {'$set': {'prefix': prefix}},
            upsert=True
        )
        print(f"Saved prefix '{prefix}' for guild {guild_id} to MongoDB")
        return True
    except Exception as e:
        print(f"Error saving prefix to MongoDB: {e}")
        return False

def get_prefix(guild_id):
    """Get prefix from MongoDB"""
    try:
        prefixes_collection = get_db()['prefixes']
        result = prefixes_collection.find_one({'_id': guild_id})
        return result['prefix'] if result else None
    except Exception as e:
        print(f"Error retrieving prefix from MongoDB: {e}")
        return None

def load_all_prefixes():
    """Load all prefixes from MongoDB"""
    try:
        prefixes_collection = get_db()['prefixes']
        results = prefixes_collection.find()
        prefixes = {doc['_id']: doc['prefix'] for doc in results}
        return prefixes
    except Exception as e:
        print(f"Error loading prefixes from MongoDB: {e}")
        return {}