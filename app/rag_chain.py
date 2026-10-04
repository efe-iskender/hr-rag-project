from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_DIR = BASE_DIR / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "openai/gpt-oss-120b"
TOP_K = 6

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Sen bir İK izin yönergesi asistanısın. Sadece aşağıdaki bağlamdaki "
     "bilgiye dayanarak Türkçe cevap ver. Bağlamda cevap yoksa veya bir sayı "
     "belirtilmemişse 'Belgede bu bilgi bulunmuyor.' de, tahmin yürütme ve "
     "dışarıdan bilgi ekleme. Cevabın sonunda ilgili madde ve sayfa "
     "numarasını belirt.\n\nBağlam:\n{context}"),
    ("human", "{question}"),
])


def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(persist_directory=str(DB_DIR), embedding_function=embeddings)


def format_context(docs):
    # page 0'dan başlıyor, kullanıcıya 1'den başlayan numara gösteriyoruz
    return "\n\n".join(
        f"[Sayfa {d.metadata.get('page', 0) + 1}]\n{d.page_content}" for d in docs
    )


def answer(question: str, vectorstore, llm):
    docs = vectorstore.similarity_search(question, k=TOP_K)
    messages = PROMPT.format_messages(context=format_context(docs), question=question)
    return llm.invoke(messages).content


if __name__ == "__main__":
    store = load_vectorstore()
    model = ChatGroq(model=LLM_MODEL, temperature=0)
    print("İK İzin Asistanı hazır. Çıkmak için 'q' yaz.")
    while True:
        soru = input("\nSoru: ").strip()
        if soru.lower() in {"q", "çıkış"}:
            break
        if soru:
            print("\nCevap:", answer(soru, store, model))