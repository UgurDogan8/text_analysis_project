import re
from collections import Counter

def istatistik_hesapla(dosya_yolu):
    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as dosya:
            metin = dosya.read()
    except FileNotFoundError:
        return "Dosya bulunamadı."

    # Harf sayısı
    harf_sayısı = len(re.findall(r'\w', metin))

    # Kelime sayısı
    kelime_sayısı = len(re.findall(r'\b\w+\b', metin))

    # Etkisiz kelime sayısı (varsayılan bir etkisiz kelime listesi kullanıldı)
    etkisiz_kelimeler = set([
        'bir', 've', 'ama', 'veya', 'gibi', 'şu', 'bu', 'o', 'şöyle', 'böyle'
    ])
    metin_kelimeler = re.findall(r'\b\w+\b', metin)
    etkisiz_kelime_sayısı = sum(1 for kelime in metin_kelimeler if kelime.lower() in etkisiz_kelimeler)

    # Kelime frekansları
    kelime_frekansları = Counter(metin_kelimeler)
    en_fazla_gecen_kelimeler = kelime_frekansları.most_common(5)
    en_az_gecen_kelimeler = kelime_frekansları.most_common()[:-6:-1]

   
    return {
        'harf_sayısı': harf_sayısı,
        'kelime_sayısı': kelime_sayısı,
        'etkisiz_kelime_sayısı': etkisiz_kelime_sayısı,
        'en_fazla_gecen_kelimeler': en_fazla_gecen_kelimeler,
        'en_az_gecen_kelimeler': en_az_gecen_kelimeler
    }

dosya_yolu = 'metin_adı.txt'  # Analiz edilecek metin belgesinin yolu
istatistikler = istatistik_hesapla(dosya_yolu)
print(istatistikler)
