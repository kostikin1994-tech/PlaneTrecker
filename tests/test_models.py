import pytest

from src.models import Aircraft

def test_aircraft_init():
    test_1 = Aircraft('AFL123', 'Russia', 850.5, 10500.0)

    assert test_1.callsign == 'AFL123'
    assert test_1.country == 'Russia'
    assert test_1.speed == 850.5
    assert test_1.altitude == 10500.0

def test_aircraft_negative_speed():
    with pytest.raises(ValueError):
        Aircraft(
            callsign='AFL123',
            country='Russia',
            speed=-100,
            altitude=10500.0
        )

def test_aircraft_negative_altitude():
    with pytest.raises(ValueError):
        Aircraft(
            callsign='AFL123',
            country='Russia',
            speed=100.4,
            altitude=-500
        )

def test_aircraft_none_values():
    aircraft = Aircraft(
        callsign='AFL123',
        country='Russia',
        speed=None,
        altitude=None
    )

    assert aircraft.speed is None
    assert aircraft.altitude is None

def test_compare_speed():
    aircraft1 = Aircraft('AFL123', 'Russia', 850, 10500)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 9000)

    result = aircraft1.compare_speed(aircraft2)

    assert result == 'Первый самолет быстрее.'

def test_compare_speed_equal():
    aircraft1 = Aircraft('AFL123', 'Russia', 700, 10500)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 9000)

    result = aircraft1.compare_speed(aircraft2)

    assert result == 'Скорости равны.'

def test_compare_speed_with_none():
    aircraft1 = Aircraft('AFL123', 'Russia', 800, 10500)
    aircraft2 = Aircraft('DLH456', 'Germany', None, 9000)

    result = aircraft1.compare_speed(aircraft2)

    assert result == 'Невозможно сравнить скорости.'


def test_aircraft_invalid_speed_type():
    with pytest.raises(TypeError):
        Aircraft('AFL123', 'Russia', 'fast', 10500)


def test_aircraft_invalid_altitude_type():
    with pytest.raises(TypeError):
        Aircraft('AFL123', 'Russia', 850, 'high')


def test_compare_speed_second_faster():
    aircraft1 = Aircraft('AFL123', 'Russia', 700, 10500)
    aircraft2 = Aircraft('DLH456', 'Germany', 850, 9000)

    assert aircraft1.compare_speed(aircraft2) == 'Второй самолет быстрее.'


def test_compare_speed_one_none():
    aircraft1 = Aircraft('AFL123', 'Russia', None, 10500)
    aircraft2 = Aircraft('DLH456', 'Germany', 850, 9000)

    assert aircraft1.compare_speed(aircraft2) == 'Невозможно сравнить скорости.'


def test_compare_altitude_first_higher():
    aircraft1 = Aircraft('AFL123', 'Russia', 850, 12000)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 9000)

    assert aircraft1.compare_altitude(aircraft2) == 'Первый самолет выше.'


def test_compare_altitude_second_higher():
    aircraft1 = Aircraft('AFL123', 'Russia', 850, 8000)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 12000)

    assert aircraft1.compare_altitude(aircraft2) == 'Второй самолет выше.'


def test_compare_altitude_equal():
    aircraft1 = Aircraft('AFL123', 'Russia', 850, 10000)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 10000)

    assert aircraft1.compare_altitude(aircraft2) == 'У самолетов одинаковая высота.'


def test_compare_altitude_none():
    aircraft1 = Aircraft('AFL123', 'Russia', 850, None)
    aircraft2 = Aircraft('DLH456', 'Germany', 700, 10000)

    assert aircraft1.compare_altitude(aircraft2) == 'Невозможно сравнить высоту.'

