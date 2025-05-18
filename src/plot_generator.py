import matplotlib.pyplot as plt


class Plotter:
    """
    Generuje różne wykresy na podstawie danych GPS z użyciem matplotlib.
    
    Ta klasa tworzy wizualizacje dla różnych metryk zebranych przez urządzenie GPS,
    takich jak prędkość, wysokość, dokładność (HDOP), liczba satelitów oraz napięcie baterii.
    """
    def __init__(self, points):
        """
        Inicjalizuje generator wykresów na podstawie punktów GPS.
        
        :param points: Lista obiektów GPSPoint do wizualizacji
        :type points: list
        """
        self.points = points

    def plot_speed(self):
        """
        Generuje i wyświetla wykres prędkości w czasie.
        
        Tworzy wykres pokazujący prędkość (km/h) dla każdego zarejestrowanego punktu.
        """
        speeds_data = [p.speed for p in self.points]
        x = list(range(1, len(speeds_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, speeds_data, linestyle='-', color='blue')
        plt.title("Wykres prędkości")
        plt.xlabel("Numer punktu")
        plt.ylabel("Prędkość (km/h)")
        plt.grid(True)
        plt.show()

    def plot_altitude(self):
        """
        Generuje i wyświetla wykres wysokości nad poziomem morza.
        
        Tworzy wykres pokazujący wysokość (m npm) dla każdego punktu.
        """
        altitudes_data = [p.altitude for p in self.points]
        x = list(range(1, len(altitudes_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, altitudes_data, linestyle='-', color='green')
        plt.title("Wykres wysokości mnpm")
        plt.xlabel("Numer punktu")
        plt.ylabel("Wysokość (m npm)")
        plt.grid(True)
        plt.show()

    def plot_hdop(self):
        """
        Generuje i wyświetla wykres dokładności HDOP.
        
        Tworzy wykres pokazujący wartość wskaźnika HDOP dla każdego punktu.
        """
        hdop_data = [p.hdop for p in self.points]
        x = list(range(1, len(hdop_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, hdop_data, linestyle='-', color='orange')
        plt.title("Wykres dokładności HDOP Horizontal Dilution of Precision")
        plt.xlabel("Numer punktu")
        plt.ylabel("Wartość wskaźnika HDOP")
        plt.grid(True)
        plt.show()

    def plot_voltage(self):
        """
        Generuje i wyświetla wykres napięcia baterii.
        
        Tworzy wykres pokazujący napięcie baterii (mV) dla każdego punktu.
        """
        voltage_data = [p.voltage for p in self.points]
        x = list(range(1, len(voltage_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, voltage_data, linestyle='-', color='red')
        plt.title("Wykres napięcia baterii")
        plt.xlabel("Numer punktu")
        plt.ylabel("Napięcie (mV)")
        plt.grid(True)
        plt.show()

    def plot_satelite(self):
        """
        Generuje i wyświetla wykres liczby satelitów.
        
        Tworzy wykres pokazujący liczbę połączonych satelitów dla każdego punktu.
        """
        satelite_data = [p.satellites for p in self.points]
        x = list(range(1, len(satelite_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, satelite_data, linestyle='-', color='green')
        plt.title("Wykres ilości satelit")
        plt.xlabel("Numer punktu")
        plt.ylabel("Ilość satelit")
        plt.grid(True)
        plt.show()