from pprint import pprint
import re
import csv


with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)


# TODO 1: выполните пункты 1-3 ДЗ

# Шаблон регулярного выражения для форматирования телефонных номеров
pattern = r'(8|\+7)\s*\(*(\d{3})\)*\s?-?(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})\s*\(?д?о?б?\.?\s*(\w*)'
pattern_compile = re.compile(pattern)


# Обрабатываем контакты, выделяя ФИО, организацию, должность, телефон и email
processed_contacts = []
for contact in contacts_list[1:]:
    # pprint(contact)
    fio = " ".join(contact[:2]).strip().split(" ")
    last_name = fio[0]
    first_name = fio[1]
    surname = fio[2] if len(fio) > 2 else ""
    # print(last_name, first_name, surname)

    organization = contact[3].strip() if contact[3] else ""
    # print(organization)
    position = contact[4].strip() if contact[4] else ""
    # print(position)

    # Номер в правильном формате +7(999)999-99-99 доб.9999
    phone_wrong = contact[5].strip() if contact[5] else ""
    phone_list = pattern_compile.findall(phone_wrong)
    phone_tuple = phone_list[0] if phone_list else None
    # print(phone_tuple)

    if phone_tuple:
        phone_number = f"+7({phone_tuple[1]}){phone_tuple[2]}-{phone_tuple[3]}-{phone_tuple[4]}"
        extension_number = phone_tuple[5] if len(phone_tuple) > 5 else None
        full_phone_number = phone_number + ' доб.' + extension_number if extension_number else phone_number
        # print(full_phone_number)
    else:
        full_phone_number = ""
        # print('Номер не найден')

    email = contact[6].strip() if contact[6] else ""
    # print(email)

    processed_contacts.append([last_name, first_name, surname, organization, position, full_phone_number, email])

# print(processed_contacts)

# Группируем контакты по ФИО
grouped_contacts = {}

for contact in processed_contacts:
    key = (contact[0], contact[1])
    # print(key)
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
# pprint(grouped_contacts)

# Преобразуем словарь в список для записи в CSV
contact_list_for_csv = [contacts_list[0]] + list(grouped_contacts.values())
print(contact_list_for_csv)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contact_list_for_csv)