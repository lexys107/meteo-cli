"""Модуль обработки команд приложения."""

from weather.api import WeatherAPI, get_weather_description
from weather.database import save_request, get_history


def get_weather_command(args):
    """Выполняет команду получения погоды или выводит историю."""
    api = WeatherAPI()

    # --- Новая команда: история ---
    if getattr(args, 'history', False):
        history = get_history(10)
        if not history:
            return "История запросов пуста."
        lines = ["", "ИСТОРИЯ ПОГОДЫ (последние 10):", "=" * 60]
        for ts, city, temp, desc in history:
            date = ts.split("T")[0]
            time = ts.split("T")[1][:5]
            lines.append(f"{date} {time}  |  {city:<15}  |  {temp:>5}°C  |  {desc or '—'}")
        lines.append("=" * 60)
        return "\n".join(lines)

    # --- Обычный запрос погоды ---
    try:
        if args.city:
            weather_data = api.get_weather_by_city(args.city)
        else:
            latitude, longitude = args.coords
            weather_data = api.get_weather_by_coords(latitude, longitude)

        # Добавляем описание и сохраняем в БД
        weather_data['description'] = get_weather_description(weather_data['weathercode'])
        save_request(weather_data['city'], weather_data)

        return format_weather_output(weather_data)

    except Exception as e:
        return f"Ошибка: {e}"


def format_weather_output(weather_data: dict) -> str:
    """Форматирует данные о погоде в красивый вывод."""
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