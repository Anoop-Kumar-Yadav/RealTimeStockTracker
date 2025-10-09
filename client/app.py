from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QCompleter
)
from PyQt5.QtCore import Qt

from utils import (
    get_all_companies,
    fetch_company_info,
    fetch_all_watchlist,
    add_to_watchlist_api,
    remove_from_watchlist_api,
    toggle_watchlist_status_api
)


class StockApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📈 Stock Watchlist Manager")
        self.setGeometry(200, 100, 1000, 650)
        self.setStyleSheet("""
            QMainWindow { background-color: #f3f5f9; }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #ffffff;
                padding: 10px;
                font-family: Consolas;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
        """)

        self.all_companies = []
        self.setup_ui()
        self.load_companies()
        self.load_watchlist()

    # ----------------- UI SETUP -----------------
    def setup_ui(self):
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(15)

        # ---- Search Section ----
        search_layout = QHBoxLayout()
        self.combo_companies = QComboBox()
        self.combo_companies.setEditable(True)
        self.combo_companies.setMinimumWidth(400)
        self.btn_fetch_info = QPushButton("Show Info")
        search_layout.addWidget(QLabel("🔍 Company:"))
        search_layout.addWidget(self.combo_companies)
        search_layout.addWidget(self.btn_fetch_info)
        main_layout.addLayout(search_layout)

        # ---- Company Info ----
        self.txt_company_info = QTextEdit()
        self.txt_company_info.setReadOnly(True)
        main_layout.addWidget(self.txt_company_info)

        # ---- Watchlist Controls ----
        button_layout = QHBoxLayout()
        self.btn_add_watchlist = QPushButton("➕ Add to Watchlist")
        self.btn_remove_watchlist = QPushButton("❌ Remove from Watchlist")
        button_layout.addWidget(self.btn_add_watchlist)
        button_layout.addWidget(self.btn_remove_watchlist)
        main_layout.addLayout(button_layout)

        # ---- Watchlist Label ----
        label = QLabel("📋 Watchlist")
        label.setStyleSheet("font-size: 18px; margin-top: 10px;")
        main_layout.addWidget(label)

        # ---- Watchlist Table ----
        self.table_watchlist = QTableWidget()
        self.table_watchlist.setColumnCount(4)
        self.table_watchlist.setHorizontalHeaderLabels(["Symbol", "Status", "Toggle", "Remove"])
        self.table_watchlist.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_watchlist.setAlternatingRowColors(True)
        self.table_watchlist.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f0f2f5;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
        """)
        main_layout.addWidget(self.table_watchlist)

        # ---- Set Central Widget ----
        self.setCentralWidget(container)

        # ---- Connect Buttons ----
        self.btn_fetch_info.clicked.connect(self.show_company_info)
        self.btn_add_watchlist.clicked.connect(self.add_to_watchlist)
        self.btn_remove_watchlist.clicked.connect(self.remove_from_watchlist)

    # ----------------- LOAD COMPANIES -----------------
    # ----------------- LOAD COMPANIES -----------------
    def load_companies(self):
        self.all_companies = get_all_companies()
        if not self.all_companies:
            QMessageBox.warning(self, "Error", "Failed to load company symbols.")
            return
    
        cleaned_companies = []
        for symbol, name in self.all_companies:
            clean_symbol = symbol.strip().upper()
            clean_name = name.split(" - ")[0].strip()
            cleaned_companies.append((clean_symbol, clean_name))
    
        # Sort by symbol
        cleaned_companies.sort(key=lambda x: x[0])
    
        self.combo_companies.clear()
    
        for symbol, name in cleaned_companies:
            display_text = f"{symbol} – {name}"
            self.combo_companies.addItem(display_text, userData=symbol)
    
        # Enable search completer
        completer = QCompleter([f"{s} – {n}" for s, n in cleaned_companies])
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.combo_companies.setCompleter(completer)
    
        # Save cleaned data for later reference
        self.all_companies = cleaned_companies
    
        # ---------------- UX IMPROVEMENTS ----------------
        self.combo_companies.setEditable(True)
        line_edit = self.combo_companies.lineEdit()
    
        # --- Clear only once on first edit ---
        self._first_edit = True
    
        def handle_first_edit():
            if self._first_edit:
                line_edit.clear()
                self._first_edit = False
    
        line_edit.textEdited.connect(handle_first_edit)
    
        # --- Show info automatically on Enter ---
        line_edit.returnPressed.connect(self.show_company_info)
    


    # ----------------- SHOW COMPANY INFO -----------------
    def show_company_info(self):
        current_text = self.combo_companies.currentText()
        if not current_text:
            QMessageBox.warning(self, "Select Company", "Please select a company first.")
            return
        # Use the actual symbol
        symbol = self.combo_companies.currentData()
        info = fetch_company_info(symbol)
        self.txt_company_info.setPlainText(info)
    # ----------------- ADD TO WATCHLIST -----------------
    # Example: Add to watchlist button
    def add_to_watchlist(self):
        symbol = self.combo_companies.currentData()  # <--- Use currentData() instead of currentText()
        if not symbol:
            QMessageBox.warning(self, "Select Company", "Please select a company first.")
            return

        success = add_to_watchlist_api(symbol)
        if success:
            QMessageBox.information(self, "Success", f"{symbol} added to watchlist.")
            self.load_watchlist()  # reload watchlist table
        else:
            QMessageBox.warning(self, "Error", f"Failed to add {symbol} to watchlist.")


    # ----------------- REMOVE FROM WATCHLIST -----------------
    def remove_from_watchlist(self):
        current_text = self.combo_companies.currentText()
        if not current_text:
            return
        symbol = current_text.split("(")[-1].strip(")")
        if remove_from_watchlist_api(symbol):
            QMessageBox.information(self, "Success", f"{symbol} removed from watchlist.")
            self.load_watchlist()
        else:
            QMessageBox.warning(self, "Error", "Failed to remove company.")

    # ----------------- LOAD WATCHLIST -----------------
    def load_watchlist(self):
        self.table_watchlist.setRowCount(0)
        watchlist = fetch_all_watchlist()
        for row, item in enumerate(watchlist):
            symbol = item["symbol"]
            status = "🟢 Active" if item["active"] else "⚪ Inactive"

            self.table_watchlist.insertRow(row)
            self.table_watchlist.setItem(row, 0, QTableWidgetItem(symbol))
            self.table_watchlist.setItem(row, 1, QTableWidgetItem(status))

            btn_toggle = QPushButton("Toggle")
            btn_remove = QPushButton("Remove")

            btn_toggle.setStyleSheet("background-color:#388E3C;")
            btn_remove.setStyleSheet("background-color:#D32F2F;")

            btn_toggle.clicked.connect(lambda _, s=symbol: self.toggle_status(s))
            btn_remove.clicked.connect(lambda _, s=symbol: self.remove_from_watchlist_direct(s))

            self.table_watchlist.setCellWidget(row, 2, btn_toggle)
            self.table_watchlist.setCellWidget(row, 3, btn_remove)

    # ----------------- TOGGLE WATCHLIST STATUS -----------------
    def toggle_status(self, symbol):
        if toggle_watchlist_status_api(symbol):
            QMessageBox.information(self, "Success", f"{symbol} status toggled.")
            self.load_watchlist()
        else:
            QMessageBox.warning(self, "Error", "Failed to toggle status.")

    # ----------------- REMOVE DIRECT -----------------
    def remove_from_watchlist_direct(self, symbol):
        if remove_from_watchlist_api(symbol):
            QMessageBox.information(self, "Success", f"{symbol} removed.")
            self.load_watchlist()
        else:
            QMessageBox.warning(self, "Error", "Failed to remove company.")


# ----------------- MAIN -----------------
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = StockApp()
    window.show()
    sys.exit(app.exec_())
