from logging import exception


class Aircraft:
    callsign: str | None
    country: str
    speed: float | None
    altitude: float | None

    def __init__(self, callsign, country, speed, altitude):
        self.callsign = callsign
        self.country = country
        self.speed = speed
        self.altitude = altitude

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        if speed is not None and (
                not isinstance(speed, int | float)
                or isinstance(speed, bool)
        ):
            raise TypeError("Скорость должна быть числом или None")

        if speed is not None and speed < 0:
            raise ValueError("Скорость не может быть отрицательной!")

        self.__speed = speed

    @property
    def altitude(self):
        return self.__altitude

    @altitude.setter
    def altitude(self, altitude):
        if altitude is not None and (
                not isinstance(altitude, int | float)
                or isinstance(altitude, bool)
        ):
            raise TypeError("Высота должна быть числом или None")

        if altitude is not None and altitude < 0:
            raise ValueError("Высота не может быть отрицательной!")

        self.__altitude = altitude

    def compare_speed(self, other):
        if self.speed is not None and other.speed is not None:
            if self.speed > other.speed:
                return 'Первый самолет быстрее.'
            elif self.speed == other.speed:
                return 'Скорости равны.'
            else:
                return 'Второй самолет быстрее.'
        else:
            return 'Невозможно сравнить скорости.'

    def compare_altitude(self, other):
        if self.altitude is not None and other.altitude is not None:
            if self.altitude > other.altitude:
                return 'Первый самолет выше.'
            elif self.altitude == other.altitude:
                return 'У самолетов одинаковая высота.'
            else:
                return 'Второй самолет выше.'
        else:
            return 'Невозможно сравнить высоту.'



