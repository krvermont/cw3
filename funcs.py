import json
from datetime import datetime

# получение всех данных
def get_data() -> list[dict]:
    with open('operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

# получение выполненных операций
def get_executed_data(data, executed_data_empty=False):
    data = [x for x in data if 'state' in x and x['state'] == "EXECUTED"]
    if executed_data_empty:
        data = [x for x in data if 'from' in x]
    return data

# получение последних данных выполненных операций
def get_last_data(data, count_last_data):
    data = sorted(data, key=lambda x: x['date'], reverse=True)
    return data[:count_last_data]

# форматируем последние выполенные операции
def get_needed_data(data):
    needed_data = []
    for row in data:
        # форматируем дату выполнения операции в формат ДД.ММ.ГГГГ
        old_format_date = datetime.strptime(row['date'], '%Y-%m-%dT%H:%M:%S.%f')
        date = old_format_date.strftime('%d.%m.%Y')
        description = row['description']

        # получаем данные отправителя и скрываем данные карты по формату XXXX XX** **** XXXX
        sender = row['from'].split()
        sender_card_number = sender.pop(-1)
        sender_private_card = sender_card_number[:6] + (len(sender_card_number[6:-4]) * '*') + sender_card_number[-4:]
        letter, letter_size = len(sender_private_card), len(sender_private_card) // 4
        sender_private_card_number = " ".join([sender_private_card[i:i + letter_size] for i in range(0, letter, letter_size)])
        sender_info = ' '.join(sender)

        # маскировка счета в формате **XXXX
        bill_number = row['to'].split()[-1]
        private_bill = '*' + '*' + bill_number[-4:]
        amount = f'{row["operationAmount"]["amount"]} {row["operationAmount"]["currency"]["name"]}'

        needed_data.append(f'''{date} {description}
{sender_info} {sender_private_card_number} -> Счет {private_bill}
{amount}
'''
 )
    return needed_data

