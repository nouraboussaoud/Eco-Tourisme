# 🔐 Configuration Avancée

## Variables d'Environnement Complètes

### Backend (.env)

```env
# =============================================
# FUSEKI CONFIGURATION
# =============================================
FUSEKI_ENDPOINT=http://localhost:3030/waste_management/sparql
FUSEKI_DATASET=waste_management

# =============================================
# AI & NLP CONFIGURATION  
# =============================================
# Options: gemini, spacy, pattern
NLP_ENGINE=pattern

# Google Gemini API (si USE_GEMINI=true)
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-pro

# SpaCy language model
SPACY_MODEL=fr_core_news_md

# =============================================
# SERVER CONFIGURATION
# =============================================
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
DEBUG_MODE=false

# =============================================
# FRONTEND CONFIGURATION
# =============================================
FRONTEND_URL=http://localhost:3000
FRONTEND_PORT=3000

# =============================================
# CORS CONFIGURATION
# =============================================
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000
CORS_CREDENTIALS=true
CORS_METHODS=GET,POST,PUT,DELETE,OPTIONS
CORS_HEADERS=*

# =============================================
# ONTOLOGY CONFIGURATION
# =============================================
ONTOLOGY_NS=http://www.semanticweb.org/achref/ontologies/2025/9/tourism-eco/
ONTOLOGY_FILE=eco-toursime.rdf

# =============================================
# RECOMMENDATION ENGINE
# =============================================
DEFAULT_BUDGET=1000
DEFAULT_DURATION=3
DEFAULT_PROFILE=Adventure

# Carbon scoring thresholds (kg CO2)
CARBON_LOW_THRESHOLD=50
CARBON_MEDIUM_THRESHOLD=150

# =============================================
# DATABASE CONFIGURATION (optional)
# =============================================
DATABASE_URL=sqlite:///./ecotravel.db
DATABASE_ECHO=false

# =============================================
# LOGGING CONFIGURATION
# =============================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# =============================================
# SECURITY CONFIGURATION
# =============================================
SECRET_KEY=your-secret-key-here-change-in-production
API_KEY_ENABLED=false
API_KEY=your-api-key-here

# =============================================
# CACHE CONFIGURATION
# =============================================
CACHE_ENABLED=true
CACHE_TTL=3600  # 1 hour

# =============================================
# RATE LIMITING
# =============================================
RATE_LIMIT_ENABLED=false
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60  # seconds

# =============================================
# PERFORMANCE
# =============================================
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30  # seconds
THREAD_POOL_SIZE=4
```

---

## Configuration Fuseki

### Fichier de Configuration (fuseki-config.ttl)

```ttl
@prefix :       <http://base/> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tdb:    <http://jena.apache.org/2016/tdb#> .
@prefix fuseki: <http://jena.apache.org/fuseki#> .
@prefix ja:     <http://jena.apache.org/2016/ja#> .

# In-memory dataset
:dataset_mem a tdb:DatasetTDB ;
    tdb:Location "target/tdb" ;
    .

:service_mem a fuseki:Service ;
    fuseki:name "waste_management" ;
    fuseki:dataset :dataset_mem ;
    fuseki:endpoint [
        fuseki:operation fuseki:query ;
        fuseki:name "sparql"
    ] ;
    fuseki:endpoint [
        fuseki:operation fuseki:update ;
        fuseki:name "update"
    ] ;
    .
```

### Lancer Fuseki avec config

```bash
# Avec fichier de configuration
fuseki-server --config=fuseki-config.ttl

# Avec stockage persistant
fuseki-server --loc=databases/waste_management --update /waste_management

# Avec allocation mémoire
export FUSEKI_HOME=/path/to/fuseki
export JENA_HOME=$FUSEKI_HOME
$FUSEKI_HOME/fuseki-server --Xmx4G --update --mem /waste_management
```

---

## Configuration Frontend

### vite.config.js Avancé

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  
  server: {
    port: 3000,
    host: '0.0.0.0',
    
    // Proxy API requests
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        ws: true,
      }
    },
    
    // Performance
    middlewareMode: false,
  },
  
  build: {
    // Optimizations
    minify: 'terser',
    sourcemap: false,
    
    rollupOptions: {
      output: {
        manualChunks: {
          'react': ['react', 'react-dom'],
          'axios': ['axios'],
          'leaflet': ['leaflet', 'react-leaflet'],
        }
      }
    },
    
    // Thresholds
    chunkSizeWarningLimit: 500,
    reportCompressedSize: true,
  },
  
  // Aliases
  resolve: {
    alias: {
      '@': '/src',
      '@components': '/src/components',
      '@utils': '/src/utils',
    }
  }
})
```

---

## Performance Tuning

### Backend - Caching

```python
# config.py
from functools import lru_cache
import redis

# Redis cache (optional)
REDIS_URL = "redis://localhost:6379/0"
CACHE_BACKEND = "redis"  # ou "memory"

# Cache TTL (seconds)
CACHE_TTL_SHORT = 60       # 1 minute
CACHE_TTL_MEDIUM = 300     # 5 minutes
CACHE_TTL_LONG = 3600      # 1 hour
```

### Query Optimization

```python
# services/recommendation_engine.py

# Batch queries
def batch_get_recommendations(self, queries: List[Dict]) -> List[Dict]:
    """Récupère plusieurs recommandations en batch"""
    results = []
    for query in queries:
        result = self.generate_recommendation(**query)
        results.append(result)
    return results

# Index popular queries
@lru_cache(maxsize=128)
def cached_profiles(self):
    """Cache des profils"""
    return self.get_profiles_list()
```

---

## Security Hardening

### Backend Security

```python
# main.py
from fastapi.middleware import Trustedhost, GZipMiddleware
from fastapi.security import HTTPBearer

app.add_middleware(
    Trustedhost.TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=1000
)

# Rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/public")
@limiter.limit("10/minute")
async def public_endpoint(request: Request):
    pass
```

### CORS Strict

```python
# config.py
CORS_ORIGINS = [
    "https://ecotravel.com",           # Production
    "https://www.ecotravel.com",       # WWW production
    "http://localhost:3000",           # Local development
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST"]
CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]
```

---

## Monitoring & Logging

### Logging Configuration

```python
# logging_config.py
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
        },
        "uvicorn": {
            "handlers": ["default"],
            "level": "INFO",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

---

## Database Configuration (Optional)

### SQLAlchemy Setup

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./ecotravel.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Deployment Configuration

### Docker (Dockerfile)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  fuseki:
    image: stain/jena-fuseki:latest
    ports:
      - "3030:3030"
    volumes:
      - fuseki_data:/fuseki

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - FUSEKI_ENDPOINT=http://fuseki:3030/waste_management/sparql
      - DEBUG_MODE=false
    depends_on:
      - fuseki

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000

volumes:
  fuseki_data:
```

### Déploiement Production

```bash
# Build Docker images
docker-compose build

# Lancer services
docker-compose up -d

# Vérifier logs
docker-compose logs -f

# Arrêter services
docker-compose down
```

---

## Environment-Specific Configs

### Development (.env.development)
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
CACHE_ENABLED=false
RATE_LIMIT_ENABLED=false
```

### Production (.env.production)
```env
DEBUG_MODE=false
LOG_LEVEL=INFO
CACHE_ENABLED=true
RATE_LIMIT_ENABLED=true
CORS_ORIGINS=https://ecotravel.com
SECRET_KEY=your-secure-key-here
```

### Testing (.env.test)
```env
DEBUG_MODE=true
FUSEKI_ENDPOINT=http://localhost:3030/test
DATABASE_URL=sqlite:///./test.db
```

---

## Checkliste Configuration Complète

- [ ] `.env` configuré avec paramètres corrects
- [ ] Fuseki démarré et accessible
- [ ] Backend démarré sans erreurs
- [ ] Frontend construit et accessible
- [ ] CORS configuré pour le domain
- [ ] Logging activé et journalisé
- [ ] Cache optimisé si haute charge
- [ ] Rate limiting configuré pour production
- [ ] Base de données initialisée (si utilisée)
- [ ] Certificats SSL en place (production)
- [ ] Backup automatique des données configuré

---

**Configuration mise à jour: 04 novembre 2025**
