# Project Context

Bu dosya, projenin arka planını, iş bağlamını, scope sınırlarını ve temel varsayımlarını açıklar.

## 1. Project Title
Akıllı İK Yönetmelik Asistanı (HR RAG Assistant)

## 2. Project Goal
Bu projenin temel amacı:
Çalışanların doğal dilde sorduğu izin ve prosedür sorularını, İK yönergesindeki ilgili maddeye dayanarak, madde ve sayfa referansıyla cevaplayan RAG tabanlı bir soru-cevap asistanı (MVP) geliştirmek.

## 3. Business / Use Case Context
İnsan Kaynakları (HR). Çalışanların izin hakları ve izin prosedürleri hakkındaki sorularını yönerge metnini manuel okumadan cevaplamak hedeflenir. Örnek belge olarak TED Üniversitesi İzin Yönergesi (KYS-YN-01, Rev. 5, 20.01.2022) kullanılmaktadır.

## 4. Problem Statement
Uzun İK yönetmelikleri ve yönergeleri (PDF) içinde izin hakları veya prosedürler gibi bilgileri manuel aramak zaman kaybıdır. Ayrıca metnin yanlış yorumlanma riski vardır. Çalışan, sorusunun cevabını ilgili maddeyle birlikte hızlıca görmek ister.

## 5. Target User
Yönergedeki hakları ve prosedürleri öğrenmek isteyen çalışanlar ve sık sorulan sorulara cevap vermek zorunda kalan İK birimi.

## 6. Target Workflow
**PDF → Metin çıkarma → Üstbilgi temizleme → Chunking → Embedding → ChromaDB → Soru → Benzerlik araması (top 6) → Prompt → Groq LLM → Referanslı cevap**

Yönerge PDF'i bir kez işlenir ve vektör veritabanına kaydedilir (`app/data_ingestion.py`). Kullanıcı soru sorduğunda en ilgili 6 parça getirilir, prompt'a yerleştirilir ve LLM yalnızca bu bağlama dayanarak cevap üretir (`app/rag_chain.py`).

## 7. In Scope
- Tek bir İK izin yönergesi PDF'i üzerinden soru-cevap
- Türkçe soru ve Türkçe cevap
- Cevapta madde ve sayfa referansı
- Belgede olmayan bilgi sorulduğunda "Belgede bu bilgi bulunmuyor" demesi
- Komut satırı (CLI) arayüzü
- 13 soruluk basit bir değerlendirme seti ve sonuçların kaydı

## 8. Out of Scope
- Birden fazla belge veya belge yükleme arayüzü
- Web arayüzü (opsiyonel, zaman kalırsa)
- Kişiye özel hesaplama (örn. kişisel izin bakiyesi)
- Hukuki danışmanlık veya belge dışı mevzuat bilgisi
- Production deployment ve kimlik doğrulama
- Model fine-tuning

## 9. Input Types
- PDF (seçilebilir metin içeren, taranmış olmayan tek belge)

## 10. Expected Output
- Answer generation: Kullanıcının sorusuna, yönergedeki maddeye dayanan ve madde/sayfa referansı içeren kısa Türkçe cevap
- Belgede karşılığı olmayan sorularda cevap uydurmadan bunu belirten yanıt

## 11. Technical Direction
### Planned components
- Document loader (PyPDFLoader)
- Text cleaning (sayfa üstbilgisi temizleme)
- Chunking (RecursiveCharacterTextSplitter)
- Embedding model
- Vector DB
- Retriever (similarity search, top 6)
- Prompt template
- LLM

### Initial tech choices
- **Language:** Python 3.10
- **Framework:** LangChain
- **LLM:** Groq üzerinden `openai/gpt-oss-120b`
- **Embedding Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Vector DB:** ChromaDB
- **Interface:** CLI

## 12. Constraints
- Zaman: 45 günlük proje süresi
- API: Groq ücretsiz katmanı ve limitleri
- Veri: Tek ve küçük bir belge (7 sayfa)
- LLM sağlayıcılarının model kataloğu zamanla değişebilir

## 13. Assumptions
- PDF'in metni seçilebilir ve düzgün okunabilir durumdadır
- Kullanılan yönerge sürümü geçerli kabul edilir
- Kullanıcılar soruları Türkçe sorar
- Kullanıcı, belgedeki bilgiyi yorumsuz ve referanslı almak ister

## 14. Risks
- Weak retrieval: Sayfa üstbilgisi parçalara karıştığında doğru madde bulunamadı. Üstbilgi temizlenerek ve top-k artırılarak giderildi.
- Hallucination: Model belgede olmayan bilgiyi uydurabilir. Prompt ile engellenmeye çalışıldı.
- Küçük test seti ve tek belge nedeniyle sonuçlar genellenemeyebilir
- Belge sürümü: Yönergenin eski sürümünde farklı değerler vardı (örn. yıllık izin süreleri)
- Ücretsiz API limitleri ve model kataloğu değişiklikleri

## 15. Success Criteria
- Belgede cevabı olan sorularda doğru değer ve doğru madde/sayfa referansı
- Belgede olmayan sorularda uydurma cevap verilmemesi
- Projenin README'deki adımlarla sıfırdan kurulup çalıştırılabilmesi
- Değerlendirme sonuçlarının `docs/` altında kayıt altında olması

## 16. Notes
- Veri kaynağı, ilk denenen PDF izin haklarını içermediği için TED Üniversitesi İzin Yönergesi ile değiştirildi (bkz. DECISIONS.md).
- Yönergenin evlilik izni için gün sayısı vermemesi, asistanın "bilgi yok" davranışını test etmek için kullanıldı.
