import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from plot_generator import Plotter
from file_leader import GPSPoint

class TestPlotter(unittest.TestCase):
    
    def setUp(self):
        # testowe punkty GPS
        self.test_points = [
            GPSPoint("10:30:45", "2023-06-15", 52.2297, 21.0122, 100.5, 270.0, 80.5, 7, 5, 3800),
            GPSPoint("10:31:00", "2023-06-15", 52.2298, 21.0123, 101.0, 270.0, 85.0, 8, 4, 3790)
        ]
        self.plotter = Plotter(self.test_points)
    
    # Sprawdź jak matplotlib jest importowany w plot_generator.py
    @patch('plot_generator.plt.figure', return_value=MagicMock())
    @patch('plot_generator.plt.show')
    def test_plot_speed(self, mock_show, mock_figure):
        """Test generowania wykresu prędkości"""
        self.plotter.plot_speed()
        mock_figure.assert_called()
        mock_show.assert_called()
    
    @patch('plot_generator.plt.figure', return_value=MagicMock())
    @patch('plot_generator.plt.show')
    def test_plot_altitude(self, mock_show, mock_figure):
        """Test generowania wykresu wysokości"""
        self.plotter.plot_altitude()
        mock_figure.assert_called()
        mock_show.assert_called()

if __name__ == '__main__':
    unittest.main()