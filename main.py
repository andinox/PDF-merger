from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtGui import QPixmap, QImage, QIcon
import fitz
from PyPDF2 import PdfMerger
import sys


class PDFMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Merger")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.MultiSelection)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)  # Activer la réorganisation
        self.layout.addWidget(self.list_widget)

        self.btn_open = QPushButton("Ouvrir PDF", self)
        self.btn_open.clicked.connect(self.openPDFs)
        self.layout.addWidget(self.btn_open)

        self.btn_combine = QPushButton("Combiner PDFs", self)
        self.btn_combine.clicked.connect(self.combinePDFs)
        self.layout.addWidget(self.btn_combine)

        self.file_names = []

    def initThumbnail(self, file_path):
        try:
            doc = fitz.open(file_path)
            first_page = doc.load_page(0)
            pixmap = first_page.get_pixmap()
            q_image = QPixmap.fromImage(QImage(pixmap.samples, pixmap.width, pixmap.height, pixmap.stride, QImage.Format_RGB888))
            return q_image
        except Exception as e:
            print("Error generating thumbnail:", e)
            return QPixmap()

    def openPDFs(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("PDF Files (*.pdf)")
        if file_dialog.exec_():
            new_files = file_dialog.selectedFiles()
            self.file_names.extend(new_files)
            self.updateListWidget()

    def combinePDFs(self):
        if self.file_names:
            merger = PdfMerger()
            for file_name in self.file_names:
                merger.append(file_name)
            output_file, _ = QFileDialog.getSaveFileName(self, "Sauvegarder PDF combiné", "", "PDF Files (*.pdf)")
            if output_file:
                with open(output_file, "wb") as fout:
                    merger.write(fout)
                QMessageBox.information(self, "Succès", "PDFs combinés avec succès!")
            else:
                QMessageBox.warning(self, "Attention", "Veuillez sélectionner un emplacement de sauvegarde.")
        else:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord sélectionner des fichiers PDF à combiner.")

    def updateListWidget(self):
        self.list_widget.clear()
        for file_name in self.file_names:
            widget = QWidget()
            layout = QVBoxLayout()

            pixmap = self.initThumbnail(file_name)
            label_image = QLabel()
            label_image.setPixmap(pixmap.scaledToWidth(150))
            label_image.setStyleSheet("border: 1px solid gray; border-radius: 10px; padding: 5px;")
            layout.addWidget(label_image)

            label_title = QLabel(file_name.split("/")[-1])
            label_title.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_title)

            widget.setLayout(layout)

            item = QListWidgetItem()
            item.setSizeHint(widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = PDFMergerApp()
    mainWindow.show()
    sys.exit(app.exec_())
