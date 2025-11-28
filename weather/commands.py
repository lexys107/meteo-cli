"""Модуль обработки команд приложения.

Содержит функции для получения погоды и красивого форматирования вывода.
"""

from .api import WeatherAPI, get_weather_description


def get_weather_command(args):
    """Выполняет команду получения погоды по городу или координатам.

    Args:
        args: Объект argparse.Namespace с параметрами командной строки.

    Returns:
        str: Отформатированная строка с данными о погоде или сообщение об ошибке.
    """
    api = WeatherAPI()

    try:
        if args.city:
            weather_data = api.get_weather_by_city(args.city)
        else:
            latitude, longitude = args.coords
            weather_data = api.get_weather_by_coords(latitude, longitude)

        return format_weather_output(weather_data)

    except Exception as e:
        return f"Ошибка: {e}"


def format_weather_output(weather_data: dict) -> str:
    """Форматирует данные о погоде в красивый текстовый вывод.

    Args:
        weather_data (dict): Словарь с данными от API.

    Returns:
        str: Многострочная строка с рамкой и информацией о погоде.
    """
    city = weather_data.get('city', 'Неизвестно')
    temp = weather_data['temperature']
    wind_speed = weather_data['windspeed']
    wind_dir = weather_data['winddirection']
    code = weather_data['weathercode']
    time = weather_data['time']
    desc = get_weather_description(code)

    lines = [
        "=" * 50,
        f"ПОГОДА: {city}",
        "=" * 50,
        f"Температура: {temp}°C",
        f"Погода: {desc}",
        f"Скорость ветра: {wind_speed} км/ч",
        f"Направление ветра: {wind_dir}°",
        f"Время обновления: {time}",
        "=" * 50
    ]
    return "\n".join(lines)