## [2026-10-03] - Altyapı Kurulumu ve Veri Hazırlama (Data Ingestion)
- Proje iskeleti oluşturuldu, Git/GitHub bağlantısı yapıldı ve `student/efe-iskender` dalı (branch) aktif edildi.
- Gerekli kütüphaneler `requirements.txt` dosyasına eklendi ve sanal ortama (venv) kuruldu.
- İK Yönetmeliği PDF dosyası sisteme eklendi.
- `PyPDFLoader` ile doküman okuma ve `RecursiveCharacterTextSplitter` ile parçalama (chunking) işlemleri yapıldı.
- `sentence-transformers` kullanılarak metinler vektörlere çevrildi ve ChromaDB veritabanına kaydedildi.
- `chroma_db` klasörü `.gitignore` dosyasına eklenerek buluta yüklenmesi engellendi.

---

## [2026-10-03] - RAG zinciri çalışır hale geldi
### Added
- Veri kaynağı TED Üniversitesi İzin Yönergesi (7 sayfa) olarak güncellendi
- `app/rag_chain.py`: ChromaDB retrieval, prompt ve Groq LLM ile komut satırı soru-cevap akışı

### Changed
- Embedding modeli Türkçe destekli `paraphrase-multilingual-MiniLM-L12-v2` oldu
- Vektör deposu `langchain-chroma` paketine taşındı, dosya yolları proje köküne göre hesaplanıyor
- LLM sağlayıcısı Gemini yerine Groq (`openai/gpt-oss-120b`) olarak değiştirildi

### Notes
- Belgede olmayan bilgiler sorulduğunda (örn. evlilik izni gün sayısı) asistan "Belgede bu bilgi bulunmuyor" diyor