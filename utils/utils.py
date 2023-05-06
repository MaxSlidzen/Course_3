import json


def get_transactions_list(path):
    """
    Формирует список словарей с данными о переводах из файла .json
    :param path: путь к файлу с .json, str
    :return: список словарей с данными, list
    """
    with open(path, 'r', encoding='utf-8') as file:
        transactions = json.load(file)
        return transactions


def get_executed_transactions(transactions):
    """
    Формирует список выполненных переводов
    :param transactions: список всех переводов, list
    :return: список выполненных переводов, list
    """
    executed_transactions = []

    for transaction in transactions:

        # В случае некорректных данных в словаре, отлавливаем ошибку и пропускаем итерацию
        try:
            if transaction['state'] == 'EXECUTED':
                executed_transactions.append(transaction)
        except KeyError:
            continue

    return executed_transactions


def get_last_5_dates(transactions):
    """
    Формирует сортированный список из 5 дат переводов, начиная от самой последней даты
    :param transactions: список операций, list
    :return: список из 5 дат переводов, сортированный по времени выполнения, list
    """
    dates = [transactions[i]["date"] for i in range(len(transactions))]
    dates.sort(reverse=True)
    last_5_dates = dates[:5]

    return last_5_dates


def get_sorted_transactions_by_date(dates, transactions):
    """
    Отбирает операции по датам совершения операций из списка
    :param dates: даты, по которым будет проходить отбор операций, list
    :param transactions: исходный список операций, list
    :return: список операций, отобранный по соответствующим датам, list
    """
    sorted_transactions = []

    # Берем по очереди элементы списка дат
    for i_dates in range(len(dates)):

        # При каждой новой итерации, начинаем сверять дату из списка с датами операций в исходном списке и
        # добавлять соответствующие операции в отсортированный список
        i_transactions = 0
        while True:
            if dates[i_dates] != transactions[i_transactions]['date']:
                i_transactions += 1
                continue
            else:
                sorted_transactions.append(transactions[i_transactions])
                break

    return sorted_transactions


def to_change_date(date):
    """
    Преобразование даты в необходимый формат
    :param date: исходная дата в формате "гггг-мм-ддТчч:мм:сс.мс", str
    :return: дата в формате "дд.мм.гггг", str
    """
    the_date = date.split("T")[0]
    yyyy_mm_dd = the_date.split('-')

    return ".".join(reversed(yyyy_mm_dd))


def to_mask_from(string):
    """
    Маскировка счета отправителя, если такой счет есть
    :param string: исходный счет отправителя, str
    :return: замаскированный счет отправителя, str
    """
    # Учитываем случаи без счета отправителя
    if string is None:
        return None

    account = string.split(' ')
    number = account[len(account) - 1]
    masked_number = f'{number[:4]} {number[4:6]}** **** {number[-4:]}'
    account[len(account) - 1] = masked_number
    return " ".join(account)


def to_mask_to(string):
    """
    Маскировка счета получателя
    :param string: исходный счет получателя, str
    :return: замаскированный счет получателя, str
    """
    account = string.split(' ')[-1]
    masked_account = f'**{account[-4:]}'

    return f'{" ".join(string.split(" ")[0:-1])} {masked_account}'


def to_change_transactions(transactions):
    """
    Изменение даты и маскировка счетов отправителя и получателя в списке операций
    :param transactions: список исходных операций, list
    :return: список форматированных операций
    """
    for transaction in transactions:
        transaction['date'] = to_change_date(transaction['date'])
        transaction['to'] = to_mask_to(transaction['to'])

        # Учитываем случаи без счета отправителя
        if 'from' in transaction:
            transaction['from'] = to_mask_from(transaction['from'])

    return transactions


def to_output(transactions):
    """
    Формирует список с данными операциями в необходимом для вывода формате
    :param transactions: список исходных операций, list
    :return: выводимые данные в необходимом формате, str
    """
    changed_transactions = []

    for transaction in transactions:
        changed_transactions.append(f'{transaction["date"]} {transaction["description"]}\n'
                                    f'{transaction["from"] if "from" in transaction else ""} -> {transaction["to"]}\n'
                                    f'{transaction["operationAmount"]["amount"]} '
                                    f'{transaction["operationAmount"]["currency"]["name"]}\n')

    return "\n".join(changed_transactions)
