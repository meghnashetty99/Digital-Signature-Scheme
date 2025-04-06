# gui.py
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QTextEdit, QLabel, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QClipboard
from ds_core import DigitalSignature  # Make sure your file is named ds_core.py

class SignatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Signature App 🔐")
        self.setGeometry(100, 100, 700, 500)

        self.ds = DigitalSignature()
        self.selected_file = ""

        # Message input
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("📝 Enter your message here...")

        # Signature output
        self.signature_output = QTextEdit()
        self.signature_output.setReadOnly(True)

        # Result label
        self.result_label = QLabel("")

        # Buttons
        self.generate_btn = QPushButton("🔑 Generate Keys")
        self.sign_btn = QPushButton("✍️ Sign Message")
        self.verify_btn = QPushButton("✅ Verify Signature")
        self.copy_sig_btn = QPushButton("📋 Copy Signature")
        self.save_sig_btn = QPushButton("💾 Save Signature to File")
        self.sign_file_btn = QPushButton("📁 Sign File")
        self.verify_file_btn = QPushButton("📂 Verify File")

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.message_input)

        layout.addWidget(self.generate_btn)
        layout.addWidget(self.sign_btn)

        layout.addWidget(QLabel("🔏 Signature Output:"))
        layout.addWidget(self.signature_output)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.copy_sig_btn)
        btn_row.addWidget(self.save_sig_btn)
        layout.addLayout(btn_row)

        layout.addWidget(self.verify_btn)
        layout.addWidget(self.result_label)

        layout.addWidget(QLabel("📄 File Options:"))
        layout.addWidget(self.sign_file_btn)
        layout.addWidget(self.verify_file_btn)

        self.setLayout(layout)

        # Connect signals
        self.generate_btn.clicked.connect(self.generate_keys)
        self.sign_btn.clicked.connect(self.sign_message)
        self.verify_btn.clicked.connect(self.verify_signature)
        self.copy_sig_btn.clicked.connect(self.copy_signature)
        self.save_sig_btn.clicked.connect(self.save_signature)
        self.sign_file_btn.clicked.connect(self.sign_file)
        self.verify_file_btn.clicked.connect(self.verify_file)

    def generate_keys(self):
        self.ds.generate_keys()
        QMessageBox.information(self, "Keys Generated", "✅ Keys saved in the 'keys/' folder.")

    def sign_message(self):
        try:
            self.ds.load_keys()
            msg = self.message_input.toPlainText()
            sig = self.ds.sign_message(msg)
            self.signature_output.setPlainText(sig.hex())
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def verify_signature(self):
        try:
            self.ds.load_keys()
            msg = self.message_input.toPlainText()
            sig_hex = self.signature_output.toPlainText()
            sig = bytes.fromhex(sig_hex)
            result = self.ds.verify_signature(msg, sig)
            self.result_label.setText(result)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def copy_signature(self):
        sig = self.signature_output.toPlainText()
        if sig:
            QApplication.clipboard().setText(sig)
            QMessageBox.information(self, "Copied", "✅ Signature copied to clipboard!")

    def save_signature(self):
        sig = self.signature_output.toPlainText()
        if sig:
            path, _ = QFileDialog.getSaveFileName(self, "Save Signature", "", "Signature Files (*.sig)")
            if path:
                with open(path, "w") as f:
                    f.write(sig)
                QMessageBox.information(self, "Saved", f"💾 Signature saved to:\n{path}")

    def sign_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Sign")
        if file_path:
            try:
                self.ds.load_keys()
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                sig = self.ds.sign_message(content)
                sig_path = file_path + ".sig"
                with open(sig_path, "w") as f:
                    f.write(sig.hex())
                QMessageBox.information(self, "File Signed", f"✅ Signature saved to:\n{sig_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def verify_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Verify")
        if not file_path:
            return

        sig_path, _ = QFileDialog.getOpenFileName(self, "Select Signature File")
        if not sig_path:
            return

        try:
            self.ds.load_keys()
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            with open(sig_path, "r") as f:
                sig_hex = f.read()
            sig = bytes.fromhex(sig_hex)
            result = self.ds.verify_signature(content, sig)
            QMessageBox.information(self, "Verification Result", result)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # DARK MODE 🔥
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI';
            font-size: 14px;
        }

        QPushButton {
            background-color: #1f1f1f;
            color: white;
            border: 1px solid #333;
            padding: 8px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #2c2c2c;
        }

        QTextEdit, QLabel {
            background-color: #1a1a1a;
            color: #eee;
            border: 1px solid #333;
            border-radius: 4px;
        }
    """
    app.setStyleSheet(dark_stylesheet)

    window = SignatureApp()
    window.show()
    sys.exit(app.exec_())
