
from src.utils import AircraftConverter


def test_convert_aircraft():
    aircraft_data = [
        [
            'a1b2c3', 'AFL123', 'Russia',
            1731321000, 1731321000,
            37.6173, 55.7558, 10500.0,
            False, 850.5, 180.0, 0.0,
            None, 10600.0, '1234', False, 0
        ],
        [
            'd4e5f6', 'DLH456', 'Germany',
            1731321100, 1731321100,
            13.4050, 52.5200, 9000.0,
            False, 780.2, 270.0, 1.0,
            None, 9100.0, '5678', False, 0
        ]
    ]

    converter = AircraftConverter()
    result = converter.convert(aircraft_data)

    assert len(result) == 2

    assert result[0].callsign == 'AFL123'
    assert result[0].country == 'Russia'
    assert result[0].altitude == 10500.0
    assert result[0].speed == 850.5

    assert result[1].callsign == 'DLH456'
    assert result[1].country == 'Germany'
    assert result[1].altitude == 9000.0
    assert result[1].speed == 780.2


def test_convert_empty_list():
    converter = AircraftConverter()
    result = converter.convert([])

    assert result == []
