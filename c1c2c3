# brains/c1_emergency.py

import chromadb
from Bio import Entrez
from config import NCBI_EMAIL, CHROMA_DB_PATH
from utils.cache import cache_api_call

class EmergencyBrain:
    """
    Cerebro especialista en primeros auxilios de emergencia.
    Utiliza una base de datos vectorial (ChromaDB) como fuente principal de conocimiento
    y PubMed como fuente de respaldo.
    """

    def __init__(self):
        Entrez.email = NCBI_EMAIL
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.client.get_collection(name="helpie_knowledge_base")

    @cache_api_call
    def _query_vector_db(self, query: str, n_results: int = 2) -> list[dict]:
        """Busca en la base de datos vectorial los documentos más relevantes."""
        results = self.collection.query(query_texts=[query], n_results=n_results)
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        return [{'content': doc, 'source': meta} for doc, meta in zip(documents, metadatas)]

    @cache_api_call
    def _query_pubmed(self, query: str, max_results: int = 2) -> list[dict]:
        """Realiza una búsqueda en PubMed como respaldo."""
        # ... (el código de PubMed de la versión anterior) ...
        try:
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            handle.close()
            id_list = record["IdList"]
            if not id_list: return []
            handle = Entrez.efetch(db="pubmed", id=id_list, rettype="abstract", retmode="text")
            articles = handle.read().split("\n\n\n")
            handle.close()
            results = []
            for article in articles:
                parts = article.split('\n')
                title = parts[0].strip() if parts else "Sin título"
                abstract = " ".join(parts[1:]).strip() if len(parts) > 1 else "Sin resumen."
                results.append({"title": title, "abstract": abstract, "source": "PubMed (NCBI)"})
            return results
        except Exception as e:
            print(f"Error al consultar PubMed: {e}")
            return []

    def process(self, query: str) -> str:
        """
        Procesa la consulta, priorizando la base de datos vectorial.
        """
        # 1. Buscar en nuestra base de conocimiento especializada
        kb_results = self._query_vector_db(query)
        
        response = "Como especialista en auxilios emergentes, te ofrezco la siguiente guía basada en protocolos de organizaciones líderes:\n\n"

        if kb_results:
            for result in kb_results:
                response += f"**Punto Clave ({result['source']}):** {result['content']}\n\n"
        else:
            # 2. Si no hay resultados en la KB, buscar en PubMed
            pubmed_results = self._query_pubmed(query)
            response += "No encontré información específica en mi base de datos principal, pero aquí tienes una guía basada en la literatura médica:\n\n"
            if pubmed_results:
                article = pubmed_results[0]
                response += f"**Evidencia Científica ({article['source']}):** {article['title']}\n"
                response += f"Resumen: {article['abstract'][:300]}...\n\n"
            else:
                response += "Para esta emergencia, la prioridad es llamar a los servicios de emergencia inmediatamente y seguir las indicaciones del operador.\n"

        response += "**Descargo de Responsabilidad:** Helpie es una herramienta educativa. En una emergencia real, llama a tu número de emergencia local sin demora."
        return response
