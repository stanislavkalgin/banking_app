import const
from pymongo import MongoClient


def create_bank_demands(bank_demands):
    """Создание в БД записи с требованиями нового банка
    Вход: JSON (словарь) вида:
    {bank_name: "Бета-банк",
    minimum_score: 100, // минимальный кредитный рейтинг 100
    interest_rate: {15: [100, 200], 20: [200, 300]}, // ставка 15% при 100 <= кредитный_рейтинг < 200 и т.д.
    loan_duration: {3: [100,250], 5: [250, 300]}, // срок кредитования 3 года при 100 <= кредитный_рейтинг < 250
    loan_sum: {'100000': [100, 200], '350000': [200, 300]} // сумма 100000 при 100 <= кредитный_рейтинг < 200 и т.д.
    test_answers: {age: [2, 3, 4, 5], ...}}  // приемлимые ответы на каждый вопрос теста"""
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    db.banks_demands.insert_one(bank_demands)


def update_bank_demands(bank_demands):
    """Обновление записи в БД о требованиях банка
    Вход: словарь новых требований банка
    Поиск банка происходит по названию"""
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    query = {'bank_name': bank_demands['bank_name']}
    new_demands = {
        '$set':
            {
                'minimum_score': bank_demands['minimum_score'],
                'interest_rate': bank_demands['interest_rate'],
                'loan_duration': bank_demands['loan_duration'],
                'loan_sum': bank_demands['loan_sum'],
                'test_answers': bank_demands['test_answers']
            }
    }
    db.banks_demands.update_one(query, new_demands)


def delete_bank_demands(bank_name):
    """Удаление записи о требованиях банка по имени
    Вход: название банка"""
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    db.banks_demands.delete_one({'bank_name': bank_name})


def calculate_credit_score(test_answers):
    """Расчет кредитного рейтинга
    Вход: словарь ответов на тест
    Возврат: число - кредитный рейтинг от 45 до 205"""
    score = 0
    for attribute in test_answers:
        score += const.ANSWERS_TEST_WEIGHTS[attribute][test_answers[attribute]]
    return score


def get_bank_approvals(test_answers):
    """Получение списка банков, одобряющих кредит по результатам теста
    Вход: словарь ответов на тест
    Выход: список словарей одобривших кредит банков с суммами, сроками и ставками"""
    # Запрос из БД банков с минимальным одобряемым рейтингом меньше нашего
    score = calculate_credit_score(test_answers)
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    answer = db.banks_demands.find({'minimum_score': {'$lt': score}})

    # Выбор банков, которые удовлетворяют наши ответы на тест
    approved_banks = []
    for bank in answer:
        if check_demands(test_answers, bank['test_answers']):
            approved_banks.append(bank)

    # Получение от одобривших банков условий, удовлетворяющих кредитному рейтингу
    banks_conditions = {}
    for bank_result in approved_banks:
        conditions = get_conditions_for_client(score, bank_result)
        banks_conditions.update({conditions['bank_name']: conditions})
    return banks_conditions


def get_conditions_for_client(score, demands_dict):
    """Выбор условий, предоставляемых клиенту с данным рейтингом
    Вход: кредитный рейтинг, словарь требований
    Возврат: словарь предоставляемых условий"""
    result = {'bank_name': demands_dict['bank_name']}
    for attribute in ['interest_rate', 'loan_duration', 'loan_sum']:
        for key in demands_dict[attribute].keys():
            lower_border = demands_dict[attribute][key][0]
            higher_border = demands_dict[attribute][key][1]
            if lower_border <= score < higher_border:
                result.update({attribute: key})
    return result


def check_demands(test_dict, demands_dict):
    """Проверка соответствия ответов на тест условиям банка
    Вход: словарь ответов, словарь условий
    Возврат: True если условия удовлетворены, False если не уловлетворены"""
    for key in test_dict.keys():
        if test_dict[key] not in demands_dict[key]:
            return False
    return True


def get_available_id(mode):
    """Запрос из БД незанятого id
    Временно не используется, но вдруг"""
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    if mode == const.SWITCHER_CLIENTS_MODE:
        resp = db.credit_clients.find_one({"$query": {}, "$orderby": {"_id": -1}})
    else:
        resp = db.credit_requests.find_one({"$query": {}, "$orderby": {"_id": -1}})
    if resp is None:
        return 1
    else:
        next_id = int(resp["_id"]) + 1
        return str(next_id)
