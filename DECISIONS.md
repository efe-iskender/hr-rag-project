# Decisions

Bu dosya, proje sürecinde alınan önemli teknik ve mimari kararları kaydeder.
Değişen kararlar silinmez, **Revised** olarak güncellenir.

---

## 1) Veri kaynağı: TED Üniversitesi İzin Yönergesi
**Decision:** Örnek belge olarak TED Üniversitesi İzin Yönergesi (KYS-YN-01, Rev. 5, 20.01.2022, 7 sayfa) kullanılır.

**Reasoning:**
- İlk denenen PDF bir kurumun uzman personelinin görevlendirilmesi ve sınavlarıyla ilgiliydi. Arama testlerinde izin haklarıyla ilgili sorulara karşılık gelen içerik bulunamadı.
- Yeni yönerge yıllık izin, mazeret izni, hastalık izni ve ücretsiz izin gibi proje senaryosuna uygun konuları maddeler halinde içeriyor.

**Alternatives considered:**
- İlk PDF'i tutmak ve soruları ona göre değiştirmek
- Başka üniversite yönergeleri (içerikleri tam doğrulanamadı)

**Consequence:**
- Belgede evlilik izni için gün sayısı yok. Bu, asistanın "bilgi yok" davranışını test etmek için kullanılıyor.
- Eski sürümde farklı değerler olduğu için belgenin güncel sürümü kullanılmalı.

**Status:** Revised

---

## 2) Vector database: ChromaDB
**Decision:** Vektör deposu olarak **ChromaDB** kullanılır (`langchain-chroma` paketi ile).

**Reasoning:**
- Yerel çalışır, ayrı bir sunucu gerektirmez.
- Diske kaydedilir (`chroma_db/`), her çalıştırmada yeniden embedding gerekmez.
- LangChain ile entegrasyonu basit ve proje ölçeğine uygun.

**Alternatives considered:**
- FAISS

**Consequence:**
- `chroma_db/` klasörü `.gitignore` içinde. Repoyu çeken kişinin önce `python app/data_ingestion.py` çalıştırması gerekir.
- Ingestion her çalışmada eski koleksiyonu silip yeniden oluşturur, böylece parçalar çoğalmaz.

**Status:** Confirmed

---

## 3) Embedding modeli: çok dilli model
**Decision:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` kullanılır.

**Reasoning:**
- Belge ve sorular Türkçe. İlk kullanılan `all-MiniLM-L6-v2` ağırlıklı olarak İngilizce için uygundur.
- Yeni model Türkçeyi destekler ve ücretsiz olarak yerelde çalışır.

**Alternatives considered:**
- `all-MiniLM-L6-v2` (ilk seçim)
- Ücretli API tabanlı embedding servisleri

**Consequence:**
- Model ilk çalıştırmada indirilir (yaklaşık 470 MB).
- Embedding modeli değiştiği için veritabanı yeniden oluşturulmak zorundadır.

**Status:** Revised

---

## 4) Chunking ve metin temizleme
**Decision:** `RecursiveCharacterTextSplitter` ile `chunk_size=1000`, `chunk_overlap=200` kullanılır. Parçalamadan önce her sayfada tekrar eden üstbilgi satırları silinir.

**Reasoning:**
- Belge küçük ve her maddesi kısa. Bu boyut bir maddeyi genelde tek parçada tutuyor.
- Her sayfanın başındaki "TED ÜNİVERSİTESİ İZİN YÖNERGESİ / Doküman No / TASNİF DIŞI" metni tüm parçalara karışıyor ve benzerlik skorlarını birbirine yaklaştırıyordu.

**Alternatives considered:**
- Madde bazlı parçalama (denenmedi, ileride değerlendirilebilir)
- Üstbilgiyi temizlemeden devam etmek

**Consequence:**
- Üstbilgi temizlenmeden önce 13 sorudan 3'ü yanlış cevaplandı. Temizlik ve top-k artırımından sonra hepsi belgeyle uyumlu çıktı.
- Temizleme kuralları bu belgeye özel. Başka bir belgede `HEADER_PREFIXES` güncellenmeli.

**Status:** Confirmed

---

## 5) LLM: Groq üzerinden `openai/gpt-oss-120b`
**Decision:** Cevap üretimi için Groq API ve `openai/gpt-oss-120b` modeli kullanılır.

**Reasoning:**
- İlk planlanan Gemini ile sürekli hata alındı, bu yüzden bırakıldı.
- Groq ücretsiz katman sunuyor ve LangChain ile `langchain-groq` üzerinden kolay bağlanıyor.
- İlk denenen `llama-3.3-70b-versatile` hesapta bulunamadı (404). Hesabın erişebildiği modeller API'den listelenip uygun biri seçildi.

**Alternatives considered:**
- Google Gemini
- `openai/gpt-oss-20b` ve `qwen/qwen3.8-27b` (yedek adaylar)
- Yerel açık kaynak model

**Consequence:**
- API anahtarı `.env` dosyasında tutulur ve `.gitignore` ile korunur.
- Model kataloğu ve ücretsiz limitler zamanla değişebilir. Model adı `app/rag_chain.py` içindeki `LLM_MODEL` sabitinde.

**Status:** Revised

---

## 6) Retrieval ve prompt stratejisi
**Decision:** Benzerlik araması ile en yakın 6 parça (`TOP_K = 6`) getirilir. Prompt, modelden yalnızca verilen bağlama dayanmasını, bilgi yoksa "Belgede bu bilgi bulunmuyor." demesini ve cevabın sonunda madde ve sayfa belirtmesini ister. `temperature=0` kullanılır.

**Reasoning:**
- 4 parça ile bazı sorularda doğru madde ilk sonuçlara giremedi.
- Belge küçük olduğu için daha fazla parça göndermek maliyetsiz.
- Belge dışı bilgiyle cevap uydurmanın önüne geçilmek isteniyor.

**Alternatives considered:**
- `TOP_K = 4` (ilk değer)
- Prompt'ta kısıtlama olmadan serbest cevap

**Consequence:**
- Belgede olmayan sorularda (evlilik izni gün sayısı, genel kültür sorusu) asistan uydurma yapmıyor.
- Cevaplar bazen kısa kalıyor. Prompt ileride "belge ne diyor" bilgisini de eklemesi için iyileştirilebilir.

**Status:** Confirmed

---

## 7) Arayüz: komut satırı
**Decision:** MVP için arayüz olarak CLI kullanılır.

**Reasoning:**
- Önce çekirdek RAG zincirinin doğruluğu önemli.
- Guide, arayüzü zorunlu tutmuyor.

**Alternatives considered:**
- Streamlit (zaman kalırsa opsiyonel)

**Consequence:**
- Kullanıcı etkileşimi `python app/rag_chain.py` ile terminalden yapılır.

**Status:** Proposed

---

## Writing Rules
- Kararlar mümkün olduğunca net yazılmalıdır.
- Kararın nedeni belirtilmeden sadece sonuç yazılmamalıdır.
- Önemli bir karar değişirse eski karar silinmemeli; **Revised** olarak güncellenmelidir.
- Bu dosya, teknik düşünme biçimini görünür kılmak için tutulur.
