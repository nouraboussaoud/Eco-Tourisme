# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

FUSEKI_ENDPOINT = os.getenv("FUSEKI_ENDPOINT", "http://localhost:3030/waste_management/sparql")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# CORS configuration
CORS_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Ontology namespace
ONTOLOGY_NS = "http://www.semanticweb.org/waste-management/2025/1/#"
