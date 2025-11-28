"""Модуль создания парсера аргументов командной строки."""

import argparse


def create_parser():
    """Создаёт и возвращает настроенный объект argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: Парсер с двумя взаимоисключающими группами аргументов.
    """
    parser = argparse.ArgumentParser(
        description='Получение текущей погоды через Open-Meteo API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  python main.py --city Москва
  python main.py -c "Санкт-Петербург"
  python main.py --coords 55.7558 37.6173
        '''
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--city', '-c',
        type=str,
        help='Название города в кавычках, если содержит пробелы'
    )
    group.add_argument(
        '--coords',
        nargs=2,
        type=float,
        metavar=('LAT', 'LON'),
        help='Широта и долгота (например: 55.7558 37.6173)'
    )

    return parser