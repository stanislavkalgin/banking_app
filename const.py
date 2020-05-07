from secret_files import MONGO_CONNECTION_STRING

# классы работодателя
STATE_EMPLOYER = 2
PRIVATE_EMPLOYER = 1
SELF_EMPLOYER = 0
# статусы заявки, PRIOR - предварительное програмное одобрение/отклонение, требующее работы оператора банка
REQUEST_APPROVED_MANUALLY = 2
REQUEST_PRIOR_APPROVED = 1
REQUEST_PRIOR_REJECTED = 0
REQUEST_REJECTED_MANUALLY = -1
REQUEST_REJECTED_BAD_SCORE = -2
# пол клиента
GENDER_MALE = "M"
GENDER_FEMALE = "F"
# для выбора режима работы функции запроса свободного id
SWITCHER_REQUESTS_MODE = 1
SWITCHER_CLIENTS_MODE = 2
