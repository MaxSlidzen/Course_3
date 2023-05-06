import json


def get_transactions_list(path):
    with open(path, 'r', encoding='utf-8') as file:
        transactions = json.load(file)
        return transactions


def get_executed_transactions(transactions):
    executed_transactions = [transaction for transaction in transactions if 'EXECUTED' in transaction.values()]
    # executed_transactions = [transaction for transaction in transactions if transaction['state'] == 'EXECUTED']

    return executed_transactions


def get_last_5_dates(executed_transactions):
    dates = [executed_transactions[i]["date"] for i in range(len(executed_transactions))]
    dates.sort(reverse=True)
    last_5_dates = dates[:5]
    return last_5_dates


def get_last_5_executed_transactions(last_5_dates, executed_transactions):
    last_5_executed_transactions = []

    for i_dates in range(len(last_5_dates)):
        i_transactions = 0
        while True:
            if last_5_dates[i_dates] != executed_transactions[i_transactions]['date']:
                i_transactions += 1
                continue
            else:
                last_5_executed_transactions.append(executed_transactions[i_transactions])
                break
    return last_5_executed_transactions


def to_change_date(_date):
    the_date = _date.split("T")[0]
    yyyy_mm_dd = the_date.split('-')
    right_date = f'{yyyy_mm_dd[2]}.{yyyy_mm_dd[1]}.{yyyy_mm_dd[0]}'
    return right_date


def to_mask_from(string):
    if string is not None:
        account = string.split(' ')
        number = account[len(account) - 1]
        masked_number = f'{number[:4]} {number[4:6]}** **** {number[-4:]}'
        account[len(account) - 1] = masked_number
    return " ".join(account)


def to_mask_to(string):
    account = string.split(' ')[1]
    masked_account = f'**{account[-4:]}'
    return f'{string.split(" ")[0]} {masked_account}'


def to_change_transactions(last_5_executed_transactions):
    for transaction in last_5_executed_transactions:
        transaction['date'] = to_change_date(transaction['date'])
        if 'from' in transaction:
            transaction['from'] = to_mask_from(transaction['from'])
        transaction['to'] = to_mask_to(transaction['to'])
    return last_5_executed_transactions


def to_output(changed_transactions):
    transactions = []
    for transaction in changed_transactions:
        transactions.append(f'{transaction["date"]} {transaction["description"]}\n'
                            f'{transaction["from"] if "from" in transaction else ""} -> {transaction["to"]}\n'
                            f'{transaction["operationAmount"]["amount"]}'
                            f'{transaction["operationAmount"]["currency"]["name"]}\n')
    return "\n".join(transactions)
