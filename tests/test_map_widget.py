import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock dla PyQtWebEngine
sys.modules['PyQt5.QtWebEngineWidgets'] = MagicMock()
sys.modules['PyQt5.QtWebEngineWidgets.QWebEngineView'] = MagicMock()

from map_widget import MapWidget

class TestMapWidget(unittest.TestCase):
    
    @patch('map_widget.RoadInfoService')
    def setUp(self, mock_road_service):
        self.map_widget = MapWidget()
        self.mock_road_service = mock_road_service
    
    def test_map_initialization(self):
        """Test czy mapa jest poprawnie inicjalizowana"""
        self.assertIsNotNone(self.map_widget)

if __name__ == '__main__':
    unittest.main()