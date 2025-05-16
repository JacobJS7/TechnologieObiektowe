import sys
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QTextEdit,
    QListWidget, QAction, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtWidgets
from map_widget import MapWidget
from file_leader import GPSLoader
from plot_generator import Plotter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Py Road")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_menu()
        self.statusBar().showMessage("Program gotowy")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.map_widget = MapWidget()
        self.map_widget.load_map()

        layout = QVBoxLayout()
        layout.addWidget(self.map_widget)
        central_widget.setLayout(layout)

        self.add_list_dock_widget(["Zaimportuj najpierw dane"])
        self.add_list_point_info(["Zaimportuj najpierw dane"])

    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Plik")
        import_action = QAction("Importuj", self)
        import_action.setObjectName("importAction")
        import_action.triggered.connect(self.import_data)
        export_action = QAction("Eksportuj", self)
        export_action.setObjectName("exportAction")
        export_action.triggered.connect(self.export_map)
        file_menu.addAction(import_action)
        file_menu.addAction(export_action)

        plot_menu = menubar.addMenu("Wykresy")
        speed_plot_action = QAction("Wykres prędkości", self)
        speed_plot_action.triggered.connect(self.show_speed_plot)

        altitude_plot_action = QAction("Wykres wysokości npm", self)
        altitude_plot_action.triggered.connect(self.show_altitude_plot)

        hdop_plot_action = QAction("Wykres dokładności HDOP", self)
        hdop_plot_action.triggered.connect(self.show_hdop_plot)

        satelite_count_action = QAction("Wykres ilości satelit", self)
        satelite_count_action.triggered.connect(self.show_satelite_plot)

        battery_voltage_action = QAction("Wykres napięcia baterii", self)
        battery_voltage_action.triggered.connect(self.show_voltage_plot)

        plot_menu.addAction(speed_plot_action)
        plot_menu.addAction(altitude_plot_action)
        plot_menu.addAction(hdop_plot_action)
        plot_menu.addAction(satelite_count_action)
        plot_menu.addAction(battery_voltage_action)

    def import_data(self):
        loader = GPSLoader()
        if loader.choose_file(self):
            self.points = loader.load_data()
            print(f"Wczytano {len(self.points)} punktów.")
            self.statusBar().showMessage("Zaimportowano wszystkie punkty")

            pointslist = [f"Punkt {i + 1}" for i in range(len(self.points))]
            if hasattr(self, "point_list_widget"):
                self.point_list_widget.clear()
                self.point_list_widget.addItems(pointslist)
            else:
                self.add_list_dock_widget(pointslist)
            self.map_widget.load_points(self.points)
            self.point_list_widget.itemClicked.connect(self.display_point_info)

    def add_list_dock_widget(self, pointslist):
        dock = QDockWidget("Lista punktów", self)
        self.point_list_widget = QListWidget()
        self.point_list_widget.addItems(pointslist)
        dock.setWidget(self.point_list_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def add_list_point_info(self, point_info):
        dock = QDockWidget("Szczegóły punktów", self)
        self.point_info_widget = QListWidget()
        self.point_info_widget.addItems(point_info)
        dock.setWidget(self.point_info_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def display_point_info(self, item):
        punkt_nazwa = item.text()
        print(f"Kliknięto: {punkt_nazwa}")
        itemindex = self.point_list_widget.row(item)

        if itemindex < 0 or itemindex >= len(self.points):
            print("Nieprawidłowy indeks punktu")
            return

        point = self.points[itemindex]

        self.point_info_widget.clear()
        self.point_info_widget.addItems([
            f"Czas: {point.time}",
            f"Data: {point.date}",
            f"Szerokość: {point.latitude}",
            f"Długość: {point.longitude}",
            f"Wysokość: {point.altitude} m npm",
            f"Kurs: {point.course}°",
            f"Prędkość: {point.speed} km/h",
            f"Liczba Połączonych Satelit: {point.satellites}",
            f"Wskaźnik HDOP: {point.hdop}",
            f"Napięcie baterii: {point.voltage} mV"
        ])

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

    def show_speed_plot(self):
        if not hasattr(self, 'points') or not self.points:
            return
        plotter = Plotter(self.points)
        plotter.plot_speed()

    def show_altitude_plot(self):
        if not hasattr(self, 'points') or not self.points:
            return
        plotter = Plotter(self.points)
        plotter.plot_altitude()

    def show_hdop_plot(self):
        if not hasattr(self, 'points') or not self.points:
            return
        plotter = Plotter(self.points)
        plotter.plot_hdop()

    def show_voltage_plot(self):
        if not hasattr(self, 'points') or not self.points:
            return
        plotter = Plotter(self.points)
        plotter.plot_voltage()

    def show_satelite_plot(self):
        if not hasattr(self, 'points') or not self.points:
            return
        plotter = Plotter(self.points)
        plotter.plot_satelite()

    def export_map(self):
        if not hasattr(self, 'points') or not self.points:
            self.statusBar().showMessage("Brak danych do eksportu. Najpierw zaimportuj dane.")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Eksportuj mapę", 
            "", 
            "Pliki HTML (*.html);;Wszystkie pliki (*)"
        )
        
        if file_name:
            try:
                # Pobierz aktualną zawartość HTML mapy
                self.map_widget.page().toHtml(lambda html_content: self._save_html_to_file(html_content, file_name))
                self.statusBar().showMessage(f"Mapa została wyeksportowana do: {file_name}")
            except Exception as e:
                self.statusBar().showMessage(f"Błąd podczas eksportowania mapy: {str(e)}")
                print(f"Błąd eksportu: {e}")
            
    def _save_html_to_file(self, html_content, file_name):
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Mapa została zapisana do pliku: {file_name}")
        except Exception as e:
            self.statusBar().showMessage(f"Błąd podczas zapisywania pliku: {str(e)}")
            print(f"Błąd zapisu: {e}")

if __name__ == "__main__":
    from PyQt5.QtCore import Qt

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
