from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
db = Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)

sorular = [
    "10 yıllık personel kaç gün yıllık izin kullanır?",
    "20 yıllık personelin yıllık izin hakkı nedir?",
    "Yıllık izinde cumartesi nasıl hesaplanır?",
]
for soru in sorular:
    print("\nSORU:", soru)
    for doc, skor in db.similarity_search_with_score(soru, k=4):
        icerik = doc.page_content
        sayfa = doc.metadata.get("page", 0) + 1
        print(
            f"  sayfa {sayfa} | mesafe {skor:.1f} | "
            f"'Hizmet süresi' var: {'Hizmet süresi' in icerik} | "
            f"'Cumartesi' var: {'Cumartesi' in icerik}"
        )