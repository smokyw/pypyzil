from typing import Any
from curl_cffi import requests
from pyzill.parse import parse_body_home, parse_body_deparments

# Заголовки HTTP-запросов для имитации браузера Chrome
headers = {
    # Типы контента, которые клиент может принять
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    # Язык, на котором клиент предпочитает получать ответы
    "Accept-Language": "en",
    # Запрет кеширования
    "Cache-Control": "no-cache",
    # Заголовок для управления кешированием (для HTTP/1.0)
    "Pragma": "no-cache",
    # Платформа браузера (Chromium/Chrome)
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    # Устройство не мобильное
    "Sec-Ch-Ua-Mobile": "?0",
    # Платформа операционной системы
    "Sec-Ch-Ua-Platform": '"Windows"',
    # Тип запрашиваемого ресурса (документ)
    "Sec-Fetch-Dest": "document",
    # Режим запроса (навигация)
    "Sec-Fetch-Mode": "navigate",
    # Откуда приходит запрос (никакой сторонний сайт)
    "Sec-Fetch-Site": "none",
    # Пользователь инициировал запрос
    "Sec-Fetch-User": "?1",
    # Автоматическое обновление небезопасных запросов до HTTPS
    "Upgrade-Insecure-Requests": "1",
    # Строка идентификации пользователя (браузер Chrome 130)
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

def get_from_home_id(
    property_id: int, proxy_url: str | None = None
) -> dict[str, Any]:
    """
    Извлекает данные о недвижимости на основе ID недвижимости с Zillow
    
    Аргументы:
        property_id (int): ID любой недвижимости с Zillow
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Формирование URL для получения деталей недвижимости по ID
    home_url = f"https://www.zillow.com/homedetails/any-title/{property_id}_zpid/"
    # Вызов функции получения данных по URL
    data = get_from_home_url(home_url, proxy_url)
    return data

def get_from_deparment_id(
    deparment_id: str, proxy_url: str | None = None
) -> dict[str, Any]:
    """
    Извлекает данные о недвижимости на основе ID департамента (апартаментов) с Zillow
    
    Аргументы:
        deparment_id (str): ID департамента (апартаментов) на Zillow
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Формирование URL для получения информации об апартаментах по ID
    home_url = f"https://www.zillow.com/apartments/texas/the-lennox/{deparment_id}"
    # Настройка прокси-сервера, если указан
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    # Выполнение GET-запроса к URL апартаментов с заголовками и имитацией браузера
    response = requests.get(url=home_url, headers=headers, proxies=proxies, impersonate="chrome124")
    # Парсинг содержимого ответа для получения информации об апартаментах
    data = parse_body_deparments(response.content)
    return data

def get_from_deparment_url(
    deparment_url: str, proxy_url: str | None = None
) -> dict[str, Any]:
    """
    Извлекает данные о недвижимости на основе URL департамента (апартаментов) с Zillow
    
    Аргументы:
        deparment_url (str): URL департамента (апартаментов) на Zillow
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Настройка прокси-сервера, если указан
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    # Выполнение GET-запроса к указанному URL апартаментов с заголовками и имитацией браузера
    response = requests.get(url=deparment_url, headers=headers, proxies=proxies, impersonate="chrome124")
    # Парсинг содержимого ответа для получения информации об апартаментах
    data = parse_body_deparments(response.content)
    return data

def get_from_home_url(home_url: str, proxy_url: str | None = None) -> dict[str, Any]:
    """
    Извлекает и парсит информацию о доме из указанного URL
    
    Аргументы:
        home_url (str): URL недвижимости
        proxy_url (str | None, опционально): URL прокси-сервера для маскировки запроса. По умолчанию None.
    
    Возвращает:
        dict[str, Any]: распознанная информация о недвижимости
    """
    # Настройка прокси-сервера, если указан
    proxies = {"http": proxy_url, "https": proxy_url} if proxy_url else None
    # Выполнение GET-запроса к указанному URL с заголовками и имитацией браузера
    response = requests.get(url=home_url, headers=headers, proxies=proxies, impersonate="chrome124")
    # Вызов исключения в случае ошибки HTTP
    response.raise_for_status()
    # Парсинг содержимого ответа для получения информации о доме
    data = parse_body_home(response.content)
    return data