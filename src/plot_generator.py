import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, points):
        self.points = points

    def plot_speed(self):
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
        satelite_data = [p.satellites for p in self.points]
        x = list(range(1, len(satelite_data) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(x, satelite_data, linestyle='-', color='green')
        plt.title("Wykres ilości satelit")
        plt.xlabel("Numer punktu")
        plt.ylabel("Ilość satelit")
        plt.grid(True)
        plt.show()