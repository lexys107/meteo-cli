# tests/test_meteo.py
import unittest
from unittest.mock import patch, Mock
import sys
import os
import requests

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather.api import WeatherAPI, get_weather_description
from weather.parser import create_parser


class TestWeatherDescription(unittest.TestCase):
    def test_known_codes(self):
        self.assertEqual(get_weather_description(0), "Ясно")
        self.assertEqual(get_weather_description(3), "Пасмурно")
        self.assertEqual(get_weather_description(61), "Небольшой дождь")
        self.assertEqual(get_weather_description(95), "Гроза")

    def test_unknown_code(self):
        self.assertEqual(get_weather_description(999), "Неизвестно")


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.api = WeatherAPI()

    @patch('requests.get')
    def test_get_coordinates_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{
                "latitude": 55.7558,
                "longitude": 37.6173,
                "name": "Москва",
                "country": "Россия"
            }]
        }
        mock_get.return_value = mock_response

        result = self.api.get_coordinates("Москва")
        self.assertEqual(result['name'], "Москва")
        self.assertAlmostEqual(result['latitude'], 55.7558)

    @patch('requests.get')
    def test_get_coordinates_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        result = self.api.get_coordinates("НесуществующийГород123")
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_coordinates_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Нет интернета")

        with self.assertRaises(Exception) as context:
            self.api.get_coordinates("Москва")
        self.assertIn("Ошибка при получении координат", str(context.exception))

    def test_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            self.api.get_weather_by_coords(100, 200)


class TestArgumentParser(unittest.TestCase):
    def test_city_argument(self):
        parser = create_parser()
        args = parser.parse_args(['--city', 'Париж'])
        self.assertEqual(args.city, 'Париж')
        self.assertIsNone(args.coords)

    def test_coords_argument(self):
        parser = create_parser()
        args = parser.parse_args(['--coords', '55.7558', '37.6173'])
        self.assertEqual(args.coords, [55.7558, 37.6173])
        self.assertIsNone(args.city)

    def test_mutually_exclusive(self):
        parser = create_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(['--city', 'Москва', '--coords', '55', '37'])


if __name__ == '__main__':
    unittest.main(verbosity=2)