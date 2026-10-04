from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

HEADER_PREFIXES = ("TED ÜN", "Doküman No", "KYS-YN-01", "TASN")


def clean_page(text: str) -> str:
    # her sayfada tekrar eden üstbilgi satırlarını at
    lines = [
        line for line in text.splitlines()
        if not line.strip().startswith(HEADER_PREFIXES)
    ]
    return "\n".join(lines).strip()

def process_pdf(file_name: str):
    file_path = DATA_DIR / file_name
    print(f"Dosya okunuyor: {file_path}")
    docs = PyPDFLoader(str(file_path)).load()
    print(f"Toplam sayfa sayısı: {len(docs)}")
    for d in docs:
        d.page_content = clean_page(d.page_content)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} parçaya bölündü.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    old_db = Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)
    old_db.delete_collection()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(DB_DIR),
    )
    print(f"Vektör veritabanı kaydedildi: {DB_DIR}")
    return vectorstore


if __name__ == "__main__":
    process_pdf("tedu_izin_yonergesi.pdf")