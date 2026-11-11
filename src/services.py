import json
import os

import requests

from src.interfaces import AircraftProvider
from src.utils import AircraftConverter


class APIAdapter(AircraftProvider):
    """Получает данные о самолётах из внешних API."""

    openstreetmap_url = 'https://nominatim.openstreetmap.org/search'
    opensky_url = 'https://opensky-network.org/api/states/all'

    def get_country_coordinates(self, country):
        """Получает географические границы страны через Nominatim."""
        headers = {
            'User-Agent': 'PlaneTracker/1.0'
        }

        params = {
            'country': country,
            'format': 'json',
            'limit': 1
        }

        try:
            response = requests.get(
                url=self.openstreetmap_url,
                params=params,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            if not data:
                return None

            return data[0].get('boundingbox')

        except requests.RequestException:
            raise
        except (ValueError, KeyError, IndexError):
            raise ValueError('Не удалось получить координаты страны.')

    def get_aircraft_states(self, boundingbox):
        """Получает данные о самолётах через OpenSky."""
        if not boundingbox or len(boundingbox) != 4:
            raise ValueError('Некорректные географические границы.')

        params = {
            'lamin': boundingbox[0],
            'lamax': boundingbox[1],
            'lomin': boundingbox[2],
            'lomax': boundingbox[3]
        }

        response = requests.get(
            url=self.opensky_url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError('Некорректный ответ OpenSky.')

        return data.get('states') or []

    def get_aircraft(self, country):
        """Получает и преобразует данные о самолётах."""
        if not country or not country.strip():
            raise ValueError('Название страны не может быть пустым.')

        boundingbox = self.get_country_coordinates(country)

        if not boundingbox:
            return []

        aircraft_data = self.get_aircraft_states(boundingbox)

        converter = AircraftConverter()
        return converter.convert(aircraft_data)


class JSONSaver:
    """Сохраняет данные о самолётах в JSON."""

    def __init__(self, filename='data/aircraft.json'):
        self.filename = filename

        # Создаём папку для файла, если её ещё нет
        directory = os.path.dirname(filename)

        if directory:
            os.makedirs(directory, exist_ok=True)

    def add_aeroplane(self, aircraft):
        """Добавляет самолёт в JSON-файл."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError('Формат JSON должен содержать список.')

        except FileNotFoundError:
            data = []

        except json.JSONDecodeError:
            raise ValueError('JSON-файл повреждён.')

        aircraft_data = {
            'callsign': aircraft.callsign,
            'country': aircraft.country,
            'speed': aircraft.speed,
            'altitude': aircraft.altitude
        }

        data.append(aircraft_data)

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def delete_aeroplane(self, callsign):
        """Удаляет самолёт по позывному."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError('Формат JSON должен содержать список.')

            updated_data = [
                aircraft for aircraft in data
                if aircraft.get('callsign') != callsign
            ]

            if len(data) == len(updated_data):
                return False

            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(updated_data, file, ensure_ascii=False, indent=4)

            return True

        except FileNotFoundError:
            return False

        except json.JSONDecodeError:
            raise ValueError('JSON-файл повреждён.')
