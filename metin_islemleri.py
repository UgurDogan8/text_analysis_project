import string
def dosya_oku(dosya_yolu):
    with open(dosya_yolu, 'r') as dosya:
        icerik = dosya.read()
    return icerik

def noktalama_isaretlerini_kaldir(metin):
    return metin.translate(str.maketrans('','', string.punctuation))

def kelimelere_ayir(metin):
    return metin.split()

def dosya_islemleri(dosya_yolu):
    icerik = dosya_oku(dosya_yolu)
    yeni_metin = noktalama_isaretlerini_kaldir(icerik)
    kelimeler = kelimelere_ayir(yeni_metin)
    return kelimeler

dosya_yolu = 'ornek.txt'
kelimeler = dosya_islemleri(dosya_yolu)
print(kelimeler)