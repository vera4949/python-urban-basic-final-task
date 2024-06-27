import csv
import sys

MIN_SMALL_HOUSE_FLOORS = 1
MAX_SMALL_HOUSE_FLOORS = 5
MIN_MEDIUM_HOUSE_FLOORS = 6
MAX_MEDIUM_HOUSE_FLOORS = 16

def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    houses_ = []
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for string in reader:
            new_dict = {
                "area_id": string["area_id"],
                "house_address": string["house_address"],
                "floor_count": int(string["floor_count"]),
                "heating_house_type": string["heating_house_type"],
                "heating_value": float(string["heating_value"]),
                "area_residential": float(string["area_residential"]),
                "population": int(string["population"]),
            }
            houses_.append(new_dict)

    return houses_

def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория в виде строки: "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        err = "Число этажей должно быть целым числом."
        raise TypeError(err)
    if floor_count <= 0:
        err = "Число этажей должно быть положительным."
        raise ValueError(err)

    if MIN_SMALL_HOUSE_FLOORS <= floor_count <= MAX_SMALL_HOUSE_FLOORS:
        result = "Малоэтажный"
    elif MIN_MEDIUM_HOUSE_FLOORS <= floor_count <= MAX_MEDIUM_HOUSE_FLOORS:
        result = "Среднеэтажный"
    else:
        result = "Многоэтажный"

    return result


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    classified_houses_ = []
    for house in houses:
        floors = house.get("floor_count")
        category = classify_house(floors)
        classified_houses_.append(category)

    return classified_houses_


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    counts_dict = {}
    for category in categories:
        if category in counts_dict:
            counts_dict[category] += 1
        else:
            counts_dict[category] = 1

    return counts_dict


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес с минимальным средним количеством кв.м. жилой площади на жильца.

    :param houses: Список словарей с данными о домах.
    :return: Адрес с минимальным средним количеством кв.м. жилой площади на жильца.
    """
    min_average_area = float("inf")
    address = ""
    for house in houses:
        average_area = house["area_residential"] / house["population"]
        if average_area < min_average_area:
            min_average_area = average_area
            address = house["house_address"]

    return address


if __name__ == "__main__":
    data = read_file("housing_data.csv")
    categories = get_count_house_categories(list(set(get_classify_houses(data))))
    address = min_area_residential(data)

    sys.stdout.write("Количество домов в каждой категории: \n")
    for name in categories:
        sys.stdout.write(f" Категория: {name}. Количество: {categories[name]}.\n")
    sys.stdout.write(
        "\nДом с минимальным средним количеством кв.м. жилой площади\
 на жильца располагается по адресу: \n",
    )
    sys.stdout.write(f" {address}")
