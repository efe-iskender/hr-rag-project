import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def process_pdf(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "data", file_name)
    
    print(f"Dosya okunuyor: {file_path}")
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(f"Başarılı! Toplam sayfa sayısı: {len(docs)}")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Metin başarıyla {len(chunks)} parçaya (chunk) bölündü.")
    
    print("Yapay zeka modeli indiriliyor ve veritabanı hazırlanıyor (Bu işlem biraz sürebilir)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    db_dir = os.path.join(current_dir, "chroma_db")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_dir
    )
    
    print(f"Harika! Tüm veriler başarıyla vektörlere çevrildi ve '{db_dir}' klasörüne kaydedildi.")
    return vectorstore

if __name__ == "__main__":
    process_pdf("ik_yonetmelik.pdf")