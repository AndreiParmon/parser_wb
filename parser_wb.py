import requests
import pandas as pd

URL = "https://static-basket-01.wbbasket.ru/vol0/data/main-menu-ru-ru-v3.json"


def get_category():
    """
    Загружаем категории с Wildberries.

    return: словарь категорий.
    """

    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    # print(response.json())
    return response.json()


def parse(data, level=1):
    """
    Рекурсивно извлекаем все категории и подкатегории.

    return: список категорий с id, name, level и url.
    """

    categories = []

    def recurse(nodes, current_level):
        for node in nodes:
            categories.append({
                "id": node.get("id", "N/A"),
                "name": node.get("name", "N/A"),
                "level": current_level,
                "url": node.get("url", "")
            })
            if node.get("childs"):
                recurse(node["childs"], current_level + 1)

    recurse(data, level)
    return categories


def filter_worlds(categories, worlds):
    """
    Отбираем категории по ключевым словам.

    return: словарь с ключами-словами и отфильтрованными списками категорий.
    """

    result = {}
    for word in worlds:
        filtered = [c for c in categories if word.lower() in c["name"].lower()]
        result[word] = filtered
    return result


def save_to_excel(data_by_sheet, filename="wb_parser.xlsx"):
    """
    Сохраняем данные в Excel по листам, соответствующим ключам.
    """

    with pd.ExcelWriter(filename) as writer:
        for sheet_name, items in data_by_sheet.items():
            df = pd.DataFrame(items)
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def main():
    """
    - Загружаем категории
    - Формируем список категорий
    - Фильтруем по ключевым словам
    - Сохраняет в Excel
    """

    category = get_category()
    categories = parse(category)
    sheets = filter_worlds(categories, ["Обувь", "Детям", "Дом"])
    save_to_excel(sheets)

    print("Файл wb_parser.xlsx успешно создан!")


if __name__ == "__main__":
    main()

