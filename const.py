from secret_files import MONGO_CONNECTION_STRING

# Варианты ответа на тест
# Возраст
AGE_18_21 = 1
AGE_22_27 = 2
AGE_28_34 = 3
AGE_35_45 = 4
AGE_46_65 = 5
AGE_65_more = 6
# Семейное положение
MARRIED_TRUE = 1
MARRIED_FALSE = 2
# Количество детей
CHILDREN_0 = 1
CHILDREN_1 = 2
CHILDREN_2 = 3
CHILDREN_3_more = 4
# Образование
EDUCATION_NONE = 1
EDUCATION_SCHOOL = 2
EDUCATION_COLLEGE = 3
EDUCATION_UNIVERSITY = 4
# Стаж работы
WORK_DURATION_less_0p5 = 1
WORK_DURATION_0p5_1p5 = 2
WORK_DURATION_1p5_3 = 3
WORK_DURATION_3_more = 4
# Работа по профессии
WORK_EQUALS_EDUCATION_TRUE = 1
WORK_EQUALS_EDUCATION_FALSE = 2
# Доход по месту работы
INCOME_less_20 = 1
INCOME_20_30 = 2
INCOME_30_50 = 3
INCOME_50_100 = 4
INCOME_100_more = 5
# Поручители
SPONSORS_TRUE = 1
SPONSORS_FALSE = 2


TEST_ANSWER_TEST_JSON = {
    "age": AGE_22_27,
    "married": MARRIED_FALSE,
    "children": CHILDREN_0,
    "education": EDUCATION_UNIVERSITY,
    "work_duration": WORK_DURATION_less_0p5,
    "work_equals_education": WORK_EQUALS_EDUCATION_TRUE,
    "income": INCOME_30_50,
    "sponsors": SPONSORS_FALSE
}

ANSWERS_TEST_WEIGHTS = {
    "age": {
        AGE_18_21: 10,
        AGE_22_27: 22,
        AGE_28_34: 35,
        AGE_35_45: 35,
        AGE_46_65: 22,
        AGE_65_more: 10
    },
    "married": {
        MARRIED_TRUE: 20,
        MARRIED_FALSE: 15
    },
    "children": {
        CHILDREN_0: 15,
        CHILDREN_1: 20,
        CHILDREN_2: 15,
        CHILDREN_3_more: 10
    },
    "education": {
        EDUCATION_NONE: 0,
        EDUCATION_SCHOOL: 5,
        EDUCATION_COLLEGE: 15,
        EDUCATION_UNIVERSITY: 25
    },
    "work_duration": {
        WORK_DURATION_less_0p5: 5,
        WORK_DURATION_0p5_1p5: 10,
        WORK_DURATION_1p5_3: 17,
        WORK_DURATION_3_more: 25
    },
    "work_equals_education": {
        WORK_EQUALS_EDUCATION_TRUE: 10,
        WORK_EQUALS_EDUCATION_FALSE: 0
    },
    "income": {
        INCOME_less_20: 5,
        INCOME_20_30: 15,
        INCOME_30_50: 25,
        INCOME_50_100: 30,
        INCOME_100_more: 35
    },
    "sponsors": {
        SPONSORS_TRUE: 35,
        SPONSORS_FALSE: 0
    }
}

TEST_BANK_DEMANDS_JSON = {
    'bank_name': 'Бета-банк',
    'minimum_score': 100,
    'interest_rate': {'15': [100, 150], '20': [150, 205]},
    'loan_duration': {'3': [100, 150], '5': [150, 205]},
    'loan_sum': {'100000': [100, 150], '350000': [150, 205]},
    'test_answers': {
        "age": [AGE_22_27, AGE_28_34, AGE_35_45, AGE_46_65],
        "married": [MARRIED_TRUE, MARRIED_FALSE],
        "children": [CHILDREN_0, CHILDREN_1, CHILDREN_2, CHILDREN_3_more],
        "education": [EDUCATION_COLLEGE, EDUCATION_UNIVERSITY],
        "work_duration": [WORK_DURATION_less_0p5, WORK_DURATION_0p5_1p5, WORK_DURATION_1p5_3, WORK_DURATION_3_more],
        "work_equals_education": [WORK_EQUALS_EDUCATION_TRUE, WORK_EQUALS_EDUCATION_FALSE],
        "income": [INCOME_20_30, INCOME_30_50, INCOME_50_100, INCOME_100_more],
        "sponsors": [SPONSORS_TRUE, SPONSORS_FALSE]
    }
}
