from dataclasses import dataclass
from PyQt5.QtWidgets import QFileDialog


@dataclass
class GPSPoint:
    """
    Klasa danych reprezentująca pojedynczy punkt GPS.

    Zawiera wszystkie metryki zarejestrowane przez urządzenie GPS w danym punkcie.

    Atrybuty:
        time (str): Czas rejestracji punktu GPS
        date (str): Data rejestracji punktu GPS
        latitude (float): Współrzędna szerokości geograficznej
        longitude (float): Współrzędna długości geograficznej
        altitude (float): Wysokość nad poziomem morza w metrach
        course (float): Kierunek w stopniach
        speed (float): Prędkość w km/h
        satellites (int): Liczba połączonych satelitów
        hdop (int): Wskaźnik dokładności HDOP
        voltage (int): Napięcie baterii w mV
    """
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
    """
    Odpowiada za wczytywanie i parsowanie danych GPS z plików tekstowych.

    Ta klasa obsługuje wybór pliku przez okno dialogowe oraz konwertuje surowe dane tekstowe
    na obiekty GPSPoint.
    """

    def __init__(self):
        """Inicjalizuje GPSLoader bez wybranego pliku."""
        self.filename = None

    def choose_file(self, parent=None):
        """
        Otwiera okno dialogowe windowsa do wyboru pliku z danymi GPS.

        :param parent: Widget nadrzędny dla okna dialogowego (główne okno)
        :type parent: QWidget lub None

        :return: True jeśli wybrano plik, False w przeciwnym razie
        :rtype: bool
        """
        file_name, _ = QFileDialog.getOpenFileName(parent, "Wybierz plik GPS", "", "Pliki tekstowe (*.txt);;Wszystkie pliki (*)")
        if file_name:
            self.filename = file_name
            return True
        return False

    def load_data(self):
        """
        Wczytuje i parsuje dane GPS z wybranego pliku danych .

        :return: Lista obiektów GPSPoint zawierających sparsowane dane
        :rtype: list
        """
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
                        print(f"Błąd parsowania linii: {line}")
        except Exception as e:
            print(f"Błąd podczas otwierania pliku: {e}")

        return points
