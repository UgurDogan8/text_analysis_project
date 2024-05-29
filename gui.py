import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox
import re
from collections import Counter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Metin Analiz Arayüzü')

        # Ana widget ve layout
        centralWidget = QWidget()
        layout = QVBoxLayout()

        # Metin yükleme ve görüntüleme alanı
        self.textEdit = QTextEdit(self)
        layout.addWidget(self.textEdit)

        # Metin yükleme düğmesi
        loadButton = QPushButton('Metin Yükle', self)
        loadButton.clicked.connect(self.loadText)
        layout.addWidget(loadButton)

        # Analiz yapma düğmesi
        analyzeButton = QPushButton('Analiz Yap', self)
        analyzeButton.clicked.connect(self.analyzeText)
        layout.addWidget(analyzeButton)

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

    def analyzeText(self):
        text = self.textEdit.toPlainText()
        
        # Harf sayısı
        harf_sayisi = len(re.findall(r'\w', text))
        
        # Kelime sayısı
        kelime_sayisi = len(re.findall(r'\b\w+\b', text))
        
        # Etkisiz kelime sayısı (varsayılan bir etkisiz kelime listesi kullanıldı)
        etkisiz_kelimeler = set([
            'bir', 've', 'ama', 'veya', 'gibi', 'şu', 'bu', 'o', 'şöyle', 'böyle'
        ])
        metin_kelimeler = re.findall(r'\b\w+\b', text)
        etkisiz_kelime_sayisi = sum(1 for kelime in metin_kelimeler if kelime.lower() in etkisiz_kelimeler)
        
        # Kelime frekansları
        kelime_frekanslari = Counter(metin_kelimeler)
        en_fazla_gecen_kelimeler = kelime_frekanslari.most_common(5)
        en_az_gecen_kelimeler = kelime_frekanslari.most_common()[:-6:-1]
        
        # Sonuçları birleştir ve göster
        results = (
            f'Harf Sayısı: {harf_sayisi}\n'
            f'Kelime Sayısı: {kelime_sayisi}\n'
            f'Etkisiz Kelime Sayısı: {etkisiz_kelime_sayisi}\n'
            f'En Fazla Geçen 5 Kelime: {en_fazla_gecen_kelimeler}\n'
            f'En Az Geçen 5 Kelime: {en_az_gecen_kelimeler}'
        )
        
        self.resultsEdit.setText(results)

    def searchText(self):
        text = self.textEdit.toPlainText()
        searchTerm = self.searchBox.text()
        if searchTerm in text:
            self.resultsEdit.setText(f'"{searchTerm}" metin içinde bulundu.')
        else:
            self.resultsEdit.setText(f'"{searchTerm}" metin içinde bulunamadı.')

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
