def jaccard_benzerlik(metin1, metin2):

    kelimeler1 = set(metin1.split())
    kelimeler2 = set(metin2.split())

    ortak_kelimeler = kelimeler1.intersection(kelimeler2)
    tum_kelimeler = kelimeler1.union(kelimeler2)

    benzerlik = len(ortak_kelimeler) / len(tum_kelimeler)
    return benzerlik

