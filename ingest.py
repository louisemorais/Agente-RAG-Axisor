import os

from dotenv import load_dotenv

from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

load_dotenv()

DATA_DIR = "data"
LANCEDB_URI = "tmp/lancedb"
TABLE_NAME = "axisor_knowledge"


def build_knowledge() -> Knowledge:
    vector_db = LanceDb(
        uri=LANCEDB_URI,
        table_name=TABLE_NAME,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    )
    return Knowledge(vector_db=vector_db)


if __name__ == "__main__":
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit(
            "GOOGLE_API_KEY não encontrada. Copie .env.example para .env e "
            "preencha sua chave da Gemini API antes de rodar a ingestão."
        )

    knowledge = build_knowledge()

    print(f"Ingerindo documentos de '{DATA_DIR}/' em LanceDB ({LANCEDB_URI})...")
    knowledge.add_content(path=DATA_DIR)
    print("Ingestão concluída! Agora rode: python chat.py para conversar com o agente")
