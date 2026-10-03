from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)

soru = "Evlilik izni kaç gün?"
print(f"SORU: {soru}")
for doc, skor in db.similarity_search_with_score(soru, k=3):
    print("Sayfa:", doc.metadata.get("page"), "| mesafe:", round(skor, 3))
    print(doc.page_content)
    print("-" * 40)