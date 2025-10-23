from html import unescape
from json import loads
from typing import Any

from bs4 import BeautifulSoup  # type: ignore

from pyzill.utils import remove_space, get_nested_value


def parse_body_home(body: bytes) -> dict[str, Any]:
    """
    Парсит HTML-контент для извлечения JSON-данных о доме
    
    Аргументы:
        body (bytes): HTML-контент веб-страницы
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Парсим тело HTML-страницы для извлечения общих компонентов
    componentProps = parse_body(body)
    # Получаем вложенные данные из кэша клиента через вспомогательную функцию
    data_raw = get_nested_value(componentProps, "gdpClientCache")
    # Преобразуем строку JSON в словарь
    property_json = loads(data_raw)
    # Инициализируем словарь для хранения распознанных данных
    parsed_data = {}
    # Проходим по всем значениям в JSON-объекте недвижимости
    for data in property_json.values():
        # Проверяем, содержит ли строковое представление данных ключевое слово "property"
        if "property" in str(data):
            # Извлекаем информацию о свойстве (недвижимости) из данных
            parsed_data = data.get("property")
    # Возвращаем распознанную информацию о недвижимости
    return parsed_data


def parse_body_deparments(body: bytes) -> dict[str, Any]:
    """
    Парсит HTML-контент для извлечения JSON-данных о департаменте (апартаментах)
    
    Аргументы:
        body (bytes): HTML-контент веб-страницы
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Парсим тело HTML-страницы для извлечения общих компонентов
    componentProps = parse_body(body)
    # Получаем вложенные данные из начального состояния Redux через вспомогательную функцию
    department_json = get_nested_value(componentProps, "initialReduxState.gdp")
    # Возвращаем JSON-данные департамента
    return department_json


def parse_body(body: bytes) -> dict[str, Any]:
    """
    Парсит HTML-контент для извлечения JSON-данных
    
    Аргументы:
        body (bytes): HTML-контент веб-страницы
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Создаем объект BeautifulSoup для парсинга HTML с помощью встроенной библиотеки html.parser
    soup = BeautifulSoup(body, "html.parser")
    # Ищем элемент с ID "__NEXT_DATA__" - это типичное место хранения JSON-данных в Next.js приложениях
    selection = soup.select_one("#__NEXT_DATA__")
    # Проверяем, найден ли элемент
    if selection:
        # Получаем текстовое содержимое найденного элемента
        htmlData = selection.getText()
        # Убираем лишние пробелы и декодируем HTML-сущности в строке данных
        htmlData = remove_space(unescape(htmlData))
        # Преобразуем строку JSON в словарь
        data = loads(htmlData)
        # Извлекаем вложенные данные из компонентов страницы с помощью вспомогательной функции
        return get_nested_value(data, "props.pageProps.componentProps")