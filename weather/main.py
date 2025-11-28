#!/usr/bin/env python3
"""
Консольное приложение для получения текущей погоды.

Использует Open-Meteo API с кэшированием результатов.
Запуск: python -m weather --city Москва
"""

from .parser import create_parser
from .commands import get_weather_command


def main():
    """Точка входа в приложение."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        result = get_weather_command(args)
        print(result)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()