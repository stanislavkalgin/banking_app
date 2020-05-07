import const
from pymongo import MongoClient


class Client:
    """Класс, содержащий данные клиента

    Данные в этом классе не участвуют в расчете и одобрении заявки, являются неизменными для каждого клиента,
    испольщуются только для отображения на экране, позже сюда можно добавить и пароль для аутентификации,
    self.id - PRIMARY KEY для таблицы клиентов
    Клиенту нужно ввести имя, номер телефона, адрес"""
    def __init__(self, name, phone_number, address, email):
        self._id = get_available_id(mode=const.SWITCHER_CLIENTS_MODE)
        self.name = name
        self.phone_number = phone_number
        self.address = address
        self.email = email

    def get_id(self):
        return self._id


class CreditRequest:
    """Класс заявки на кредит, связан с клиентом через client_id

    request_id - PRIMARY KEY для таблицы заявок
    Клиенту нужно будет ввести пол (const str), возраст (int), срок проживания в данной области (int),
    класс работадателя (государственный и тд) (const int), наличие счета в банке (bool), недвижимоти (bool),
    страховки жизни либо здоровья (bool), срок работы на текущей работе (int), зарплату (int),
    сумму требуемого кредита (int), срок кредитования (int)

    Всё, что вводится здесь, используется для решения по кредиту, и большинство может изменяться от заявки к заявке"""
    def __init__(self, client_id, gender, age, time_in_city, employer,
                 has_bank_account, has_real_estate, has_insurance, employment_time,
                 client_salary, credit_sum, credit_time_range):
        self.client_id = client_id
        self._id = get_available_id(mode=const.SWITCHER_REQUESTS_MODE)
        # Поля для расчета кредитного рейтинга
        self.client_gender = gender
        self.client_age = age
        self.client_time_in_city = time_in_city
        self.client_employer_class = employer
        self.client_has_bank_account = has_bank_account
        self.client_has_real_estate = has_real_estate
        self.client_has_insurance = has_insurance
        self.client_employment_time = employment_time
        # Сам кредитный рейтинг
        self.client_credit_score = self.calculate_credit_score()
        # Поля, относящиеся к самой заявке - зарплата клиента, сумма, период, рассчитанная годовая ставка процента,
        # максимальная сумма кредита, доступная для этого клиента
        self.client_salary = client_salary
        self.requested_sum = credit_sum
        self.time_range = credit_time_range
        self.interest_rate = self.calculate_interest_rate()
        self.max_sum = self.calculate_max_credit_sum()
        # Статус заявки
        self.status = self.prior_approval()

    def calculate_credit_score(self):
        """Кредитный рейтинг по модели Дюрана. Положительный кредитный рейтинг показывает,
        сколько годовых доходов заемщика банк может ему предоставить в качестве кредита"""
        score = 0
        # женщины получают 0.4 к рейтингу, мужчины не получают ничего
        if self.client_gender == const.GENDER_FEMALE:
            score += 0.4
        # за каждый год возраста свыше 20 лет + 0.1 балла, но не более 0.3
        if 20 < self.client_age < 24:
            score += (self.client_age - 20) * 0.1
        elif self.client_age >= 24:
            score += 0.3
        # за каждый год проживания в данной местности + 0.042 балла, но не более 0.42
        if self.client_time_in_city < 11:
            score += self.client_time_in_city * 0.042
        elif self.client_time_in_city >= 11:
            score += 0.42
        # государственный работодатель(2) + 0.55, частный(1) + 0.16, ИП или бизнес(0) - ничего
        if self.client_employer_class == const.STATE_EMPLOYER:
            score += 0.55
        elif self.client_employer_class == const.PRIVATE_EMPLOYER:
            score += 0.16
        # наличие накопительного счета + 0,45 баллов; наличие недвижимости + 0,35 баллов;
        # наличие полиса по страхованию + 0,19 баллов
        if self.client_has_bank_account:
            score += 0.45
        if self.client_has_real_estate:
            score += 0.35
        if self.client_has_insurance:
            score += 0.19
        # за каждый год работы на текущем предприятии 0,059 баллов
        score += self.client_employment_time * 0.059
        # возвращает положительный рейтинг, если заемщик платежеспособен
        return (score - 0.85) / 2

    def calculate_max_credit_sum(self):
        """Расчет суммы кредита, которую может выдать банк заемщику"""
        if self.client_credit_score <= 0:
            return 0
        else:
            return self.client_salary * 12 * self.client_credit_score

    def calculate_interest_rate(self):
        """Расчет кредитной ставки, чем выше рейтинг тем ниже ставка, ставка != множитель"""
        return 0.22 + (self.client_credit_score * -0.05)

    def calculate_monthly_payment(self):
        """Расчет ежемесячного платежа по формуле аннуитетных платежей"""
        i = self.interest_rate / 12
        n = self.time_range
        k = (i * ((1 + i) ** n)) / (((1 + i) ** n) - 1)
        return round(self.requested_sum * k, 2)

    def prior_approval(self):
        """Возвращает код статуса заявки - 0 если предварительно не одобрена из за излишней суммы,
         1 если предварительно одобрена, -2 если клиент признан неплатежеспособным"""
        max_sum = self.calculate_max_credit_sum()
        if self.client_credit_score < 0:
            return const.REQUEST_REJECTED_BAD_SCORE  # -2
        elif self.requested_sum <= max_sum:
            return const.REQUEST_PRIOR_APPROVED  # 1
        else:
            return const.REQUEST_PRIOR_REJECTED  # 0


def get_available_id(mode):
    """Запрос из БД незанятого id"""
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


if __name__ == "__main__":
    # print(calculate_credit_score("F", 50, 30, 2, True, True, True, 30))
    # print(calculate_interest_rate())
    # print(calculate_monthly_payment(500000, 0.18, 12))
    pass
