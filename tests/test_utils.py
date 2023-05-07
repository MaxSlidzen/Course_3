from utils import utils
import pytest
import os.path


def test_get_transactions_list():
    json_path = os.path.abspath('test.json')
    assert utils.get_transactions_list(json_path) == [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041"
        },
        [
            1,
            2,
            3,
            4,
            5
        ],
        "Элемент списка",
        True,
        56.6,
        None
    ]
    with pytest.raises(FileNotFoundError):
        utils.get_transactions_list('Несуществующий путь')


def test_get_executed_transactions():
    assert utils.get_executed_transactions([{'state': 'EXECUTED'}, {'state': 'cancelled'}]) == [{'state': 'EXECUTED'}]
    assert utils.get_executed_transactions([{'state': 'cancelled'}, {}, {'state': 'EXECUTED'}]) == [
        {'state': 'EXECUTED'}]


def test_get_last_5_dates():
    assert utils.get_last_5_dates([{'date': '2023-05-13'},
                                   {'date': '2009-04-13'},
                                   {'date': '2013-09-30'},
                                   {'date': '2023-05-14'},
                                   {'date': '2023-06-13'},
                                   {'date': '2018-12-01'},
                                   {'date': '2022-04-13'},
                                   {'date': '2015-09-10'},
                                   {'date': '2005-11-23'}]) == ['2023-06-13',
                                                                '2023-05-14',
                                                                '2023-05-13',
                                                                '2022-04-13',
                                                                '2018-12-01']


def test_get_sorted_transactions_by_date():
    dates = ['2023-06-13',
             '2018-12-01']

    transactions = [{'date': '2018-12-01'},
                    {
                        "id": 441945886,
                        "state": "EXECUTED",
                        "date": "2019-12-01",
                        "operationAmount": {
                            "amount": "31957.58",
                            "currency": {
                                "name": "руб.",
                                "code": "RUB"
                            }
                        },
                        "description": "Перевод организации",
                        "from": "Maestro 1596837868705199",
                        "to": "Счет 64686473678894779589"
                    },
                    {"id": 441945886,
                     "state": "EXECUTED",
                     "date": "2023-06-13"}]

    assert utils.get_sorted_transactions_by_date(dates, transactions) == [{"id": 441945886,
                                                                           "state": "EXECUTED",
                                                                           "date": "2023-06-13"},
                                                                          {'date': '2018-12-01'}]


def test_to_change_date():
    assert utils.to_change_date("2000-11-15") == '15.11.2000'
    assert utils.to_change_date("yyyy-mm-dd") == 'dd.mm.yyyy'


def test_to_mask_from():
    assert utils.to_mask_from(None) == None
    assert utils.to_mask_from('None 135698784562') == 'None 1356 98** **** 4562'


def test_to_mask_to():
    assert utils.to_mask_to('Счет 864523458972') == 'Счет **8972'
