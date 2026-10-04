import sys
from pathlib import Path

from langchain_groq import ChatGroq

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "app"))
from rag_chain import LLM_MODEL, answer, load_vectorstore  # noqa: E402

# (soru, belgeye göre beklenen cevap)
TEST_SET = [
    ("3 yıldır çalışan bir personelin yıllık izni kaç gün?", "14 gün (Madde 5)"),
    ("10 yıllık personel kaç gün yıllık izin kullanır?", "20 gün (Madde 5)"),
    ("20 yıllık personelin yıllık izin hakkı nedir?", "26 gün (Madde 5)"),
    ("52 yaşında, 3 yıldır çalışan biri en az kaç gün izin alır?", "20 günden az olmaz (Madde 5)"),
    ("Yıllık izinde cumartesi nasıl hesaplanır?", "Cumartesi yarım gün düşülür (Madde 5)"),
    ("Hastalık raporu kaç gün içinde İK'ya teslim edilmeli?", "En geç 2 işgünü (Madde 6)"),
    ("Ücretsiz izin en fazla ne kadar sürer?", "1 yıl; doğum ve sağlıkta 24 aya kadar (Madde 7)"),
    ("İkinci bir ücretsiz izin ne zaman istenebilir?", "Dönüşten en az 1 yıl sonra (Madde 7)"),
    ("Ücretsiz izin bitince 3 gün işe gelmezsem ne olur?", "İstifa etmiş sayılır (Madde 7)"),
    ("İdari personele izin vermeye yetkili kişi kim?", "Birim yöneticisinin oluru ile Genel Sekreter (Madde 9)"),
    ("Evlilik izni kaç gün?", "Belgede gün sayısı yok"),
    ("Doğum izni kaç hafta?", "Belgede hafta sayısı yok"),
    ("Türkiye'nin başkenti neresi?", "Belge kapsamı dışı, cevap verilmemeli"),
]


def main():
    store = load_vectorstore()
    llm = ChatGroq(model=LLM_MODEL, temperature=0)

    lines = ["# Değerlendirme Sonuçları", "", f"Model: `{LLM_MODEL}`", ""]
    for i, (soru, beklenen) in enumerate(TEST_SET, 1):
        cevap = answer(soru, store, llm)
        print(f"\n[{i}] {soru}\nBeklenen: {beklenen}\nCevap: {cevap}")
        lines += [
            f"## {i}. {soru}",
            f"**Beklenen:** {beklenen}",
            "",
            f"**Cevap:** {cevap}",
            "",
            "**Sonuç:** [ ] doğru  [ ] kısmen  [ ] yanlış",
            "",
        ]

    out = BASE_DIR / "docs" / "evaluation_results.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nSonuçlar kaydedildi: {out}")


if __name__ == "__main__":
    main()