
from src.models import Aircraft
from src.services import JSONSaver


def test_add_aircraft(tmp_path):
    file_path = tmp_path / 'aircraft.json'
    saver = JSONSaver(str(file_path))

    aircraft = Aircraft('AFL123', 'Russia', 850, 10500)
    saver.add_aeroplane(aircraft)

    import json
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    assert len(data) == 1
    assert data[0]['callsign'] == 'AFL123'
    assert data[0]['country'] == 'Russia'


def test_delete_aircraft(tmp_path):
    file_path = tmp_path / 'aircraft.json'
    saver = JSONSaver(str(file_path))

    aircraft = Aircraft('AFL123', 'Russia', 850, 10500)
    saver.add_aeroplane(aircraft)

    result = saver.delete_aeroplane('AFL123')

    assert result is True
    assert saver.delete_aeroplane('AFL123') is False


def test_delete_from_missing_file(tmp_path):
    file_path = tmp_path / 'missing.json'
    saver = JSONSaver(str(file_path))

    assert saver.delete_aeroplane('AFL123') is False
