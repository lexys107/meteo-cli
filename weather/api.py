"""Модуль для работы с API Open-Meteo.

Содержит класс WeatherAPI для получения координат и текущей погоды,
а также вспомогательную функцию преобразования кода погоды в текст.
"""

import requests
from .cache import WeatherCache


class WeatherAPI:
    """Клиент для работы с Open-Meteo API с поддержкой кэширования."""

    def __init__(self):
        """Инициализирует клиент API и объект кэша."""
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.cache = WeatherCache()

    def get_coordinates(self, city_name: str):
        """Получает географические координаты по названию города.

        Args:
            city_name (str): Название города (регистр не важен).

        Returns:
            dict | None: Словарь с ключами latitude, longitude, name, country
                         или None, если город не найден.

        Raises:
            Exception: При сетевых ошибках или проблемах с API.
        """
        cache_key = f"coords_{city_name.lower()}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            'name': city_name,
            'count': 1,
            'language': 'ru',
            'format': 'json'
        }

        try:
            response = requests.get(self.geocoding_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get('results'):
                result = data['results'][0]
                coords = {
                    'latitude': result['latitude'],
                    'longitude': result['longitude'],
                    'name': result['name'],
                    'country': result['country']
                }
                self.cache.set(cache_key, coords)
                return coords
            return None

        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении координат: {e}")

    def get_weather(self, latitude: float, longitude: float, city_name: str | None = None):
        """Получает текущую погоду по координатам.

        Args:
            latitude (float): Широта.
            longitude (float): Долгота.
            city_name (str | None): Название города для отображения (опционально).

        Returns:
            dict: Данные о погоде (temperature, windspeed, weathercode и др.).

        Raises:
            Exception: При сетевых ошибках или проблемах с API.
        """
        cache_key = f"weather_{latitude}_{longitude}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            return cached_data

        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': 'true',
            'timezone': 'auto',
            'forecast_days': 1
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            weather_data = {
                'temperature': data['current_weather']['temperature'],
                'windspeed': data['current_weather']['windspeed'],
                'winddirection': data['current_weather']['winddirection'],
                'weathercode': data['current_weather']['weathercode'],
                'time': data['current_weather']['time'],
                'city': city_name
            }

            self.cache.set(cache_key, weather_data)
            return weather_data

        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении погоды: {e}")

    def get_weather_by_city(self, city_name: str):
        """Получает погоду по названию города.

        Args:
            city_name (str): Название города.

        Returns:
            dict: Данные о погоде.

        Raises:
            Exception: Если город не найден или произошла ошибка API.
        """
        coords = self.get_coordinates(city_name)
        if not coords:
            raise Exception(f"Город '{city_name}' не найден")

        city_display_name = f"{coords['name']}, {coords['country']}"
        return self.get_weather(coords['latitude'], coords['longitude'], city_display_name)

    def get_weather_by_coords(self, latitude: float, longitude: float):
        """Получает погоду по прямым координатам с валидацией.

        Args:
            latitude (float): Широта от -90 до 90.
            longitude (float): Долгота от -180 до 180.

        Returns:
            dict: Данные о погоде.

        Raises:
            ValueError: Если координаты вне допустимого диапазона.
            Exception: При ошибках API.
        """
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Неверные координаты. Широта: -90..90, Долгота: -180..180")

        return self.get_weather(latitude, longitude)


def get_weather_description(weathercode: int) -> str:
    """Преобразует числовой код погоды Open-Meteo в человекочитаемое описание.

    Args:
        weathercode (int): Код погоды по классификации WMO.

    Returns:
        str: Описание погоды на русском языке или "Неизвестно".
    """
    weather_codes = {
        0: "Ясно", 1: "Преимущественно ясно", 2: "Переменная облачность", 3: "Пасмурно",
        45: "Туман", 48: "Туман с инеем",
        51: "Лёгкая морось", 53: "Умеренная морось", 55: "Сильная морось",
        56: "Лёгкая ледяная морось", 57: "Сильная ледяная морось",
        61: "Небольшой дождь", 63: "Умеренный дождь", 65: "Сильный дождь",
        66: "Лёдный дождь (слабый)", 67: "Лёдный дождь (сильный)",
        71: "Небольшой снег", 73: "Умеренный снег", 75: "Сильный снег",
        77: "Снежные зёрна",
        80: "Небольшие ливни", 81: "Умеренные ливни", 82: "Сильные ливни",
        85: "Небольшие снежные ливни", 86: "Сильные снежные ливни",
        95: "Гроза", 96: "Гроза с небольшим градом", 99: "Гроза с сильным градом"
    }
    return weather_codes.get(weathercode, "Неизвестно")