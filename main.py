from src.services import APIAdapter, JSONSaver


def print_aircraft(aircraft_list):
    """Выводит информацию о самолётах."""
    if not aircraft_list:
        print('Самолёты не найдены.')
        return

    for number, plane in enumerate(aircraft_list, start=1):
        print(f'\nСамолёт №{number}')
        print(f'Позывной: {plane.callsign or "Неизвестен"}')
        print(f'Страна: {plane.country}')
        print(
            f'Скорость: {plane.speed if plane.speed is not None else "Неизвестна"} м/с'
        )
        print(
            f'Высота: {plane.altitude if plane.altitude is not None else "Неизвестна"} м'
        )
        print('-' * 30)


def filter_by_country(aircraft_list):
    """Фильтрует самолёты по стране происхождения."""
    country = input('Введите страну самолёта: ').strip()

    return [
        plane for plane in aircraft_list
        if plane.country.lower() == country.lower()
    ]


def filter_by_altitude(aircraft_list):
    """Фильтрует самолёты по диапазону высоты."""
    try:
        min_altitude = float(input('Минимальная высота (м): '))
        max_altitude = float(input('Максимальная высота (м): '))
    except ValueError:
        print('Ошибка! Введите числовые значения.')
        return aircraft_list

    if min_altitude < 0 or min_altitude > max_altitude:
        print('Некорректный диапазон высоты.')
        return aircraft_list

    return [
        plane for plane in aircraft_list
        if plane.altitude is not None
        and min_altitude <= plane.altitude <= max_altitude
    ]


def sort_aircraft(aircraft_list):
    """Сортирует самолёты по скорости или высоте по убыванию."""
    print('\nСортировка:')
    print('1. По скорости')
    print('2. По высоте')

    choice = input('Выберите вариант: ')

    if choice == '1':
        attribute = 'speed'
    elif choice == '2':
        attribute = 'altitude'
    else:
        print('Неверный выбор.')
        return aircraft_list

    return sorted(
        aircraft_list,
        key=lambda plane: (
            getattr(plane, attribute) is None,
            -(getattr(plane, attribute) or 0)
        )
    )


def show_top_aircraft(aircraft_list):
    """Показывает N самых быстрых самолётов."""
    try:
        amount = int(input('Сколько самолётов показать? '))
        if amount <= 0:
            print('Количество должно быть больше нуля.')
            return
    except ValueError:
        print('Введите целое число.')
        return

    sorted_aircraft = sorted(
        aircraft_list,
        key=lambda plane: (
            plane.speed is None,
            -(plane.speed or 0)
        )
    )

    print_aircraft(sorted_aircraft[:amount])


def save_aircraft(aircraft_list, saver):
    """Сохраняет найденные самолёты в JSON."""
    if not aircraft_list:
        print('Нет самолётов для сохранения.')
        return

    for plane in aircraft_list:
        saver.add_aeroplane(plane)

    print(f'Сохранено самолётов: {len(aircraft_list)}')


def delete_aircraft(saver):
    """Удаляет самолёт из JSON по позывному."""
    callsign = input('Введите позывной самолёта: ').strip()

    if not callsign:
        print('Позывной не может быть пустым.')
        return

    if saver.delete_aeroplane(callsign):
        print('Самолёт успешно удалён.')
    else:
        print('Самолёт не найден.')


def main():
    api = APIAdapter()
    saver = JSONSaver()

    country = input('Введите страну для поиска самолётов: ').strip()

    if not country:
        print('Название страны не может быть пустым.')
        return

    try:
        aircraft_list = api.get_aircraft(country)
    except Exception as error:
        print(f'Ошибка при получении данных: {error}')
        return

    if not aircraft_list:
        print('Самолёты не найдены или страна не определена.')
        return

    print(f'\nНайдено самолётов: {len(aircraft_list)}')

    while True:
        print('\n--- МЕНЮ ---')
        print('1. Показать самолёты')
        print('2. Фильтр по стране')
        print('3. Фильтр по высоте')
        print('4. Сортировка по скорости или высоте')
        print('5. Показать Top N самых быстрых')
        print('6. Сохранить самолёты в JSON')
        print('7. Удалить самолёт из JSON')
        print('0. Выход')

        choice = input('Выберите действие: ')

        if choice == '1':
            print_aircraft(aircraft_list)

        elif choice == '2':
            filtered = filter_by_country(aircraft_list)
            print(f'Найдено: {len(filtered)}')
            print_aircraft(filtered)

        elif choice == '3':
            filtered = filter_by_altitude(aircraft_list)
            print(f'Найдено: {len(filtered)}')
            print_aircraft(filtered)

        elif choice == '4':
            aircraft_list = sort_aircraft(aircraft_list)
            print('Сортировка выполнена.')
            print_aircraft(aircraft_list)

        elif choice == '5':
            show_top_aircraft(aircraft_list)

        elif choice == '6':
            try:
                save_aircraft(aircraft_list, saver)
            except (OSError, ValueError) as error:
                print(f'Ошибка сохранения: {error}')

        elif choice == '7':
            try:
                delete_aircraft(saver)
            except (OSError, ValueError) as error:
                print(f'Ошибка удаления: {error}')

        elif choice == '0':
            print('Работа программы завершена.')
            break

        else:
            print('Неизвестная команда. Попробуйте ещё раз.')


if __name__ == '__main__':
    main()

