from entities import *
from pymongo import MongoClient


def create_new_request(client_id):
    """Создание заявки из консоли, константы вводятся в ручную, ибо временно, потом будут поступать с фронта"""
    gender = input("Ваш пол: M/F?")
    while gender not in "MF":
        gender = input("Введите пол нормально M/F")
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


def create_new_client(phone_number):
    """Если номера телефона в базе нет, создается новый клиент с запросом полей"""
    name = input("Ваше имя: ")
    address = input("Ваш адрес: ")
    email = input("Ваш e-mail: ")
    new_client = Client(name=name,
                        phone_number=phone_number,
                        address=address,
                        email=email)
    return new_client


def client_create_request():
    """Сценарий создания заявки клиентом в консольном варианте
    Пользователь ищется по номеру телефона, подразумевается что он уникален, если номера в базе нет,
    создается новый пользователь"""
    phone_number = input("Ваш номер телефона")
    client = MongoClient(const.MONGO_CONNECTION_STRING)
    db = client.banking_app
    resp = db.credit_clients.find_one({"phone_number": phone_number})
    if resp is None:
        new_client = create_new_client(phone_number)
        db.credit_clients.insert_one(new_client.__dict__)
        client_id = new_client.get_id()
    else:
        print("Мы Вас узнали, {}".format(resp["name"]))
        client_id = resp["_id"]
    print("Заполните заявку")
    new_request = create_new_request(client_id)
    decision = get_bool_from_input("Отправить заявку? ")
    if decision:
        db.credit_requests.insert_one(new_request.__dict__)
        if new_request.status == const.REQUEST_PRIOR_APPROVED:
            print("Ваша заявка предварительно одобрена, ежемесячный платеж составит {} рублей".format(str(new_request.calculate_monthly_payment())))
        elif new_request.status == const.REQUEST_PRIOR_REJECTED:
            print("Мы можем выдать вам только {} рублей".format(str(new_request.max_sum)))
        else:
            print("Денег не будет, отказано")


if __name__ == "__main__":
    client_create_request()
