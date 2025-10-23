from typing import Any, List
from curl_cffi import requests
import json


def for_sale(
    pagination: int,
    search_value: str,
    min_beds: int,
    max_beds: int,
    min_bathrooms: int,
    max_bathrooms: int,
    min_price: int,
    max_price: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """
    Получает результаты поиска объектов недвижимости на продажу.
    Вы получите словарь с ключами mapResults и listResults. 
    Используйте mapResults, который содержит все объявления из всех страниц пагинации.
    listResults больше подходит для правой боковой панели, которую вы видите при поиске на Zillow.
    Обратите внимание, что максимальный размер mapResults составляет 500, 
    поэтому если вы получите результаты размером 500, и если вы хотите получить все результаты 
    из определенного района, вам нужно изменить масштаб или координаты.
    Даже если вы попытаетесь пройти через все страницы пагинации, это не сработает, 
    даже если вы используете mapResults или listResults.
    Я бы рекомендовал не использовать пагинацию, потому что у вас есть все результаты (максимум 500) в mapResults.
    
    Аргументы:
        pagination (int): номер страницы в пагинации
        search_value (str): поисковое значение
        min_beds (int): минимальное количество спален
        max_beds (int): максимальное количество спален
        min_bathrooms (int): минимальное количество ванных комнат
        max_bathrooms (int): максимальное количество ванных комнат
        min_price (int): минимальная цена
        max_price (int): максимальная цена
        ne_lat (float): северо-восточная широта
        ne_long (float): северо-восточная долгота
        sw_lat (float): юго-западная широта
        sw_long (float): юго-западная долгота
        zoom_value (int): значение масштаба
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.

    Возвращает:
        dict[str, Any]: список объектов недвижимости в формате JSON
    """
    # Настройка фильтров для поиска объектов на продажу
    filters = {
        # Установка сортировки по релевантности
        "sortSelection":  {"value": "globalrelevanceex"},
        # Включение всех типов домов
        "isAllHomes":  {"value": True},
    }
    # Вызов общей функции поиска с установленными фильтрами
    return search(pagination, search_value, min_beds, max_beds, min_bathrooms, max_bathrooms, min_price, max_price, ne_lat, ne_long, sw_lat, sw_long, zoom_value, filters, proxy_url)


def for_rent(
    pagination: int,
    search_value: str,
    is_entire_place: bool,
    is_room: bool,
    min_beds: int,
    max_beds: int,
    min_bathrooms: int,
    max_bathrooms: int,
    min_price: int,
    max_price: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """
    Получает результаты поиска аренды недвижимости.
    Вы получите словарь с ключами mapResults и listResults. 
    Используйте mapResults, который содержит все объявления из всех страниц пагинации.
    listResults больше подходит для правой боковой панели, которую вы видите при поиске на Zillow.
    Обратите внимание, что максимальный размер mapResults составляет 500, 
    поэтому если вы получите результаты размером 500, и если вы хотите получить все результаты 
    из определенного района, вам нужно изменить масштаб или координаты.
    Даже если вы попытаетесь пройти через все страницы пагинации, это не сработает, 
    даже если вы используете mapResults или listResults.
    Я бы рекомендовал не использовать пагинацию, потому что у вас есть все результаты (максимум 500) в mapResults.
    
    Аргументы:
        pagination (int): номер страницы в пагинации
        search_value (str): поисковое значение
        is_entire_place (bool): флаг, указывающий, искать ли целое жилье
        is_room (bool): флаг, указывающий, искать ли комнату
        min_beds (int): минимальное количество спален
        max_beds (int): максимальное количество спален
        min_bathrooms (int): минимальное количество ванных комнат
        max_bathrooms (int): максимальное количество ванных комнат
        min_price (int): минимальная цена
        max_price (int): максимальная цена
        ne_lat (float): северо-восточная широта
        ne_long (float): северо-восточная долгота
        sw_lat (float): юго-западная широта
        sw_long (float): юго-западная долгота
        zoom_value (int): значение масштаба
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.

    Возвращает:
        dict[str, Any]: список объектов недвижимости в формате JSON
    """
    # Настройка фильтров для поиска аренды
    filters = {
        # Установка сортировки по приоритету
        "sortSelection":  {"value": "priorityscore"},
        # Исключение новостроек
        "isNewConstruction":  {"value": False},
        # Исключение объектов на аренде
        "isForSaleForeclosure":  {"value": False},
        # Исключение продаж напрямую от владельца
        "isForSaleByOwner":  {"value": False},
        # Исключение продаж через агента
        "isForSaleByAgent":  {"value": False},
        # Включение аренды
        "isForRent":  {"value": True},
        # Исключение объектов "Скоро появится"
        "isComingSoon":  {"value": False},
        # Исключение аукционов
        "isAuction":  {"value": False},
        # Включение всех типов домов
        "isAllHomes":  {"value": True},
    }
    
    # Установка фильтра для поиска комнаты, если указано
    if is_room:
        filters["isRoomForRent"] = {"value": True}
    
    # Установка фильтра для исключения целого жилья, если указано
    if not is_entire_place:    
        filters["isEntirePlaceForRent"] = {"value": False}
        
    # Вызов общей функции поиска с установленными фильтрами
    return search(pagination, search_value, min_beds, max_beds, min_bathrooms, max_bathrooms, min_price, max_price, ne_lat, ne_long, sw_lat, sw_long, zoom_value, filters, proxy_url)


def sold(
    pagination: int,
    search_value: str,
    min_beds: int,
    max_beds: int,
    min_bathrooms: int,
    max_bathrooms: int,
    min_price: int,
    max_price: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """
    Получает результаты поиска проданных объектов недвижимости.
    Вы получите словарь с ключами mapResults и listResults. 
    Используйте mapResults, который содержит все объявления из всех страниц пагинации.
    listResults больше подходит для правой боковой панели, которую вы видите при поиске на Zillow.
    Обратите внимание, что максимальный размер mapResults составляет 500, 
    поэтому если вы получите результаты размером 500, и если вы хотите получить все результаты 
    из определенного района, вам нужно изменить масштаб или координаты.
    Даже если вы попытаетесь пройти через все страницы пагинации, это не сработает, 
    даже если вы используете mapResults или listResults.
    Я бы рекомендовал не использовать пагинацию, потому что у вас есть все результаты (максимум 500) в mapResults.
    
    Аргументы:
        pagination (int): номер страницы в пагинации
        search_value (str): поисковое значение
        min_beds (int): минимальное количество спален
        max_beds (int): максимальное количество спален
        min_bathrooms (int): минимальное количество ванных комнат
        max_bathrooms (int): максимальное количество ванных комнат
        min_price (int): минимальная цена
        max_price (int): максимальная цена
        ne_lat (float): северо-восточная широта
        ne_long (float): северо-восточная долгота
        sw_lat (float): юго-западная широта
        sw_long (float): юго-западная долгота
        zoom_value (int): значение масштаба
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.

    Возвращает:
        dict[str, Any]: список объектов недвижимости в формате JSON
    """
    # Настройка фильтров для поиска проданных объектов
    filters = {
        # Установка сортировки по релевантности
        "sortSelection":  {"value": "globalrelevanceex"},
        # Исключение новостроек
        "isNewConstruction":  {"value": False},
        # Исключение объектов на аренде
        "isForSaleForeclosure":  {"value": False},
        # Исключение продаж напрямую от владельца
        "isForSaleByOwner":  {"value": False},
        # Исключение продаж через агента
        "isForSaleByAgent":  {"value": False},
        # Исключение аренды
        "isForRent":  {"value": False},
        # Исключение объектов "Скоро появится"
        "isComingSoon":  {"value": False},
        # Исключение аукционов
        "isAuction":  {"value": False},
        # Включение всех типов домов
        "isAllHomes":  {"value": True},
        # Включение недавно проданных объектов
        "isRecentlySold":  {"value": True},
    }
    # Вызов общей функции поиска с установленными фильтрами для проданных объектов
    return search(pagination, search_value, min_beds, max_beds, min_bathrooms, max_bathrooms, min_price, max_price, ne_lat, ne_long, sw_lat, sw_long, zoom_value, filters, proxy_url)
    

def search(
    pagination: int,
    search_value: str,
    min_beds: int,
    max_beds: int,
    min_bathrooms: int,
    max_bathrooms: int,
    min_price: int,
    max_price: int,
    ne_lat: float,
    ne_long: float,
    sw_lat: float,
    sw_long: float,
    zoom_value: int,
    filter_state: dict[str, Any],
    proxy_url: str | None = None,
) -> dict[str, Any]:
    """
    Получает результаты поиска по заданному номеру страницы.
    
    Аргументы:
        pagination (int): номер страницы в пагинации
        search_value (str): поисковое значение
        min_beds (int): минимальное количество спален
        max_beds (int): максимальное количество спален
        min_bathrooms (int): минимальное количество ванных комнат
        max_bathrooms (int): максимальное количество ванных комнат
        min_price (int): минимальная цена
        max_price (int): максимальная цена
        ne_lat (float): северо-восточная широта
        ne_long (float): северо-восточная долгота
        sw_lat (float): юго-западная широта
        sw_long (float): юго-западная долгота
        zoom_value (int): значение масштаба
        filter_state (dict[str, Any]): входные данные для выполнения поиска
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.

    Возвращает:
        dict[str, Any]: список объектов недвижимости в формате JSON
    """
    # Установка заголовков для HTTP-запроса, имитирующих реальный браузер
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "origin": "https://www.zillow.com",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    
    # Подготовка данных запроса
    inputData = {
        # Состояние поискового запроса
        "searchQueryState": {
            # Отображение карты
            "isMapVisible": True,
            # Отображение списка
            "isListVisible": True,
            # Границы карты (координаты северо-востока и юго-запада)
            "mapBounds": {
                "north": ne_lat,  # северная граница (широта)
                "east": ne_long,  # восточная граница (долгота)
                "south": sw_lat,  # южная граница (широта)
                "west": sw_long,  # западная граница (долгота)
            },
            # Состояние фильтров, передаваемое из внешней функции
            "filterState": filter_state,
            # Уровень масштаба карты
            "mapZoom": zoom_value,
            # Информация о пагинации
            "pagination": {
                "currentPage": pagination,
            },
        },
        # Что включать в ответ
        "wants": {
            "cat1": ["listResults", "mapResults"],  # результаты списка и карты
            "cat2": ["total"],  # общая информация
        },
        # Идентификатор запроса
        "requestId": 10,
        # Флаг отладочного запроса
        "isDebugRequest": False,
    }
    
    # Если задан поисковый запрос, добавляем его в состояние
    if search_value is not None:
        inputData["searchQueryState"]["usersSearchTerm"] = search_value

    # Обработка фильтра по количеству спален
    if min_beds is not None or max_beds is not None:
        # Создание словаря для фильтра спален
        beds = {}
        # Установка минимального количества спален, если указано
        if min_beds is not None:
            beds["min"] = min_beds
        # Установка максимального количества спален, если указано
        if max_beds is not None:
            beds["max"] = max_beds
        # Добавление фильтра спален в состояние фильтров
        inputData["searchQueryState"]["filterState"]["beds"] = beds

    # Обработка фильтра по количеству ванных комнат
    if min_bathrooms is not None or max_bathrooms is not None:
        # Создание словаря для фильтра ванных комнат
        baths = {}
        # Установка минимального количества ванных комнат, если указано
        if min_bathrooms is not None:
            baths["min"] = min_bathrooms
        # Установка максимального количества ванных комнат, если указано
        if max_bathrooms is not None:
            baths["max"] = max_bathrooms
        # Добавление фильтра ванных комнат в состояние фильтров
        inputData["searchQueryState"]["filterState"]["baths"] = baths

    # Обработка фильтра по цене
    if min_price is not None or max_price is not None:
        # Создание словаря для фильтра цены
        price = {}
        # Установка минимальной цены, если указана
        if min_price is not None:
            price["min"] = min_price
        # Установка максимальной цены, если указана
        if max_price is not None:
            price["max"] = max_price
        # Добавление фильтра цены в состояние фильтров
        inputData["searchQueryState"]["filterState"]["price"] = price

    # Настройка прокси-сервера, если указан
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    
    # Выполнение HTTP-запроса к API Zillow
    response = requests.put(
        url="https://www.zillow.com/async-create-search-page-state",  # URL-адрес API для создания состояния поиска
        json=inputData,  # Данные запроса в формате JSON
        headers=headers,  # Заголовки запроса
        proxies=proxies,  # Прокси-сервер (если указан)
        impersonate="chrome124",  # Имитация браузера Chrome версии 124
    )
    
    # Преобразование ответа в формат JSON
    data = response.json()
    
    # Возврат результата поиска из ответа
    # Получаем результаты из ключа "cat1" -> "searchResults", 
    # возвращаем пустой словарь, если ключи отсутствуют
    return data.get("cat1", {}).get("searchResults", {})