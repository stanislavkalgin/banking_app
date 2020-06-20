import entities
import const
from pprint import pprint


def test_create_bank_demand():
    test_bank_demands = const.TEST_BANK_DEMANDS_JSON
    success = entities.create_bank_demands(test_bank_demands)
    return success


def test_update_bank_demands():
    test_bank_demands = const.TEST_BANK_DEMANDS_JSON
    entities.update_bank_demands(test_bank_demands)


def test_delete_bank_demands():
    test_bank_name = 'Бетабанк'
    entities.delete_bank_demands(test_bank_name)


def test_calculate_credit_score():
    score = entities.calculate_credit_score(const.TEST_ANSWER_TEST_JSON)
    return score, (score == 117)


def test_get_bank_approvals():
    pprint(entities.get_bank_approvals(const.TEST_ANSWER_TEST_JSON))


def test_get_all_bank_names():
    return entities.get_all_bank_names()


if __name__ == "__main__":
    pprint(const.TEST_BANK_DEMANDS_JSON)