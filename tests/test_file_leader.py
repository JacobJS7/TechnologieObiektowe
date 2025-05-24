import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from file_leader import GPSLoader, GPSPoint

class TestGPSLoader(unittest.TestCase):
    
    def setUp(self):
        self.loader = GPSLoader()
    
    @patch('builtins.open', new_callable=mock_open, read_data="10:30:45;2023-06-15;52.2297;21.0122;100.5;270.0;80.5;7;5;3800")
    def test_load_data(self, mock_file):
        """Test wczytywania danych z pliku"""
        # Ustawiamy nazwę pliku
        self.loader.filename = "test_data.txt"
        
        # Wywołujemy metodę load_data
        points = self.loader.load_data()
        
        # Sprawdzamy czy dane zostały poprawnie wczytane
        self.assertEqual(len(points), 1)
        self.assertEqual(points[0].time, "10:30:45")
        self.assertEqual(points[0].date, "2023-06-15")
        self.assertEqual(points[0].latitude, 52.2297)
        self.assertEqual(points[0].longitude, 21.0122)
        self.assertEqual(points[0].altitude, 100.5)
        self.assertEqual(points[0].course, 270.0)
        self.assertEqual(points[0].speed, 80.5)
        self.assertEqual(points[0].satellites, 7)
        self.assertEqual(points[0].hdop, 5)
        self.assertEqual(points[0].voltage, 3800)
    
    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_choose_file(self, mock_dialog):
        """Test wyboru pliku"""
        # Mockujemy dialog wyboru pliku
        mock_dialog.return_value = ("test_file.txt", "")
        
        # Wywołujemy metodę choose_file
        result = self.loader.choose_file()
        
        # Sprawdzamy wyniki
        self.assertTrue(result)
        self.assertEqual(self.loader.filename, "test_file.txt")
        
        # Test gdy użytkownik anuluje wybór
        mock_dialog.return_value = ("", "")
        result = self.loader.choose_file()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()