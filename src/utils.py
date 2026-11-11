from src.models import Aircraft

class AircraftConverter:

    def convert(self, aircraft_data):
        data_list = []
        for n in aircraft_data:
            data_dict = {
                'callsign': None,
                'country': None,
                'speed': None,
                'altitude': None
            }
            data_dict['callsign'] = n[1]
            data_dict['country'] = n[2]
            altitude = n[7]
            speed = n[9]

            data_dict['altitude'] = (
                altitude if altitude is not None and altitude >= 0 else None
            )
            data_dict['speed'] = (
                speed if speed is not None and speed >= 0 else None
            )

            aircraft_obj = Aircraft(**data_dict)
            data_list.append(aircraft_obj)

        return data_list






