from utils import utils
import os.path

PATH = os.path.abspath("data/operations.json")


def main():
    transactions = utils.get_transactions_list(PATH)
    executed_transaction = utils.get_executed_transactions(transactions)
    last_5_dates = utils.get_last_5_dates(executed_transaction)
    last_5_executed_transactions = utils.get_sorted_transactions_by_date(last_5_dates, executed_transaction)
    changed_transactions = utils.to_change_transactions(last_5_executed_transactions)
    last_5 = utils.to_output(changed_transactions)

    return last_5


print(main())
