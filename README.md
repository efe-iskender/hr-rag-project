# Akıllı İK Yönetmelik Asistanı (HR RAG Assistant)

## 1. Project Overview
Bu proje, **İnsan Kaynakları (İK) izin yönergeleri** kapsamında geliştirilen bir **GenAI / RAG application**'dır.

Projenin temel amacı: **Çalışanların doğal dilde sorduğu izin sorularını, yönergedeki ilgili maddeye dayanarak madde ve sayfa referansıyla cevaplamak.**

## 2. Problem Definition
### Problem
Uzun İK yönetmelikleri ve yönergeleri (PDF) içinde izin hakları veya prosedürler gibi bilgileri manuel aramak zaman alır ve metnin yanlış yorumlanmasına yol açabilir.

### Why this problem matters
Çalışanlar sık karşılaşılan sorularının ("Yıllık iznim kaç gün?", "Hastalık raporunu ne zaman teslim etmeliyim?") cevabını hızlıca ve kaynağıyla birlikte görmek ister. İK birimi de aynı soruları tekrar tekrar cevaplamak zorunda kalmaz.

### Target user / use case
Yönergedeki hakları ve prosedürleri öğrenmek isteyen çalışanlar ve İK birimi. Kullanıcı terminalden Türkçe bir soru sorar, sistem belgeden bulduğu maddeye dayanarak cevap verir.

## 3. Solution Approach
Bu proje aşağıdaki genel akışla çalışır:

1. Data / document ingestion (PDF okuma)
2. Preprocessing / cleaning (tekrar eden sayfa üstbilgisini silme)
3. Chunking
4. Embedding
5. Vector store
6. Retrieval
7. Prompt construction
8. LLM response generation

### Architecture summary
PDF, `PyPDFLoader` ile sayfa sayfa okunur ve her sayfanın başındaki tekrar eden üstbilgi satırları temizlenir. Metin `RecursiveCharacterTextSplitter` ile 1000 karakterlik, 200 karakter çakışmalı parçalara bölünür. Her parça, Türkçe destekli `paraphrase-multilingual-MiniLM-L12-v2` modeliyle vektöre çevrilir ve ChromaDB'ye kaydedilir. Kullanıcı bir soru sorduğunda soru aynı modelle vektöre çevrilir ve veritabanından en yakın 6 parça getirilir. Bu parçalar, modele yalnızca verilen bağlama dayanmasını ve bilgi yoksa bunu söylemesini isteyen bir prompt'a yerleştirilir. Groq üzerindeki `openai/gpt-oss-120b` modeli cevabı üretir ve cevabın sonunda madde ve sayfa numarasını belirtir.

## 4. Tech Stack

| Component       | Choice                                              | Notes                                   |
| --------------- | --------------------------------------------------- | --------------------------------------- |
| Language        | Python                                              | Python 3.10                             |
| Framework       | LangChain                                           | `langchain-chroma`, `langchain-groq`    |
| LLM             | `openai/gpt-oss-120b`                               | Groq API üzerinden                      |
| Embedding Model | `paraphrase-multilingual-MiniLM-L12-v2`             | Türkçe destekli, yerelde çalışır        |
| Vector DB       | ChromaDB                                            | Yerel, `chroma_db/` klasörüne kaydedilir |
| UI / Interface  | CLI                                                 | Terminalden soru-cevap                  |
| Evaluation      | Manuel inceleme, 13 soruluk set                     | `tests/eval_questions.py`               |

## 5. Project Structure
```text
HR_RAG_Project/
├── app/
│   ├── data_ingestion.py   # PDF okuma, temizleme, chunking, embedding, ChromaDB
│   ├── rag_chain.py        # Retrieval + prompt + LLM, komut satırı arayüzü
│   └── search_test.py      # Retrieval kalitesini incelemek için yardımcı script
├── data/
│   └── tedu_izin_yonergesi.pdf
├── docs/
│   └── evaluation_results.md
├── tests/
│   └── eval_questions.py
├── README.md
├── TASKS.md
├── CHANGELOG.md
├── DECISIONS.md
├── PROJECT_CONTEXT.md
├── requirements.txt
└── .gitignore
```

### Folder descriptions
- `app/`: Ana application code
- `data/`: Kaynak belge (TED Üniversitesi İzin Yönergesi)
- `docs/`: Değerlendirme çıktıları
- `tests/`: Değerlendirme soru seti ve çalıştırma scripti

## 6. Setup
### Requirements
- Python version: **3.10**
- Gerekli API key: **var** (Groq, ücretsiz hesapla alınabilir: console.groq.com)

### Installation
```bash
git clone https://github.com/efe-iskender/hr-rag-project.git
cd hr-rag-project
git checkout student/efe-iskender

python -m venv venv
venv\Scripts\activate        # Windows (macOS/Linux: source venv/bin/activate)

pip install -r requirements.txt
```

### Environment Variables
Proje klasörünün kökündeki `.env.example` dosyasını `.env` adıyla kopyalayıp Groq anahtarını yazın. `.env` dosyası `.gitignore` içindedir, GitHub'a gitmez.

```env
GROQ_API_KEY=buraya_kendi_anahtarinizi_yazin
```

## 7. Run Instructions
Önce belgeyi işleyip vektör veritabanını oluşturun (`chroma_db/` repoda bulunmaz, bu adım zorunludur):

```bash
python app/data_ingestion.py
```

Sonra asistanı başlatın ve soru sorun (çıkmak için `q` yazın):

```bash
python app/rag_chain.py
```

Değerlendirme setini çalıştırmak için:

```bash
python tests/eval_questions.py
```

Sonuçlar `docs/evaluation_results.md` dosyasına yazılır. İlk çalıştırmada embedding modeli (yaklaşık 470 MB) indirilir.

## 8. Example Input / Output
### Example input
```text
52 yaşında, 3 yıldır çalışan biri en az kaç gün izin alır?
```

### Example output
52 yaşındaki ve 3 yıldır çalışan personel için temel yıllık izin 14 gündür. Ancak 50 yaş ve üzeri personele verilecek izin süresinin 20 günden az olamayacağı hükmü nedeniyle en az 20 gün izin alır. Kaynak: Madde 5 – Yıllık İzin, sayfa 2.

### Example: belgede olmayan bilgi
```text
Evlilik izni kaç gün?
```

Yönerge evlilik halinde 4857 sayılı İş Kanunu uyarınca ücretli izin verildiğini belirtir ancak gün sayısı vermez. Asistan cevap uydurmak yerine "Belgede bu bilgi bulunmuyor." yanıtını verir.

## 9. Key Features
- Türkçe soru ve cevap
- Her cevapta madde ve sayfa referansı
- Belgede olmayan bilgide uydurma yapmaması
- Aynı soru setiyle tekrarlanabilir değerlendirme

## 10. Evaluation
13 soruluk bir set hazırlandı: 10 soru belgede cevabı olan, 2 soru belgede bilgisi olmayan, 1 soru belge kapsamı dışında. Sonuçlar manuel incelemeyle değerlendirildi.

- **İlk çalıştırma:** 9 doğru, 1 kısmen doğru, 3 yanlış. Üç hata da retrieval kaynaklıydı, doğru madde ilk sonuçlara girmiyordu ve model dürüstçe "bilgi yok" diyordu.
- **Düzeltmeler:** Her sayfada tekrar eden üstbilgi temizlendi ve getirilen parça sayısı 4'ten 6'ya çıkarıldı.
- **Son çalıştırma:** 13 sorunun hepsi belgeyle uyumlu çıktı.

Ayrıntılar `docs/evaluation_results.md` içindedir.

## 11. Limitations
Bu proje aşağıdaki sınırlılıklara sahiptir:
- Tek ve küçük bir belge (7 sayfa) ile çalışır, sonuçlar başka belgelere genellenmeyebilir.
- Test seti küçüktür ve düzeltmeler yapılırken aynı sorular kullanıldı, bu yüzden son sonuç olduğundan iyimser görünebilir.
- Sayfa üstbilgisi temizleme kuralları bu belgeye özeldir, başka bir belgede güncellenmelidir.
- Cevaplar bazen kısadır. Örneğin belgede sayı olmayan sorularda belgenin ne dediğini değil sadece "bilgi yok" bilgisini verir.
- Asistan hukuki danışmanlık vermez, yalnızca yönerge metnini aktarır.
- Groq ücretsiz katmanının limitleri ve model kataloğu zamanla değişebilir.
- Arayüz yalnızca komut satırıdır.

## 12. Future Improvements
İleride aşağıdaki geliştirmeler yapılabilir:
- Madde bazlı parçalama ile referans doğruluğunu artırmak
- Prompt'u, bilgi bulunamayan durumlarda belgenin ilgili hükmünü de aktaracak şekilde geliştirmek
- Streamlit ile web arayüzü eklemek
- Birden fazla belgeyi desteklemek
- Daha geniş ve otomatik bir değerlendirme seti hazırlamak

## 13. Project Status
**Status:** MVP ready

## 14. Repository Workflow
- Geliştirme `student/efe-iskender` branch'i üzerinde yapılmıştır.
- `main` branch yalnızca kontrollü ve temiz sürümler için kullanılmalıdır.
- Önemli değişiklikler `CHANGELOG.md` içinde takip edilmiştir.
- Alınan teknik kararlar `DECISIONS.md`, görev takibi `TASKS.md` içindedir.

## 15. Author
- Name: Efe İskender
- Final Project Topic: Akıllı İK Yönetmelik Asistanı (RAG tabanlı soru-cevap)
