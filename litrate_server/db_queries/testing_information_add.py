from db_queries.signingup import signup_user
from passlib.handlers.sha2_crypt import sha256_crypt
from db_queries.file_adding import *
from db_queries.messages_work import add_message
from db_queries.update_queries import update_user_name


def add_users():
    signup_user("brodskij@gmail.com", sha256_crypt.encrypt("123456"), "Creator") # id = 1
    update_user_name("Иосиф", "Бродский", 1)
    signup_user("esenin@gmail.com", sha256_crypt.encrypt("123456"), "Creator") # id = 2
    update_user_name("Сергей", "Есенин", 2)
    signup_user("shevchenko@gmail.com", sha256_crypt.encrypt("123456"), "Creator") # od = 3
    update_user_name("Тарас", "Шевченко", 3)
    signup_user("franko@gmail.com", sha256_crypt.encrypt("123456"), "Creator") # id = 4
    update_user_name("Иван", "Франко", 4)
    signup_user("ukrainka@gmail.com", sha256_crypt.encrypt("123456"), "Creator") # id = 5
    update_user_name("Леся", "Украинка", 5)
    signup_user("bookshome@gmail.com", sha256_crypt.encrypt("123456"), "Publisher") # id = 6
    update_user_name("Джон", "Сноу", 6)
    signup_user("vinnitsacityprintery@gmail.com", sha256_crypt.encrypt("123456"), "Publisher") # id = 7
    update_user_name("Агент", "Смит", 7)


def add_compositions():
    add_poem_by_text("", "Одиночество",
                     [], 1, 1) # 1
    add_poem_by_text("", "Натюрморт",
                     [], 1, 1) # 2
    add_poem_by_text("", "Я вас любил",
                     [], 1, 1) # 3
    add_poem_by_text("", "Вальсок",
                     [], 1, 1) # 4
    add_poem_by_text("", "Исповедь хулигана",
                     [], 2, 2)  # 5
    add_poem_by_text("", "Корова",
                     [], 2, 2)  # 6
    add_poem_by_text("", "Край любимый! Сердцу снятся",
                     [], 2, 2)  # 7
    add_poem_by_text("", "На кавказе",
                     [], 2, 2)  # 8
    add_poem_by_text("", "Осень",
                     [], 2, 2)  # 9
    add_poem_by_text("", "Думи мої, думи мої",
                     [], 3, 3)  # 10
    add_poem_by_text("", "Думка",
                     [], 3, 3)  # 11
    add_poem_by_text("", "На батька бісового я трачу...",
                     [], 3, 3)  # 12
    add_poem_by_text("", "Ой стрічечка до стрічечки",
                     [], 3, 3)  # 13
    add_poem_by_text("", "Ой я свого чоловіка",
                     [], 3, 3)  # 14
    add_poem_by_text("", "Плач Ярославни",
                     [], 3, 3)  # 15
    add_poem_by_text("", "Стоїть в селі Суботові",
                     [], 3, 3)  # 16
    add_poem_by_text("", "Туман, туман долиною",
                     [], 3, 3)  # 17
    add_poem_by_text("", "Я не нездужаю, нівроку...",
                     [], 3, 3)  # 18
    add_poem_by_text("", "Якби ви знали, паничі...",
                     [], 3, 3)  # 19
    add_poem_by_text("", "У неділю не гуляла",
                     [], 3, 3)  # 20
    add_poem_by_text("", "Тим неситим очам...",
                     [], 3, 3)  # 21
    add_poem_by_text("", "Тарасова ніч",
                     [], 3, 3)  # 22
    add_poem_by_text("", "Слава",
                     [], 3, 3)  # 23
    add_poem_by_text("", "Породила мене мати",
                     [], 3, 3)  # 24
    add_poem_by_text("", "Песня караульного у тюрьмы",
                     [], 3, 3)  # 25
    add_poem_by_text("", "Беркут",
                     [], 4, 4)  # 26
    add_prose_by_text("", "Будяки",
                     [], 4, 4)  # 27
    add_prose_by_text("", "Без праці",
                     [], 4, 4)  # 28
    add_poem_by_text("", "Мойсей",
                     [], 4, 4)  # 29
    add_poem_by_text("", "Декадент",
                     [], 4, 4)  # 30
    add_poem_by_text("", "Гімн",
                     [], 4, 4)  # 31
    add_prose_by_text("", "Лелія",
                     [], 5, 5)  # 32
    add_prose_by_text("", "Голосні струни",
                     [], 5, 5)  # 33
    add_prose_by_text("", "Пізно",
                     [], 5, 5)  # 34
    add_prose_by_text("", "Мгновение",
                     [], 5, 5)  # 35
    add_prose_by_text("", "Примара",
                     [], 5, 5)  # 36

