# setup_knowledge_base.py

import json
import chromadb
from sentence_transformers import SentenceTransformer
from config import CHROMA_DB_PATH, KNOWLEDGE_BASE_FILE, EMBEDDING_MODEL_NAME

def setup_vector_db():
    """
    Carga los documentos, genera embeddings y los almacena en ChromaDB.
    """
    print("🚀 Iniciando la configuración de la base de datos vectorial...")

    # 1. Cargar el modelo de embeddings
    print(f"Cargando modelo de embeddings: {EMBEDDING_MODEL_NAME}")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    # 2. Cargar los documentos desde el archivo JSON
    print(f"Cargando documentos desde: {KNOWLEDGE_BASE_FILE}")
    with open(KNOWLEDGE_BASE_FILE, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    # 3. Crear la colección en ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection_name = "helpie_knowledge_base"
    
    # Eliminar la colección si ya existe para empezar de cero
    try:
        client.delete_collection(name=collection_name)
        print(f"Colección '{collection_name}' existente eliminada.")
    except ValueError:
        pass

    collection = client.create_collection(name=collection_name)
    print(f"Colección '{collection_name}' creada.")

    # 4. Generar embeddings y almacenar documentos
    ids = [str(i) for i in range(len(documents))]
    texts = [doc['content'] for doc in documents]
    metadatas = [{'source': doc['source']} for doc in documents]

    print("Generando embeddings y almacenando en ChromaDB...")
    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )
    
    print("✅ Base de datos vectorial configurada exitosamente.")
    print(f"Se han almacenado {len(documents)} documentos.")

if __name__ == "__main__":
    setup_vector_db()
