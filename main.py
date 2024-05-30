import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox, QInputDialog
import re
from collections import Counter
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        create_database()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Metin Analiz Arayüzü')

        # Ana widget ve layout
        centralWidget = QWidget()
        layout = QVBoxLayout()

        # Metin yükleme ve görüntüleme alanı
        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)

        # İkinci metin yükleme ve görüntüleme alanı
        self.textEdit2 = QTextEdit(self)
        layout.addWidget(self.textEdit2)

        # Metin yükleme düğmeleri
        loadButton1 = QPushButton('Metin 1 Yükle', self)
        loadButton1.clicked.connect(self.loadText)
        layout.addWidget(loadButton1)

        loadButton2 = QPushButton('Metin 2 Yükle', self)
        loadButton2.clicked.connect(self.loadText2)
        layout.addWidget(loadButton2)

        # Veritabanı işlevleri düğmeleri
        saveToDBButton = QPushButton('Veritabanına Kaydet', self)
        saveToDBButton.clicked.connect(self.saveTextToDB)
        layout.addWidget(saveToDBButton)

        updateInDBButton = QPushButton('Veritabanında Güncelle', self)
        updateInDBButton.clicked.connect(self.updateTextInDB)
        layout.addWidget(updateInDBButton)

        deleteFromDBButton = QPushButton('Veritabanından Sil', self)
        deleteFromDBButton.clicked.connect(self.deleteTextFromDB)
        layout.addWidget(deleteFromDBButton)

        loadFromDBButton = QPushButton('Veritabanından Metinleri Yükle', self)
        loadFromDBButton.clicked.connect(self.loadTextsFromDB)
        layout.addWidget(loadFromDBButton)

        # Analiz yapma düğmesi
        analyzeButton = QPushButton('Analiz Yap', self)
        analyzeButton.clicked.connect(self.analyzeText)
        layout.addWidget(analyzeButton)

        # Jaccard benzerlik düğmesi
        jaccardButton = QPushButton('Jaccard Benzerlik', self)
        jaccardButton.clicked.connect(self.calculateJaccardSimilarity)
        layout.addWidget(jaccardButton)

        # Arama bölümü
        self.searchBox = QLineEdit(self)
        self.searchBox.setPlaceholderText('Arama terimini girin')
        layout.addWidget(self.searchBox)

        searchButton = QPushButton('Ara', self)
        searchButton.clicked.connect(self.searchText)
        layout.addWidget(searchButton)

        # Sonuçları görüntüleme alanı
        self.resultLabel = QLabel('Sonuçlar:', self)
        layout.addWidget(self.resultLabel)

        self.resultsEdit = QTextEdit(self)
        self.resultsEdit.setReadOnly(True)
        layout.addWidget(self.resultsEdit)

        # Layout'u ana widget'e ata ve merkezi widget olarak ayarla
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def loadText(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Metin Dosyalarını Aç", "", "Text Files (*.txt);;All Files (*)", options=options)
        if files:
            combinedText = ""
            for fileName in files:
                with open(fileName, 'r', encoding='utf-8') as file:
                    combinedText += file.read() + "\n\n"
            self.textEdit.setText(combinedText)

    def loadText2(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Metin Dosyalarını Aç", "", "Text Files (*.txt);;All Files (*)", options=options)
        if files:
            combinedText = ""
            for fileName in files:
                with open(fileName, 'r', encoding='utf-8') as file:
                    combinedText += file.read() + "\n\n"
            self.textEdit2.setText(combinedText)

    def saveTextToDB(self):
        name, ok = QInputDialog.getText(self, 'Metin İsmi', 'Metin için bir isim girin:')
        if ok:
            existing_text = get_text_by_name(name)
            if existing_text:
                QMessageBox.warning(self, "Hata", "Aynı isimde bir metin zaten var.")
            else:
                content = self.textEdit.toPlainText()
                add_text_to_db(name, content)
                QMessageBox.information(self, "Başarılı", "Metin veritabanına kaydedildi.")

    def updateTextInDB(self):
        text_id, ok = QInputDialog.getInt(self, 'Metin ID', 'Güncellenecek metnin ID numarasını girin:')
        if ok:
            name, ok = QInputDialog.getText(self, 'Yeni Metin İsmi', 'Metin için yeni bir isim girin:')
            if ok:
                content = self.textEdit.toPlainText()
                update_text_in_db(text_id, name, content)
                QMessageBox.information(self, "Başarılı", "Metin güncellendi.")

    def deleteTextFromDB(self):
        text_id, ok = QInputDialog.getInt(self, 'Metin ID', 'Silinecek metnin ID numarasını girin:')
        if ok:
            delete_text_from_db(text_id)
            QMessageBox.information(self, "Başarılı", "Metin silindi.")

    def loadTextsFromDB(self):
        texts = get_all_texts()
        combinedText = ""
        for text in texts:
            combinedText += f'ID: {text[0]}, Name: {text[1]}\n{text[2]}\n\n'
        self.textEdit.setText(combinedText)

    def analyzeText(self):
        text1 = self.textEdit.toPlainText()
        text2 = self.textEdit2.toPlainText()
        
        # Metin 1 için analiz
        harf_sayisi1 = len(re.findall(r'\w', text1))
        kelime_sayisi1 = len(re.findall(r'\b\w+\b', text1))
        etkisiz_kelimeler1 = set([
            'bir', 've', 'ama', 'veya', 'gibi', 'şu', 'bu', 'o', 'şöyle', 'böyle'
        ])
        metin_kelimeler1 = re.findall(r'\b\w+\b', text1)
        etkisiz_kelime_sayisi1 = sum(1 for kelime in metin_kelimeler1 if kelime.lower() in etkisiz_kelimeler1)
        kelime_frekanslari1 = Counter(metin_kelimeler1)
        en_fazla_gecen_kelimeler1 = kelime_frekanslari1.most_common(5)
        en_az_gecen_kelimeler1 = kelime_frekanslari1.most_common()[:-6:-1]
        
        # Metin 2 için analiz
        harf_sayisi2 = len(re.findall(r'\w', text2))
        kelime_sayisi2 = len(re.findall(r'\b\w+\b', text2))
        etkisiz_kelimeler2 = set([
            'bir', 've', 'ama', 'veya', 'gibi', 'şu', 'bu', 'o', 'şöyle', 'böyle'
        ])
        metin_kelimeler2 = re.findall(r'\b\w+\b', text2)
        etkisiz_kelime_sayisi2 = sum(1 for kelime in metin_kelimeler2 if kelime.lower() in etkisiz_kelimeler2)
        kelime_frekanslari2 = Counter(metin_kelimeler2)
        en_fazla_gecen_kelimeler2 = kelime_frekanslari2.most_common(5)
        en_az_gecen_kelimeler2 = kelime_frekanslari2.most_common()[:-6:-1]
        
        # Sonuçların birleşmesi ve gösterilmesi
        results = (
            f'Metin 1 Analizi:\n'
            f'Harf Sayısı: {harf_sayisi1}\n'
            f'Kelime Sayısı: {kelime_sayisi1}\n'
            f'Etkisiz Kelime Sayısı: {etkisiz_kelime_sayisi1}\n'
            f'En Fazla Geçen 5 Kelime: {en_fazla_gecen_kelimeler1}\n'
            f'En Az Geçen 5 Kelime: {en_az_gecen_kelimeler1}\n\n'
            f'Metin 2 Analizi:\n'
            f'Harf Sayısı: {harf_sayisi2}\n'
            f'Kelime Sayısı: {kelime_sayisi2}\n'
            f'Etkisiz Kelime Sayısı: {etkisiz_kelime_sayisi2}\n'
            f'En Fazla Geçen 5 Kelime: {en_fazla_gecen_kelimeler2}\n'
            f'En Az Geçen 5 Kelime: {en_az_gecen_kelimeler2}'
        )
        
        self.resultsEdit.setText(results)


    def searchText(self):
        text = self.textEdit.toPlainText()
        searchTerm = self.searchBox.text()
        if searchTerm in text:
            self.resultsEdit.setText(f'"{searchTerm}" metin içinde bulundu.')
        else:
            self.resultsEdit.setText(f'"{searchTerm}" metin içinde bulunamadı.')

    def calculateJaccardSimilarity(self):
        metin1 = self.textEdit.toPlainText()
        metin2 = self.textEdit2.toPlainText()

        if not metin1 or not metin2:
            QMessageBox.warning(self, "Hata", "İki metni de girmelisiniz.")
            return

        benzerlik = jaccard_benzerlik(metin1, metin2)
        self.resultsEdit.setText(f'Jaccard Benzerlik: {benzerlik:.2f}')

def jaccard_benzerlik(metin1, metin2):
    kelimeler1 = set(metin1.split())
    kelimeler2 = set(metin2.split())

    ortak_kelimeler = kelimeler1.intersection(kelimeler2)
    tum_kelimeler = kelimeler1.union(kelimeler2)

    benzerlik = len(ortak_kelimeler) / len(tum_kelimeler)
    return benzerlik

def create_database():
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS texts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_text_to_db(name, content):
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('INSERT INTO texts (name, content) VALUES (?, ?)', (name, content))
    conn.commit()
    conn.close()

def update_text_in_db(text_id, name, content):
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('UPDATE texts SET name = ?, content = ? WHERE id = ?', (name, content, text_id))
    conn.commit()
    conn.close()

def delete_text_from_db(text_id):
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('DELETE FROM texts WHERE id = ?', (text_id,))
    conn.commit()
    conn.close()

def get_all_texts():
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM texts')
    rows = c.fetchall()
    conn.close()
    return rows

def get_text_by_name(name):
    conn = sqlite3.connect('texts.db')
    c = conn.cursor()
    c.execute('SELECT * FROM texts WHERE name = ?', (name,))
    text = c.fetchone()
    conn.close()
    return text


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
