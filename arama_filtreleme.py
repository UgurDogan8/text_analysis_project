def dosya_arama(dosya_adi, aranan_metin):
    bulunan_satirlar = []
    with open(dosya_adi, 'r', encoding='utf-8') as dosya:
        satirlar = dosya.readlines()
        for satir in satirlar:
            if aranan_metin in satir:
                bulunan_satirlar.append(satir)
    return bulunan_satirlar

def dosya_filtrele(dosya_adi, filtre):
    uygun_satirlar = []
    with open(dosya_adi, 'r', encoding='utf-8') as dosya:
        satirlar = dosya.readlines()
        for satir in satirlar:
            if filtre(satir):
                uygun_satirlar.append(satir)
    return uygun_satirlar

# Uzun satır filtreyi tanımla
def uzun_satir_filtre(satir):
    return len(satir) > 50  # 50 karakterden uzun satırları seç

# Örnek Kullanım:
dosya_adi = 'deneme.txt'

# Uzun satırları filtrele
uygun_satirlar = dosya_filtrele(dosya_adi, uzun_satir_filtre)
print("Uzun Satırlar:")
for satir in uygun_satirlar:
    print(satir.strip())
    print()  # Her satırın altına boş bir satır ekle
