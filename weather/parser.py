"""Модуль создания парсера аргументов командной строки."""

import argparse


def create_parser():
    """Создаёт и возвращает настроенный объект argparse.ArgumentParser.

    Returns:
        argparse.ArgumentParser: Парсер с взаимоисключающими --city/--coords
                                и дополнительным флагом --history.
    """
    parser = argparse.ArgumentParser(
        description='Получение текущей погоды через Open-Meteo API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры:
  py -m weather --city Москва
  py -m weather -c "Санкт-Петербург"
  py -m weather --coords 55.7558 37.6173
  py -m weather --history          ← новая команда!
        '''
    )

    # Взаимоисключающая группа: только один из этих двух аргументов
    group = parser.add_mutually_exclusive_group()
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

    # НОВАЯ КОМАНДА — ДОЛЖНА БЫТЬ ВНЕ ГРУППЫ!
    parser.add_argument(
        '--history',
        action='store_true',
        help='Показать историю последних запросов погоды'
    )

    return parser