from aiogram.dispatcher.filters.state import StatesGroup, State


class Test1(StatesGroup):

    Q11 = State()
    Q12 = State()
    Q13 = State()


class Test2(StatesGroup):

    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()




class Test(StatesGroup):

    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State() # Шаги ставок
    Q7 = State()


    Q8 = State()   # Добавление услуги на границе
    Q9 = State()   # Добавление услуги на границе
    Q10 = State()   # Добавление услуги на границе

    Q11 = State()   # Поездки
    Q12 = State()   # Поездки
    Q13 = State()   # Поездки
    Q14 = State()   # Поездки
    Q15 = State()   # Поездки
    Q16 = State()   # Поездки
    Q17 = State()   # Поездки

    Q18 = State()   # Изменить никнейм
    Q19 = State()   #
    Q20 = State()   #
    Q21 = State()   #
    Q22 = State()   # Изменить телефон
    Q23 = State()   # Изменить авто
    Q24 = State()   # Изменить стаж

    Q25 = State()   # Обратная связь
    Q26 = State()   # pro_7

    Q27 = State()   # pro_14
    Q28 = State()   # pro_14

    Q29 = State()   # pro_28
    Q30 = State()   # pro_28

    Q31 = State()   # light_7

    Q32 = State()   # light_14

    Q33 = State()   # light_28

    Q34 = State()   # add_audio