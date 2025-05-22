import requests
from math import radians, sin, cos, sqrt, atan2

class RoadInfoService:
    """
    Serwis do pobierania i przetwarzania informacji o drogach i limitach prędkości.
    Korzysta z Overpass API do pozyskania danych o drogach.
    """
    
    def __init__(self):
        """Inicjalizacja serwisu informacji o drogach."""
        self.speed_limits_cache = {}  # Cache na limity prędkości, żeby ograniczyć liczbę zapytań do API

    def get_route_speed_limits(self, points):
        """
        Pobiera limity prędkości dla całej trasy za jednym razem z Overpass API.

        :param points: Lista punktów GPS
        :type points: list
        :return: Słownik segmentów dróg i ich limitów prędkości oraz typy dróg
        :rtype: dict
        """
        if not points or len(points) < 2:
            return {}
            
        min_lat = min(p.latitude for p in points)
        max_lat = max(p.latitude for p in points)
        min_lon = min(p.longitude for p in points)
        max_lon = max(p.longitude for p in points)
        
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
        out geom;
        """
        
        road_segments = {}
        
        try:
            print("Pobieranie danych o drogach...")
            response = requests.get(overpass_url, params={"data": overpass_query}, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                print(f"Pobrano dane o {len(data.get('elements', []))} drogach")
                
                for road in data.get("elements", []):
                    tags = road.get("tags", {})
                    road_type = tags.get("highway", "unclassified")
                    
                    if "maxspeed" in tags:
                        try:
                            speed_limit = int(tags["maxspeed"].split()[0])
                        except (ValueError, IndexError):
                            # domyślny limit na podstawie typu drogi
                            speed_limit = self._get_default_speed_limit(road_type)
                    else:
                        speed_limit = self._get_default_speed_limit(road_type)
                            
                    # Wszystkie segmenty drogi
                    coords = road.get("geometry", [])
                    for i in range(len(coords) - 1):
                        start = (coords[i]["lat"], coords[i]["lon"])
                        end = (coords[i+1]["lat"], coords[i+1]["lon"])
                        segment = (start, end)
                        road_segments[segment] = (speed_limit, road_type)
                
                print(f"Znaleziono {len(road_segments)} segmentów dróg")
                road_types = {}
                for segment, (limit, road_type) in list(road_segments.items())[:10]:
                    if road_type not in road_types:
                        road_types[road_type] = limit
                print(f"Przykładowe typy dróg i limity: {road_types}")
            else:
                print(f"Błąd API: {response.status_code}")
                
        except Exception as e:
            print(f"Błąd podczas pobierania danych o drogach: {e}")
        
        return road_segments

    def _get_default_speed_limit(self, road_type):
        """
        Zwraca domyślny limit prędkości dla danego typu drogi w Polsce.
        
        :param road_type: Typ drogi z OSM
        :type road_type: str
        :return: Domyślny limit prędkości w km/h
        :rtype: int
        """
        limits = {
            'motorway': 140,
            'trunk': 120,
            'primary': 90,
            'secondary': 90,
            'tertiary': 90,
            'residential': 50,
            'service': 30,
            'living_street': 20,
            'motorway_link': 80,
            'trunk_link': 80,
            'primary_link': 70,
            'secondary_link': 70,
            'tertiary_link': 70,
        }
        return limits.get(road_type, 50)  # 50 km/h domyślny limit

    def find_nearest_road_segment(self, lat, lon, road_segments):
        """
        Znajduje najbliższy segment drogi dla danego punktu.

        :param lat: Szerokość geograficzna punktu
        :type lat: float
        :param lon: Długość geograficzna punktu
        :type lon: float
        :param road_segments: Słownik segmentów dróg i ich danych
        :type road_segments: dict
        :return: Najbliższy segment, jego limit prędkości i typ drogi
        :rtype: tuple
        """
        if not road_segments:
            return None, 50, "unknown"
            
        min_distance = float('inf')
        nearest_segment = None
        
        for segment, (speed_limit, road_type) in road_segments.items():
            # Oblicz odległość punktu od segmentu drogi
            distance = self.point_to_segment_distance_improved(lat, lon, *segment[0], *segment[1])
            
            if distance < min_distance:
                min_distance = distance
                nearest_segment = (segment, speed_limit, road_type)

        # Jeśli punkt jest dalej niż 50m od najbliższej drogi, użyj domyślnego limitu prędkości
        if min_distance > 0.05:  
            return None, 50, "unknown"
            
        return nearest_segment

    def point_to_segment_distance_improved(self, px, py, x1, y1, x2, y2):
        """
        Oblicza dokładną odległość punktu od odcinka drogi.

        :return: Odległość w kilometrach
        :rtype: float
        """
        # długość segmentu
        segment_length = self.haversine_distance(x1, y1, x2, y2)
        
        # Jeśli segment jest praktycznie punktem, zwróć odległość do tego punktu
        if segment_length < 0.00001:
            return self.haversine_distance(px, py, x1, y1)
        
        # minimum odległości do punktów początkowego i końcowego
        return min(
            self.haversine_distance(px, py, x1, y1),
            self.haversine_distance(px, py, x2, y2)
        )
        
    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """
        Oblicza odległość między dwoma punktami geograficznymi w kilometrach.

        :param lat1: Szerokość geograficzna pierwszego punktu
        :type lat1: float
        :param lon1: Długość geograficzna pierwszego punktu
        :type lon1: float
        :param lat2: Szerokość geograficzna drugiego punktu
        :type lat2: float
        :param lon2: Długość geograficzna drugiego punktu
        :type lon2: float
        :return: Odległość w kilometrach
        :rtype: float
        """
        # Promień Ziemi w km
        R = 6371.0
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
        
    def get_speed_limit_at_point(self, latitude, longitude, search_radius=0.002):
        """
        Pobiera limit prędkości obowiązujący w konkretnym punkcie GPS.

        :param latitude: Szerokość geograficzna punktu
        :type latitude: float
        :param longitude: Długość geograficzna punktu
        :type longitude: float
        :param search_radius: Promień poszukiwania dróg wokół punktu (w stopniach), domyślnie 200m
        :type search_radius: float
        :return: Limit prędkości w km/h, typ drogi
        :rtype: tuple[int, str]
        """
        # Sprawdź w cache czy mamy już informacje o tym punkcie
        cache_key = f"{latitude:.5f},{longitude:.5f}"
        if cache_key in self.speed_limits_cache:
            return self.speed_limits_cache[cache_key]
        
        # Definiuj obszar poszukiwań
        min_lat = latitude - search_radius
        max_lat = latitude + search_radius
        min_lon = longitude - search_radius
        max_lon = longitude + search_radius
        
        # Zapytanie Overpass API o drogi w pobliżu punktu
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        way["highway"]({min_lat},{min_lon},{max_lat},{max_lon});
        out geom;
        """
        
        try:
            print(f"Pobieranie informacji o drodze dla punktu: {latitude}, {longitude}")
            response = requests.get(overpass_url, params={"data": overpass_query}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                road_segments = {}
                
                for road in data.get("elements", []):
                    tags = road.get("tags", {})
                    road_type = tags.get("highway", "unclassified")
                    
                    if "maxspeed" in tags:
                        try:
                            speed_limit = int(tags["maxspeed"].split()[0])
                        except (ValueError, IndexError):
                            speed_limit = self._get_default_speed_limit(road_type)
                    else:
                        speed_limit = self._get_default_speed_limit(road_type)
                            
                    # Wszystkie segmenty drogi
                    coords = road.get("geometry", [])
                    for i in range(len(coords) - 1):
                        start = (coords[i]["lat"], coords[i]["lon"])
                        end = (coords[i+1]["lat"], coords[i+1]["lon"])
                        segment = (start, end)
                        road_segments[segment] = (speed_limit, road_type)
                
                # Znajdź najbliższy segment drogi
                _, speed_limit, road_type = self.find_nearest_road_segment(
                    latitude, longitude, road_segments
                )
                
                # Zapisz w cache
                self.speed_limits_cache[cache_key] = (speed_limit, road_type)
                
                print(f"Znaleziony limit prędkości: {speed_limit} km/h (typ drogi: {road_type})")
                return speed_limit, road_type
                
            else:
                print(f"Błąd API: {response.status_code}")
                return 50, "unknown"  # Domyślny limit
                    
        except Exception as e:
            print(f"Błąd podczas pobierania informacji o drodze: {e}")
            return 50, "unknown"  # Domyślny limit