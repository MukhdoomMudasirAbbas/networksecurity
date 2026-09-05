import os
import dns.resolver

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env
load_dotenv()

# Use Google DNS for MongoDB SRV lookup
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8", "8.8.4.4"]

# Get MongoDB URL from .env
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

if not MONGO_DB_URL:
    raise ValueError("MONGO_DB_URL is not found in .env file")

# Create MongoDB client
client = MongoClient(
    MONGO_DB_URL,
    server_api=ServerApi("1")
)

# Test connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("MongoDB connection failed:")
    print(e)
finally:
    client.close()