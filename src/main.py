import sys

from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QTextEdit, QListWidget
)
from PyQt5.QtCore import Qt



class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.load_map()

    def load_map(self):
        map_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        </head>
        <body style="margin:0">
            <div id="mapid" style="width: 100%; height: 100vh;"></div>
            <script>
                var map = L.map('mapid').setView([52.2298, 21.0122], 12);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '© OpenStreetMap contributors'
                }).addTo(map);
            </script>
        </body>
        </html>
        """
        self.setHtml(map_html)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Py Road")
        self.setGeometry(100, 100, 1200, 800)

        # mapa
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.map_widget = MapWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)
        central_widget.setLayout(layout)

        self.add_list_dock_widget("Lista punktów", ["Punkt 1", "Punkt 2", "Punkt 3", "Punkt 4"], "left")
        self.add_dock_widget("Dane GPS", "Pozycja: 52.2298 N, 21.0122 E", "bottom")
        self.add_table_dock_widget("Napięcie baterii", [["12v", "3a"]], ["Napiecie", "Amper"], "bottom")

    def add_list_dock_widget(self, title, pointslist, position):
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea
        )

        list = QListWidget()
        list.addItems(pointslist)
        dock.setWidget(list)
        self.addDockWidget(getattr(Qt, f"{position.capitalize()}DockWidgetArea"), dock)

    def add_dock_widget(self, title, default_text, position):
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea
        )

        text_edit = QTextEdit()
        text_edit.setText(default_text)
        text_edit.setReadOnly(True)
        dock.setWidget(text_edit)
        self.addDockWidget(getattr(Qt, f"{position.capitalize()}DockWidgetArea"), dock)

    def add_table_dock_widget(self, title, data, headers, position):
        dock = QDockWidget(title, self)
        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea
        )

        #tabela
        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(value))

        dock.setWidget(table)
        self.addDockWidget(getattr(Qt, f"{position.capitalize()}DockWidgetArea"), dock)


if __name__ == "__main__":
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
