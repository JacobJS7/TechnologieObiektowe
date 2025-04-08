import sys
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QTextEdit,
    QListWidget, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtWidgets

from map_widget import MapWidget
from file_leader import GPSLoader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Py Road")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_menu()
        self.statusBar().showMessage("Program gotowy")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        map_widget = MapWidget()
        map_widget.load_map()

        layout = QVBoxLayout()
        layout.addWidget(map_widget)
        central_widget.setLayout(layout)

        self.add_list_dock_widget("Lista punktów", ["Punkt 1", "Punkt 2", "Punkt 3", "Punkt 4"], "left")
        self.add_dock_widget("Dane GPS", "Pozycja: 52.2298 N, 21.0122 E", "bottom")
        self.add_table_dock_widget("Napięcie baterii", [["12v", "3a"]], ["Napiecie", "Amper"], "bottom")

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        import_action = QAction("Importuj", self)
        import_action.setObjectName("importAction")
        import_action.triggered.connect(self.import_data)
        export_action = QAction("Eksportuj", self)
        export_action.setObjectName("exportAction")
        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        plot_menu = menubar.addMenu("Wykresy")
        speed_plot_action = QAction("Wykres prędkości", self)
        altitude_plot_action = QAction("Wykres wysokości npm", self)
        HDOP_plot_action = QAction("Wykres dokładności HDOP", self)
        satelite_count_action = QAction("Wykres ilości satelit", self)
        plot_menu.addAction(speed_plot_action)
        plot_menu.addAction(altitude_plot_action)
        plot_menu.addAction(HDOP_plot_action)
        plot_menu.addAction(satelite_count_action)

    def import_data(self):
        loader = GPSLoader()
        if loader.choose_file(self):
            points = loader.load_data()
            print(f"Wczytano {len(points)} punktów.")
            self.statusBar().showMessage("Zaimportowano wszystkie punkty")
                # Dodac waypointy do mapy tutaj
                # Dodac waypointy do mapy tutaj
            for point in points:
                print(f"Godzina: {point.time} Data: {point.date} Latitude: {point.latitude} Longitude: {point.longitude}")
                print(f"Prędkość: {point.speed} km/h | Kurs: {point.course}° | Satelity: {point.satellites} | HDOP: {point.hdop}")

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
