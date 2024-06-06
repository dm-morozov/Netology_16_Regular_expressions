
# Адресная книга

Домашнее задание к лекции 2.2 «Regular expressions»

## Описание проекта

В рамках этого задания я научился использовать регулярные выражения для обработки данных в адресной книге. Кейс основан на реальных данных из [ФНС](https://www.nalog.ru/opendata/) и [Минфин](https://www.minfin.ru/ru/opendata/).

### Задачи

1. Поместить Фамилию, Имя и Отчество человека в соответствующие поля `lastname`, `firstname` и `surname`. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
2. Привести все телефоны в формат `+7(999)999-99-99`. Если есть добавочный номер, формат будет такой: `+7(999)999-99-99 доб.9999`.
3. Объединить все дублирующиеся записи о человеке в одну. Считается, что если совпадают одновременно Фамилия и Имя, то это один и тот же человек.

## Что было сделано

### Шаг 1: Чтение данных из файла

Сначала я прочитал данные из исходного CSV файла в список `contacts_list`:

```
import csv
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

```

### Шаг 2: Обработка данных

Затем я обработал контакты, выделяя ФИО, организацию, должность, телефон и email. Я использовал регулярные выражения для форматирования номеров телефонов и объединения дублирующихся записей:

```
import re

# Шаблон регулярного выражения для форматирования телефонных номеров
pattern = r'(8|\+7)\s*\(*(\d{3})\)*\s?-?(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?д?о?б?\.?\s*(\w*)'
pattern_compile = re.compile(pattern)

# Обрабатываем контакты
processed_contacts = []
for contact in contacts_list[1:]:
    fio = " ".join(contact[:3]).strip().split(" ")
    last_name = fio[0]
    first_name = fio[1] if len(fio) > 1 else ""
    surname = fio[2] if len(fio) > 2 else ""

    organization = contact[3].strip() if contact[3] else ""
    position = contact[4].strip() if contact[4] else ""

    # Форматируем номер телефона
    phone_wrong = contact[5].strip() if contact[5] else ""
    phone_list = pattern_compile.findall(phone_wrong)
    phone_tuple = phone_list[0] if phone_list else None

    if phone_tuple:
        phone_number = f"+7({phone_tuple[1]}){phone_tuple[2]}-{phone_tuple[3]}-{phone_tuple[4]}"
        extension_number = phone_tuple[5] if len(phone_tuple) > 5 else None
        full_phone_number = phone_number + f" доб.{extension_number}" if extension_number else phone_number
    else:
        full_phone_number = ""

    email = contact[6].strip() if contact[6] else ""

    processed_contacts.append([last_name, first_name, surname, organization, position, full_phone_number, email])

# Группируем контакты по ФИО
grouped_contacts = {}

for contact in processed_contacts:
    key = (contact[0], contact[1])
    if key not in grouped_contacts:
        grouped_contacts[key] = contact
    else:
        existing_cont = grouped_contacts[key]
        grouped_contacts[key] = [
            contact[0],
            contact[1],
            contact[2] if contact[2] else existing_cont[2],
            contact[3] if contact[3] else existing_cont[3],
            contact[4] if contact[4] else existing_cont[4],
            contact[5] if contact[5] else existing_cont[5],
            contact[6] if contact[6] else existing_cont[6]
        ]

# Преобразуем словарь в список для записи в CSV
contact_list_for_csv = [contacts_list[0]] + list(grouped_contacts.values())
pprint(contact_list_for_csv)

```

### Шаг 3: Сохранение данных в файл

Сохраняем обработанные данные в новый CSV файл:

```python
pythonКопировать код
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contact_list_for_csv)

```

## Чему я научился

- Использовать регулярные выражения для поиска и замены данных в строках.
- Разделять строку на части и корректно обрабатывать элементы.
- Форматировать номера телефонов в определенный формат.
- Обрабатывать данные из CSV файлов и сохранять их обратно в формате CSV.
- Объединять дублирующиеся записи, группируя данные по определенным критериям.

## Заключение

Этот проект помог мне улучшить навыки работы с регулярными выражениями и данными в формате CSV. Я научился приводить данные в порядок и обрабатывать их для дальнейшего использования.

```

Этот `README.md` объясняет, что было сделано, чему ученик научился и предоставляет примеры кода для выполнения задач.

```