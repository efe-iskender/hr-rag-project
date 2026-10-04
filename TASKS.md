# Tasks

Bu dosya, proje sürecini yönetmek için kullanılır. Görevler düzenli olarak güncellenir.

## Project status
- **Current phase:** Testing
- **Current focus:** Proje belgelerinin (PROJECT_CONTEXT, DECISIONS, TASKS) tamamlanması
- **Last updated:** 2026-10-04

---

## Backlog
- [ ] Madde bazlı chunking denemesi (referans kalitesini artırmak için)
- [ ] Prompt'u iyileştir: belgede sayı yoksa belgenin ne dediğini de belirt
- [ ] Streamlit arayüzü (opsiyonel)
- [ ] İkinci bir belge ekleme (opsiyonel)

## In Progress
- [ ] PROJECT_CONTEXT.md, DECISIONS.md ve TASKS.md içeriklerinin tamamlanması
- [ ] README.md'nin doldurulması

## Blocked
- Şu an bloke olan görev yok.

## Done
- [x] Repository ve `student/efe-iskender` branch'i oluşturuldu
- [x] Sanal ortam ve requirements.txt hazırlandı
- [x] Veri kaynağı olarak TED Üniversitesi İzin Yönergesi seçildi
- [x] Ingestion pipeline yazıldı (PDF okuma, üstbilgi temizleme, chunking, embedding, ChromaDB)
- [x] Embedding modeli Türkçe destekli modelle değiştirildi
- [x] LLM Gemini yerine Groq olarak değiştirildi
- [x] RAG zinciri yazıldı (`app/rag_chain.py`)
- [x] 13 soruluk değerlendirme seti hazırlandı ve çalıştırıldı (`tests/eval_questions.py`)
- [x] Retrieval hatası teşhis edilip düzeltildi (üstbilgi temizliği, top-k artırımı)

---

## Phase 1 — Problem Definition and Scope
- [x] Problem statement yaz
- [x] Target user / use case belirle
- [x] Scope dışı alanları tanımla
- [x] Başarı kriterlerini yaz

## Phase 2 — Data and Documents
- [x] Data source / document source belirle
- [x] Sample input topla
- [x] Input formatını incele
- [x] Gerekliyse preprocessing planı çıkar

## Phase 3 — RAG Design
- [x] Chunking strategy belirle
- [x] Embedding model seç
- [x] Vector DB seç
- [x] Retrieval yaklaşımını tanımla
- [x] Prompt template taslağı hazırla

## Phase 4 — Core Implementation
- [x] Data loader / parser yaz
- [x] Chunking pipeline oluştur
- [x] Embedding + vector store entegrasyonu yap
- [x] Retriever oluştur
- [x] LLM response pipeline bağla

## Phase 5 — Testing and Improvement
- [x] Örnek query seti hazırla
- [x] Basit evaluation yap
- [x] Retrieval hatalarını not et
- [ ] Prompt iyileştirmesi yap
- [ ] Edge case kontrolü yap

## Phase 6 — Finalization
- [ ] README tamamla
- [ ] CHANGELOG güncelle
- [ ] Örnek output ekle
- [ ] Final demo hazırlığı yap
- [ ] Repository cleanup yap

---

## Milestones
### Milestone 1
- [x] Proje fikri onaylandı
- [x] Repository açıldı
- [x] Student branch oluşturuldu

### Milestone 2
- [x] Data source netleşti
- [x] İlk mimari taslak oluştu
- [x] İlk parsing / preprocessing adımı tamamlandı

### Milestone 3
- [x] Retrieval pipeline çalışıyor
- [x] Prompt + LLM zinciri çalışıyor
- [x] İlk demo alınabiliyor

### Milestone 4
- [ ] README taslağı tamamlandı
- [ ] Sonuçlar iyileştirildi
- [ ] Final sunuma hazır hale gelindi
