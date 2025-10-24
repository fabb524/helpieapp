# utils/cache.py

from cachetools import cached, TTLCache
from config import CACHE_TTL

# Crear una caché con un tiempo de vida (TTL) definido en config.py
# maxsize=100 significa que guardará hasta 100 resultados únicos
api_cache = TTLCache(maxsize=100, ttl=CACHE_TTL)

def cache_api_call(func):
    """
    Decorador para cachear llamadas a APIs.
    Utiliza el primer argumento de la función como clave de caché.
    """
    return cached(api_cache)(func)
