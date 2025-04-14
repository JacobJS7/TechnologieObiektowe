from dataclasses import dataclass
from PyQt5.QtWidgets import QFileDialog


@dataclass
class GPSPoint:
    time: str
    date: str
    latitude: float
    longitude: float
    altitude: float
    course: float
    speed: float
    satellites: int
    hdop: int
    voltage: int


class GPSLoader:
    def __init__(self):
        self.filename = None

    def choose_file(self, parent=None):
        file_name, _ = QFileDialog.getOpenFileName(parent, "Wybierz plik GPS", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)")
        if file_name:
            self.filename = file_name
            return True
        return False

    def load_data(self):
        if not self.filename:
            print("Nie wybrano pliku.")
            return []

        points = []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                for line in file:
                    row = line.strip().split(";")
                    if len(row) != 10:
                        print(f"Niepoprawny format linii: {line}")
                        continue
                    try:
                        point = GPSPoint(
                            time=row[0],
                            date=row[1],
                            latitude=float(row[2]),
                            longitude=float(row[3]),
                            altitude=float(row[4]),
                            course=float(row[5]),
                            speed=float(row[6]),
                            satellites=int(row[7]),
                            hdop=int(row[8]),
                            voltage=int(row[9])
                        )
                        points.append(point)
                    except ValueError:
                        print(f"Blad parsowania linii: {line}")
        except Exception as e:
            print(f"Błąd podczas otwierania pliku: {e}")

        return points
