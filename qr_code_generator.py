import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QDoubleSpinBox, QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import qrcode
from PIL import Image
from io import BytesIO

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.qr_image = None  # To store the generated QR code image

    def initUI(self):
        self.setWindowTitle('QR Code Generator')
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        # Data input
        data_layout = QHBoxLayout()
        data_label = QLabel('Text or URL:')
        self.data_input = QLineEdit()
        data_layout.addWidget(data_label)
        data_layout.addWidget(self.data_input)
        layout.addLayout(data_layout)

        # Width input
        width_layout = QHBoxLayout()
        width_label = QLabel('Width (mm):')
        self.width_input = QDoubleSpinBox()
        self.width_input.setRange(10, 1000)
        self.width_input.setValue(60)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_input)
        layout.addLayout(width_layout)

        # Height input
        height_layout = QHBoxLayout()
        height_label = QLabel('Height (mm):')
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(10, 1000)
        self.height_input.setValue(60)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_input)
        layout.addLayout(height_layout)

        # Generate button
        self.generate_button = QPushButton('Generate QR Code')
        self.generate_button.clicked.connect(self.generate_qr_code)
        layout.addWidget(self.generate_button)

        # Save button
        self.save_button = QPushButton('Save QR Code')
        self.save_button.clicked.connect(self.save_qr_code)
        self.save_button.setEnabled(False)  # Disable until QR code is generated
        layout.addWidget(self.save_button)

        # QR Code display
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.qr_label)

        self.setLayout(layout)

    def generate_qr_code(self):
        data = self.data_input.text()
        width_mm = self.width_input.value()
        height_mm = self.height_input.value()

        self.qr_image = self.create_qr_code(data, width_mm, height_mm)
        qr_pixmap = QPixmap.fromImage(self.qr_image)
        self.qr_label.setPixmap(qr_pixmap)
        self.save_button.setEnabled(True)  # Enable save button

    def create_qr_code(self, data, width_mm, height_mm):
        width_inch = width_mm / 25.4
        height_inch = height_mm / 25.4
        dpi = 300
        width_px = int(width_inch * dpi)
        height_px = int(height_inch * dpi)
        
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=1, border=0)
        qr.add_data(data)
        qr.make(fit=True)

        base_size = min(width_px, height_px)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((base_size, base_size), Image.NEAREST)
        
        new_img = Image.new('RGB', (width_px, height_px), color='white')
        paste_x = (width_px - base_size) // 2
        paste_y = (height_px - base_size) // 2
        new_img.paste(img, (paste_x, paste_y))
        
        return QImage(new_img.tobytes("raw", "RGB"), new_img.width, new_img.height, QImage.Format.Format_RGB888)

    def save_qr_code(self):
        if self.qr_image is None:
            QMessageBox.warning(self, "Warning", "Please generate a QR code first.")
            return

        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("PNG Files (*.png);;BMP Files (*.bmp)")
        file_dialog.setDefaultSuffix("png")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            if file_path:
                if self.qr_image.save(file_path):
                    QMessageBox.information(self, "Success", f"QR code saved successfully to {file_path}")
                else:
                    QMessageBox.critical(self, "Error", "Failed to save the QR code.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QRCodeGenerator()
    ex.show()
    sys.exit(app.exec())