from dataclasses import dataclass

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

class GPSLoader:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        points = []
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                row = line.strip().split(";")
                if len(row) != 9:
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
                        hdop=int(row[8])
                    )
                    points.append(point)
                except ValueError:
                    print(f"Błąd parsowania linii: {line}")
        return points
