# Changelog

Bu dosya, proje sürecindeki önemli değişiklikleri tarih bazlı olarak kaydetmek için kullanılır.
Her küçük commit'i buraya yazmak gerekmez. Milestone seviyesindeki anlamlı değişiklikler eklenmelidir.

## [2026-10-03] - Altyapı kurulumu ve veri hazırlama (Data Ingestion)
### Added
- Proje iskeleti oluşturuldu, Git/GitHub bağlantısı yapıldı ve `student/efe-iskender` dalı (branch) aktif edildi.
- Gerekli kütüphaneler `requirements.txt` dosyasına eklendi ve sanal ortam (venv) kuruldu.
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

---

## [2026-10-04] - Retrieval iyileştirmesi, değerlendirme ve proje belgeleri
### Added
- 13 soruluk değerlendirme seti ve çalıştırma scripti (`tests/eval_questions.py`), sonuçlar `docs/evaluation_results.md` içinde
- PROJECT_CONTEXT, DECISIONS ve TASKS dosyaları gerçek proje bilgileriyle dolduruldu
- README; kurulum, çalıştırma, örnek çıktı, değerlendirme ve limitasyonlarla tamamlandı

### Changed
- Her sayfada tekrar eden üstbilgi satırları chunking öncesinde temizlenmeye başlandı
- Getirilen parça sayısı (`TOP_K`) 4'ten 6'ya çıkarıldı

### Fixed
- Madde 5'teki yıllık izin süreleri ve Cumartesi hesabı için doğru parça bulunamıyordu, "Belgede bu bilgi bulunmuyor" cevabı veriliyordu. Düzeltmeden sonra 13 sorunun hepsi belgeyle uyumlu cevaplandı.

### Notes
- Test seti küçük ve tek belgeyle sınırlı, düzeltmeler aynı sorularla yapıldı (bkz. README Limitations)
- Proje, MVP seviyesinde çalışan RAG asistanı durumunda
