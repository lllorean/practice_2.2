import requests
import json
import os

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "resourse/save.json"

def fetch_rates():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()
        return data.get('Valute', {})
    except requests.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return {}

def load_groups():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Ошибка чтения файла save.json. Создаем новый.")
            return {}
    return {}

def save_groups(groups):
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(groups, f, ensure_ascii=False, indent=4)
        print("Группы сохранены в save.json")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")

def view_all_currencies(rates):
    if not rates:
        print("Нет данных о валютах.")
        return
    print("Текущие курсы валют:")
    for code, info in rates.items():
        print(f"{code}: {info['Name']} - {info['Value']} RUB (предыдущий: {info['Previous']})")

def view_specific_currency(rates):
    code = input("Введите код валюты (например, USD): ").upper()
    if code in rates:
        info = rates[code]
        print(f"{code}: {info['Name']} - {info['Value']} RUB (предыдущий: {info['Previous']})")
    else:
        print("Валюта не найдена.")

def create_group(groups):
    group_name = input("Введите название группы: ")
    if group_name in groups:
        print("Группа уже существует.")
        return
    groups[group_name] = []
    print(f"Группа '{group_name}' создана.")

def view_groups(groups, rates):
    if not groups:
        print("Нет созданных групп.")
        return
    for name, codes in groups.items():
        print(f"Группа '{name}':")
        for code in codes:
            if code in rates:
                info = rates[code]
                print(f"  {code}: {info['Name']} - {info['Value']} RUB")
            else:
                print(f"  {code}: Валюта не найдена.")

def edit_group(groups, rates):
    group_name = input("Введите название группы для редактирования: ")
    if group_name not in groups:
        print("Группа не найдена.")
        return
    print("1. Добавить валюту")
    print("2. Удалить валюту")
    choice = input("Выберите действие: ")
    code = input("Введите код валюты: ").upper()
    if choice == '1':
        if code not in groups[group_name]:
            if code in rates:
                groups[group_name].append(code)
                print(f"Валюта {code} добавлена в группу '{group_name}'.")
            else:
                print("Валюта не найдена в списке курсов.")
        else:
            print("Валюта уже в группе.")
    elif choice == '2':
        if code in groups[group_name]:
            groups[group_name].remove(code)
            print(f"Валюта {code} удалена из группы '{group_name}'.")
        else:
            print("Валюта не найдена в группе.")
    else:
        print("Неверный выбор.")

def main():
    rates = fetch_rates()
    groups = load_groups()
    while True:
        print("\nМеню:")
        print("1. Просмотреть текущий курс всех валют")
        print("2. Посмотреть валюту по коду")
        print("3. Создать группу валют")
        print("4. Просмотреть все группы")
        print("5. Изменить список отслеживаемых валют в группе")
        print("6. Сохранить группы")
        print("7. Обновить курсы")
        print("8. Выход")
        choice = input("Выберите опцию: ")
        if choice == '1':
            view_all_currencies(rates)
        elif choice == '2':
            view_specific_currency(rates)
        elif choice == '3':
            create_group(groups)
        elif choice == '4':
            view_groups(groups, rates)
        elif choice == '5':
            edit_group(groups, rates)
        elif choice == '6':
            save_groups(groups)
        elif choice == '7':
            rates = fetch_rates()
            print("Курсы обновлены.")
        elif choice == '8':
            save_groups(groups)
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()