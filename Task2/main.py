from pprint import pprint

import requests

BASE_URL = 'https://toyotas.pythonanywhere.com'

def get_auth_token(phone_number):
    print(f'Отправка запроса с номером телефона {phone_number}...', end='')

    url = f'{BASE_URL}/auth/send-code/'  # URL для запроса
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'number': phone_number,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print('Ok')
    else:
        print(f'Ошибка {response.status_code}:', response.text)
        return None, None

    auth_code = response.json()['code']
    print()
    print('Получен код авторизации ', auth_code)
    print('Отправка запроса для авторизации...', end='')

    url = f'{BASE_URL}/auth/verification-code/'  # URL для запроса
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'number': phone_number,
        'code': auth_code
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print('Ok')
        #pprint(response.json())
    else:
        print(f'Ошибка {response.status_code}:', response.text)
        return None, None

    print('Получены данные для входа')
    print('access_token')
    print(f'{response.json()["access_token"][:30]}...')
    print('refresh_token')
    print(f'{response.json()["refresh_token"][:30]}...')
    print()

    return response.json()["access_token"], response.json()["refresh_token"]

def get_profile(token):
    print('Запрос информации о профиле...', end='')
    url = f'{BASE_URL}/users/profile/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Ok')
    else:
        return

    js = response.json()
    print('Получена информация о профиле')
    print(f"Номер телефона: {js['your_number']}")
    print(f"Инвайт-код: {js['your_code']}")
    print(f"Активированный код / None: {js['activated_code']}")
    print(f"Количество рефералов: {len(js['referals_numbers'])}")
    print(f"Список рефералов:")
    print(*[f'    {i}' for i in js['referals_numbers']])

    return js


auth, refresh = get_auth_token('+79080474120')
get_profile(auth)
