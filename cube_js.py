import datetime
import http.client
import json
import csv
import requests

"""ВАРИАНТ_№1"""
# Словарь для преобразования имен полей
field_mapping = {
    "events_event.active": "Активные",
    "events_event.deleted": "Удаленные",
    "events_event.show_price": "Цена",
    "events_event.tickets_count": "Количество билетов"
}

# Параметры запроса
params = {
    "query": {
        "measures": ["events_event.tickets_count"],
        "dimensions": ["events_event.active", "events_event.deleted", "events_event.show_price"],
        "order": {"events_event.tickets_count": "desc"},
        "filters": [{"member": "events_event.address", "operator": "set"}]
    }
}

# Отправка запроса
conn = http.client.HTTPConnection("localhost", 4000)
conn.request("POST", "/cubejs-api/v1/load", body=json.dumps(params), headers={"Content-Type": "application/json"})
response = conn.getresponse()

# Проверка успешности запроса
if response.status == 200:
    data = json.loads(response.read().decode())
    current_time = datetime.datetime.now().strftime("%Y.%m.%d_%H-%M")

    # Получение заголовков
    headers = data['data'][0].keys()

    # Преобразование заголовков с использованием field_mapping
    translated_headers = [field_mapping.get(header, header) for header in headers]

    # Преобразование данных в CSV
    with open(f'result/{current_time}_output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Запись заголовков
        writer.writerow(translated_headers)
        # Запись строк данных
        for row in data['data']:
            writer.writerow(row.values())

    print(f"Данные успешно сохранены в {current_time}_output.csv")
else:
    print(f"Ошибка запроса: {response.status}")

conn.close()



"""ВАРИАНТ_№2"""
# # URL для запроса к CubeJS API
# url = 'http://localhost:4000/cubejs-api/v1/load'
#
# # Запросные параметры
# query = {
#     "measures": ["events_event.tickets_count"],
#     "dimensions": ["events_event.active", "events_event.deleted", "events_event.show_price", "events_event.date", "events_event.time", "events_event.created"],
#     "order": {"events_event.tickets_count": "desc"}
# }
#
# # Подготовка параметров запроса
# payload = {
#     "query": query
# }
#
# # Выполнение запроса
# response = requests.post(url, json=payload)
#
# # Проверка статуса ответа
# if response.status_code == 200:
#     # Попытка разобрать JSON ответ
#     try:
#         data = response.json()
#
#         # Печать полного ответа для отладки
#         print("Ответ от API CubeJS:")
#         print(json.dumps(data, indent=2))
#
#         # Проверьте, есть ли ключ 'data' в ответе
#         if 'data' in data:
#             results = data['data']
#
#             if results:
#                 # Получаем список всех dimensions из запроса
#                 requested_dimensions = query.get("dimensions", [])
#
#                 # Определяем заголовки на основе запрашиваемых dimensions
#                 if isinstance(results, list) and len(results) > 0:
#                     available_dimensions = set(requested_dimensions) & set(results[0].keys())
#                     fieldnames = list(available_dimensions)
#                 else:
#                     fieldnames = []
#
#                 # Запись в CSV
#                 current_time = datetime.datetime.now().strftime("%Y.%m.%d_%H-%M")
#                 with open(f'{current_time}_output.csv', 'w', newline='') as csvfile:
#                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#                     # Запись заголовков, если они есть
#                     if fieldnames:
#                         writer.writeheader()
#
#                     # Запись строк данных
#                     for row in results:
#                         # Отфильтровываем данные по доступным dimensions
#                         filtered_row = {key: row.get(key, "") for key in fieldnames}
#                         writer.writerow(filtered_row)
#
#                 print("Данные успешно сохранены в 'output.csv'.")
#             else:
#                 print("Ответ не содержит данных.")
#         else:
#             print("Ключ 'data' отсутствует в ответе от API.")
#     except json.JSONDecodeError:
#         print("Ошибка при разборе ответа JSON.")
# else:
#     print(f"Ошибка запроса: {response.status_code} - {response.text}")
