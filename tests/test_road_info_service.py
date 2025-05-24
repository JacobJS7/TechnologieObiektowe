import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Dodajemy ścieżkę do katalogu src, aby móc importować moduły
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from road_info_service import RoadInfoService

class TestRoadInfoService(unittest.TestCase):
    
    def setUp(self):
        self.service = RoadInfoService()
    
    def test_get_default_speed_limit(self):
        """Test czy domyślne limity są poprawnie zwracane"""
        self.assertEqual(self.service._get_default_speed_limit('motorway'), 140)
        self.assertEqual(self.service._get_default_speed_limit('residential'), 50)
        self.assertEqual(self.service._get_default_speed_limit('nonexistent'), 50)  # default
    
    def test_haversine_distance(self):
        """Test obliczania odległości między punktami"""
        # Warszawa -> Kraków, ~252km
        # https://en.wikipedia.org/wiki/Haversine_formula
        dist = self.service.haversine_distance(52.2297, 21.0122, 50.0647, 19.9450)
        self.assertAlmostEqual(dist, 252.0, delta=5.0)  # dopuszczamy błąd 5km
    
    @patch('requests.get')
    def test_get_route_speed_limits(self, mock_get):
        """Test pobierania limitów prędkości z mockowanym API"""
        # Mock odpowiedzi requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'elements': [
                {
                    'tags': {'highway': 'motorway', 'maxspeed': '140'},
                    'geometry': [
                        {'lat': 52.0, 'lon': 21.0},
                        {'lat': 52.1, 'lon': 21.1}
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Punkty testowe
        class MockPoint:
            def __init__(self, lat, lon):
                self.latitude = lat
                self.longitude = lon
        
        points = [MockPoint(52.0, 21.0), MockPoint(52.1, 21.1)]
        
        # Testuje metodę
        result = self.service.get_route_speed_limits(points)
        
        # Wyniki check
        self.assertEqual(len(result), 1)
        segment = ((52.0, 21.0), (52.1, 21.1))
        self.assertIn(segment, result)
        self.assertEqual(result[segment], (140, 'motorway'))

if __name__ == '__main__':
    unittest.main()