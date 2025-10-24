# config.py

import os
from dotenv import load_dotenv

load_dotenv() # Cargar variables desde el archivo .env

# --- Claves de API ---
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "tu_email@ejemplo.com")
OPENFDA_API_KEY = os.getenv("OPENFDA_API_KEY", "tu_clave_openFDA")
DETECTLANGUAGE_API_KEY = os.getenv("DETECTLANGUAGE_API_KEY", "tu_clave_detectlanguage")
LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL", "https://libretranslate.de/translate")

# --- Configuración de Modelos y Bases de Datos ---
ORCHESTRATOR_MODEL_NAME = os.getenv("ORCHESTRATOR_MODEL_NAME", "google/flan-t5-large")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
KNOWLEDGE_BASE_FILE = os.getenv("KNOWLEDGE_BASE_FILE", "./data/knowledge_base.json")

# --- Configuración de Caché ---
# Tiempo de vida en segundos para el caché (ej. 1 hora)
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
