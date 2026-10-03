## [1. Gün] - Altyapı Kurulumu ve Veri Hazırlama (Data Ingestion)
- Proje iskeleti oluşturuldu, Git/GitHub bağlantısı yapıldı ve `student/efe-iskender` dalı (branch) aktif edildi.
- Gerekli kütüphaneler `requirements.txt` dosyasına eklendi ve sanal ortama (venv) kuruldu.
- İK Yönetmeliği PDF dosyası sisteme eklendi.
- `PyPDFLoader` ile doküman okuma ve `RecursiveCharacterTextSplitter` ile parçalama (chunking) işlemleri yapıldı.
- `sentence-transformers` kullanılarak metinler vektörlere çevrildi ve ChromaDB veritabanına kaydedildi.
- `chroma_db` klasörü `.gitignore` dosyasına eklenerek buluta yüklenmesi engellendi.