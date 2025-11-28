"""Модуль кэширования данных о погоде на диск в JSON-файл.

Кэш имеет TTL (время жизни) — по умолчанию 1 час.
"""

import json
import os
from datetime import datetime, timedelta


class WeatherCache:
    """Кэш погоды с хранением на диске и автоматической очисткой устаревших записей."""

    def __init__(self, cache_file: str = 'weather_cache.json', ttl_hours: int = 1):
        """Инициализирует кэш.

        Args:
            cache_file (str): Путь к файлу кэша.
            ttl_hours (int): Время жизни записи в часах.
        """
        self.cache_file = cache_file
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_cache_file()

    def _ensure_cache_file(self):
        """Создаёт пустой файл кэша, если его нет."""
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False)

    def get(self, key: str):
        """Получает данные из кэша по ключу, если они не устарели.

        Returns:
            Any | None: Данные или None, если кэш пустой/просрочен.
        """
        # ... (код без изменений, только докстринг выше)
        try:
            if not os.path.exists(self.cache_file):
                return None

            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)

            if key not in cache:
                return None

            entry = cache[key]
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if datetime.now() - cached_time < self.ttl:
                return entry['data']
            else:
                self._remove_expired()
                return None

        except (json.JSONDecodeError, KeyError, ValueError, OSError) as e:
            print(f"Ошибка чтения кэша: {e}")
            return None

    def set(self, key: str, data):
        """Сохраняет данные в кэш с текущей меткой времени.

        Args:
            key (str): Ключ кэша.
            data (Any): Данные (должны быть JSON-serializable).
        """
        # ... код без изменений

    def _remove_expired(self):
        """Удаляет все просроченные записи из кэша."""
        # ... код без изменений