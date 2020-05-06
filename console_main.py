from entities import *


def create_new_request():
    """Создание заявки из консоли, константы вводятся в ручную, ибо временно"""
    client_id = 1
    gender = input("Ваш пол: M/F?")
    age = int(input("Ваш возраст: "))
    time_in_city = int(input("Как давно вы живете в этом городе?"))
    employer = int(input("Ваш работодатель: 2 - бюджетная организация, 1 - частная организация, 0 - вы предприниматель"))
    has_bank_account = get_bool_from_input("У вас есть вклад в банке?")
    has_real_estate = get_bool_from_input("У вас есть недвижимость в собственности?")
    has_insurance = get_bool_from_input("У вас есть страхование жизни или здоровья?")
    employment_time = int(input("Как давно вы работаете на своей работе?"))
    salary = int(input("Ваша зарплата: "))
    requested_sum = int(input("Требуемая сумма кредита, рублей: "))
    time_range = int(input("Срок кредитования, месяцев: "))
    request_object = CreditRequest(client_id=client_id,
                                   gender=gender,
                                   age=age,
                                   time_in_city=time_in_city,
                                   employer=employer,
                                   has_bank_account=has_bank_account,
                                   has_real_estate=has_real_estate,
                                   has_insurance=has_insurance,
                                   employment_time=employment_time,
                                   client_salary=salary,
                                   credit_sum=requested_sum,
                                   credit_time_range=time_range)
    return request_object


def get_bool_from_input(message):
    """Запрос ответа от пользователя и перевод его в bool"""
    res = input(message + "Y/N ")
    if res == "Y" or res == "y":
        return True
    elif res == "N" or res == "n":
        return False
    else:
        print("Не распознано")
        return get_bool_from_input(message)


a = create_new_request()
print("Статус заявки:", a.status)
print("Ежемесячный платеж", a.calculate_monthly_payment())
print("Максимальная сумма кредита", a.calculate_max_credit_sum()),
print("Кредитный рейтинг", a.client_credit_score)
print("Ставка по кредиту", a.interest_rate)
