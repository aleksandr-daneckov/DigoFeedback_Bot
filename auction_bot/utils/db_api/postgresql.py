import datetime
from typing import Union
from uuid import uuid4
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)

                elif fetchval:
                    result = await connection.fetchval(command, *args)

                elif fetchrow:
                    result = await connection.fetchrow(command, *args)

                elif execute:
                    result = await connection.execute(command, *args)
            return result

    # async def create_table_users(self):
    #     sql = """
    #     CREATE TABLE IF NOT EXISTS Users (
    #     id SERIAL PRIMARY KEY,
    #     full_name VARCHAR(255) NOT NULL,
    #     username varchar(255) NULL,
    #     telegram_id BIGINT NOT NULL UNIQUE
    #     );
    #     """
    #     await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id, user_name, full_name, phone):
        sql = "INSERT INTO users (telegram_id, user_name, full_name, phone) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, telegram_id, user_name, full_name, phone, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)



    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)




    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, fetchrow=True)





    async def my_account(self, telegram_id):
        """Проверяем, прошел ли пользователь опрос"""
        sql = "select * from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetch=True)





########################################################################################################################

    async def searh_ppr(self, name_checkpoint):
        """     """
        sql = "select * from checkpoint where name_checkpoint = $1"
        return await self.execute(sql, name_checkpoint, fetch=True)


    async def add_service_granica(self, name_service, name_checkpoint, telegram_id):
        """     """
        sql = "INSERT INTO service_granica (name_service, name_checkpoint, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, name_service, name_checkpoint, telegram_id, fetchrow=True)

    async def searh_service_granica(self, name_service, name_checkpoint):
        """     """
        sql = "select u.*, sg.* from users u left join service_granica sg on u.telegram_id = sg.telegram_id where name_service = $1 and name_checkpoint = $2"
        return await self.execute(sql, name_service, name_checkpoint, fetch=True)

    async def search_users(self, telegram_id):
        """    """
        sql = "select * from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetch=True)


    async def update_nick_user(self, nick, telegram_id):
        """    """
        sql = "UPDATE Users SET nick=$1 WHERE telegram_id=$2"
        return await self.execute(sql, nick, telegram_id, fetchrow=True)


    async def update_poezdki(self, phone, avto, staj, telegram_id):
        """    """
        sql = "UPDATE Users SET phone=$1, avto=$2, staj=$3 WHERE telegram_id=$4"
        return await self.execute(sql, phone, avto, staj, telegram_id, fetchrow=True)

    async def proverka_voditelya(self, telegram_id):
        """    """
        sql = "select avto from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def search_user_id(self, telegram_id):
        """    """
        sql = "select id from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)


    async def add_poezdka_1(self, user_id, date):
        """     """
        sql = "INSERT INTO poezdki (user_id, date) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, date, fetchrow=True)

    async def update_poezdki_finish(self, parametri, mesta, user_id):
        """    """
        sql = "UPDATE poezdki SET parametri = $1, mesta = $2 WHERE user_id = $3"
        return await self.execute(sql, parametri, int(mesta), user_id, fetchrow=True)

    async def search_poezdki(self, user_id):
        """    """
        sql = "select * from poezdki where user_id = $1"
        return await self.execute(sql, user_id, fetch=True)


    async def search_city_1(self, user_id):
        """    """
        sql = "select city_1 from poezdki where user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def search_city_2(self, user_id):
        """    """
        sql = "select city_2 from poezdki where user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def search_full_poezdki(self, user_id):
        """    """
        sql = "select u.*, p.* from users u left join poezdki p on u.id = p.user_id where u.id = $1"
        return await self.execute(sql, user_id, fetch=True)


    async def search_poezdku(self, city_1, city_2, date):
        """    """
        sql = "select u.*, p.* from users u left join poezdki p on u.id = p.user_id where city_1 = $1 and city_2 = $2 and date = $3 and mesta > 0"
        return await self.execute(sql, city_1, city_2, date, fetch=True)

    async def update_poezdki_finish_him(self, km, times, user_id):
        """    """
        sql = "UPDATE poezdki SET km = $1, times = $2 WHERE user_id = $3"
        return await self.execute(sql, km, times, user_id, fetchrow=True)


    async def update_poezdki_1(self, time, user_id):
        """    """
        sql = "UPDATE poezdki SET time = $1 WHERE user_id = $2"
        return await self.execute(sql, time, user_id, fetchrow=True)

    async def update_poezdki_2(self, price, city1, city2, user_id):
        """    """
        sql = "UPDATE poezdki SET price = $1, city_1 = $2, city_2 = $3 WHERE user_id = $4"
        return await self.execute(sql, price, city1, city2, user_id, fetchrow=True)

    async def add_poezdka2(self, user_id, city_1, city_2, date, time, price, parametri, times, mesta, km):
        """     """
        sql = "INSERT INTO poezdki2 (user_id, city_1, city_2, date, time, price, parametri, times, mesta, km) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) returning *"
        return await self.execute(sql, user_id, city_1, city_2, date, time, price, parametri, times, mesta, km, fetchrow=True)

    async def delete_poezdka(self, id):
        """    """
        sql = "delete from poezdki WHERE id = $1"
        return await self.execute(sql, id, fetchrow=True)

    async def search_mesta(self, id_poezdki):
        """    """
        sql = "select mesta from poezdki where id = $1"
        return await self.execute(sql, id_poezdki, fetchval=True)

    async def update_mesta(self, kolvo, id_poezdki):
        """    """
        sql = "UPDATE poezdki SET mesta = mesta - $1  WHERE id = $2"
        return await self.execute(sql, kolvo, id_poezdki, fetchrow=True)


    async def update_manager(self, telegram_id):
        """ Добавляем менеджера   """
        sql = "UPDATE users SET manager = true WHERE telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchrow=True)


    async def update_manager_2(self, telegram_id):
        """    """
        sql = "UPDATE users SET manager = false WHERE telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchrow=True)


    async def add_passangers(self, id_poezdki):
        """    """
        sql = "select passengers from poezdki where id = $1"
        return await self.execute(sql, id_poezdki, fetchval=True)


    async def search_id_user(self, id_poezdki):
        """    """
        sql = "select user_id from poezdki where id = $1"
        return await self.execute(sql, id_poezdki, fetchval=True)

    async def search_telegram_id(self, user_id):
        """    """
        sql = "select telegram_id from users where id = $1"
        return await self.execute(sql, int(user_id), fetchval=True)

    async def search_id_poezdki(self, user_id):
        """    """
        sql = "select id from poezdki where user_id = $1"
        return await self.execute(sql, user_id, fetchval=True)

    async def search_passengers(self, id_poezdki):
        """    """
        sql = "select passengers from poezdki where id = $1"
        return await self.execute(sql, id_poezdki, fetchval=True)

    async def search_nick(self, telegram_id):
        """    """
        sql = "select nick from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)


    async def search_poezdki_full(self, id_poezdki):
        """    """
        sql = "select * from poezdki where id = $1"
        return await self.execute(sql, id_poezdki, fetch=True)


    async def update_mesta2(self, kolvo, id_poezdki):
        """    """
        sql = "UPDATE poezdki SET mesta = mesta + $1  WHERE id = $2"
        return await self.execute(sql, kolvo, id_poezdki, fetchrow=True)


    async def update_phone_user(self, phone, telegram_id):
        """    """
        sql = "UPDATE Users SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, fetchrow=True)


    async def update_avto_user(self, avto, telegram_id):
        """    """
        sql = "UPDATE Users SET avto=$1 WHERE telegram_id=$2"
        return await self.execute(sql, avto, telegram_id, fetchrow=True)

    async def update_staj_user(self, staj, telegram_id):
        """    """
        sql = "UPDATE Users SET staj=$1 WHERE telegram_id=$2"
        return await self.execute(sql, staj, telegram_id, fetchrow=True)

    async def update_count_poezdok(self, telegram_id):
        """    """
        sql = "UPDATE Users SET passenger = passenger + 1 WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)


    async def update_tek_poezdki(self, poezdka, telegram_id):
        """    """
        sql = "UPDATE Users SET poezdka = $1 WHERE telegram_id = $2"
        return await self.execute(sql, int(poezdka), telegram_id, fetchrow=True)


    async def search_ful_poezdki(self, id_poezdki):
        """    """
        sql = "select u.*, p.* from users u left join poezdki p on u.id = p.user_id where p.id = $1"
        return await self.execute(sql, id_poezdki, fetch=True)


    async def update_count_driver(self, telegram_id):
        """    """
        sql = "UPDATE Users SET driver = driver + 1 WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)


    async def search_id_users_poezdki(self, id_poezdki):
        """    """
        sql = "select id from users where poezdka = $1"
        return await self.execute(sql, int(id_poezdki), fetch=True)

    async def update_users_poezdki(self, id_poezdki):
        """    """
        sql = "UPDATE Users SET poezdka = 0 WHERE poezdka = $1"
        return await self.execute(sql, id_poezdki, fetchrow=True)

    async def update_1_users_poezdki(self, telegram_id):
        """    """
        sql = "UPDATE Users SET poezdka = 0 WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def update_count_granica(self, telegram_id):
        """    """
        sql = "UPDATE Users SET count_granica = count_granica + 1 WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def search_usluga_granica(self, ppr: list, usluga: list):
        """Ищем услугу на границе"""
        sql = f'select * from service_granica where name_checkpoint = ANY($1::text[]) and name_service = ANY($2::text[])'
        return await self.execute(sql, ppr, usluga, fetch=True)

    async def poisk_uslug(self):
        """     """
        sql = "SELECT * FROM service_granica"
        return await self.execute(sql, fetch=True)


    async def proverka_uslugi(self, name_service, name_checkpoint, telegram_id):
        """    """
        sql = "select * from service_granica where name_service = $1 and name_checkpoint = $2 and telegram_id = $3"
        return await self.execute(sql, name_service, name_checkpoint, telegram_id, fetch=True)


    async def poisk_moih_uslug(self, telegram_id):
        """     """
        sql = "SELECT * FROM service_granica where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetch=True)


    async def count_uslug(self, telegram_id):
        sql = "SELECT COUNT(*) FROM service_granica where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def delete_uslugi(self, id_uslugi):
        """     """
        sql = "delete from service_granica WHERE id = $1"
        return await self.execute(sql, id_uslugi, fetchrow=True)

    async def update_status_100(self, telegram_id):
        """    """
        sql = "UPDATE Users SET status = '🥉 БРОНЗА' WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def update_status_500(self, telegram_id):
        """    """
        sql = "UPDATE Users SET status = '🥈 СЕРЕБРО' WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)


    async def update_status_1000(self, telegram_id):
        """    """
        sql = "UPDATE Users SET status = '🥇 ЗОЛОТО' WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)





########################################################################################################################
                                           #  Аукцион бот
########################################################################################################################

    async def update_users_lang(self, lang, telegram_id):
        """  Обновляем язык у пользователя  """
        sql = "UPDATE Users SET lang = $1 WHERE telegram_id = $2"
        return await self.execute(sql, lang, telegram_id, fetchrow=True)


    async def select_id_users(self, telegram_id):
        """  Достаем ID пользователя  """
        sql = "select id from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)


    async def select_lang(self, telegram_id):
        """  Проверяем язык пользователя  """
        sql = "select lang from users where telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)


    async def select_last_id_items(self, telegram_id):
        """  Находим последний добавленный аукцион """
        sql = "select id from items where telegram_id = $1 order by id DESC LIMIT 1"
        return await self.execute(sql, int(telegram_id), fetchval=True)


    async def add_item(self, file_id, title, start_price, current_price, bliz_price, telegram_id, time, urls, step_1, step_2, step_3, step_4, step_5, step_6, path, type_file, rules, description):
        """  Добавляем товар на аукцион  """
        sql = "INSERT INTO items (photo, title, start_price, current_price, bliz_price, telegram_id, time, url, step_1, step_2, step_3, step_4, step_5, step_6, path, type_file, rules, description) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18) returning *"
        return await self.execute(sql, file_id, title, int(start_price), int(current_price), int(bliz_price), int(telegram_id), int(time), str(urls), int(step_1), int(step_2), int(step_3), int(step_4), int(step_5), int(step_6), str(path), str(type_file), str(rules), str(description), fetchrow=True)


    async def search_auction(self, url):
        """  Находим активный аукцион  """
        sql = "select * from items where url = $1 and enable = True"
        return await self.execute(sql, str(url), fetch=True)


    async def add_rates(self, telegram_id, id_items, sum):
        """  Добавляем ставку  """
        sql = "INSERT INTO rates (telegram_id, id_items, sum) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, int(telegram_id), int(id_items), int(sum), fetchrow=True)


    async def select_current_price(self, id_auction):
        """  Находим текущую сумму товара  """
        sql = "select current_price from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)



    async def select_name_auction(self, id_auction):
        """  Находим название аукциона  """
        sql = "select title from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def select_bliz_price(self, id_auction):
        """  Уточняем есть ли блиц цена у аукциона  """
        sql = "select bliz_price from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def select_time_auction(self, id_auction):
        """  Находим оставшееся время аукциона  """
        sql = "select time from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def select_description_auction(self, id_auction):
        """  Достаем description товара  """
        sql = "select description from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def count_rates(self, id_auction):
        """  Проверяем сколько ставок уже есть на этот аукцион """
        sql = "SELECT COUNT(*) FROM rates where id_items = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def search_users_in_auction(self, id_auction):
        """  Находим всех кто сделал ставки в этом аукционе  """
        sql = "select r.*, u.first_name from rates r left join users u on r.telegram_id = u.telegram_id where r.id_items = $1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def update_current_price(self, current_price, id_auction):
        """  Обновляем текущую сумму лота  """
        sql = "UPDATE items SET current_price = $1 WHERE id = $2"
        return await self.execute(sql, int(current_price), int(id_auction), fetchrow=True)


    async def search_gold_rates(self, id_auction):
        """  Находим золотую ставку лота  """
        sql = "SELECT r.*, u.first_name  FROM rates r left join users u on r.telegram_id = u.telegram_id where id_items = $1 ORDER BY sum DESC LIMIT 1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def last_user_rates(self, id_items):
        """  Находим последнего проголосовавшего (telegram_id)  """
        sql = "select telegram_id from rates where id_items = $1 ORDER BY sum DESC LIMIT 1"
        return await self.execute(sql, int(id_items), fetchval=True)


    async def search_silver_rates(self, id_auction):
        """  Находим серебряную ставку лота  """
        sql = "SELECT r.*, u.first_name FROM rates r left join users u on r.telegram_id = u.telegram_id where id_items = $1 ORDER BY sum DESC offset 1 LIMIT 1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def close_auction(self, buyer, id_auction):
        """  Закрываем аукцион  """
        sql = "UPDATE items SET buyer = $1, enable = false WHERE id = $2"
        return await self.execute(sql, int(buyer), int(id_auction), fetchrow=True)


    async def search_items_and_vendor(self, id_auction):
        """  Достаем всю информацию о товаре и продавце  """
        sql = "select i.photo, i.title, u.* from items i left join users u on i.telegram_id = u.id where i.id = $1"
        return await self.execute(sql, int(id_auction), fetch=True)



    async def full_name_on_telegram(self, id_auction):
        """  Достаем fullname  """
        sql = "select i.photo, i.title, u.* from items i left join users u on i.telegram_id = u.id where i.id = $1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def search_items_and_rates(self, id_auction):
        """  Достаем информацию по аукциону, ставкам  """
        sql = "select i.photo, i.type_file, i.title, i.imi,r.telegram_id as tel_id_stavka, r.sum, u.telegram_id as vendor, u.username as username_vendor, u.phone from items i right join rates r on i.id = r.id_items left join users u on i.telegram_id = u.id where i.id = $1 order by sum desc limit 1"
        return await self.execute(sql, int(id_auction), fetch=True)



    async def search_items_no_rates(self, id_auction):
        """  Достаем информацию по аукциону где нет ставок  """
        sql = "select i.imi, i.path, i.photo, i.type_file, i.title, i.current_price, u.telegram_id as vendor from items i left join rates r on i.id = r.id_items left join users u on i.telegram_id = u.id where i.id = $1 order by sum desc limit 1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def search_items_and_buyer(self, id_auction):
        """  Достаем всю информацию о товаре и покупателе  """
        sql = "select i.photo, i.title, u.* from items i left join users u on i.buyer = u.id where i.id = $1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def select_telegram_id_vendor(self, id_auction):
        """  Достаем того, Telegram ID кто создал аукцион  """
        sql = "select telegram_id from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def delete_items(self, id_auction):
        """  Удаляем аукцион  """
        sql = "delete from items WHERE id = $1"
        return await self.execute(sql, int(id_auction), fetchrow=True)



    async def delete_rates(self, id_rates):
        """  Удаляем ставку  """
        sql = "delete from rates WHERE id = $1"
        return await self.execute(sql, int(id_rates), fetchrow=True)



    async def search_all_information_from_auction(self, id_auction):
        """  Находим всю информацию об аукционе  """
        sql = "select * from items where id = $1"
        return await self.execute(sql, int(id_auction), fetch=True)


    async def search_all_information_from_rates(self, id_rates):
        """  Находим всю информацию о ставке  """
        sql = "select r.*, u.first_name from rates r left join users u on r.telegram_id = u.telegram_id where r.id = $1"
        return await self.execute(sql, int(id_rates), fetch=True)


    async def select_steps(self, telegram_id):
        """  Выбираем шаги пользователя и правила """
        sql = "select step_1, step_2, step_3, step_4, step_5, step_6, rules from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetch=True)


    async def select_steps_in_item(self, id_auction):
        """  Выбираем шаги у аукциона  """
        sql = "select step_1, step_2, step_3, step_4, step_5, step_6 from items where id = $1"
        return await self.execute(sql, int(id_auction), fetch=True)



    async def select_rules_for_user(self, telegram_id):
        """  Выбираем правила пользователя  """
        sql = "select rules from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetch=True)



    async def update_rules_for_user(self, rules, telegram_id):
        """  Обновляем правила пользователя """
        sql = "UPDATE users SET rules = $1 WHERE telegram_id = $2"
        return await self.execute(sql, str(rules), int(telegram_id), fetchrow=True)




    async def update_items_imi(self, imi, id_auction):
        """  Обновляем imi аукциона """
        sql = "UPDATE items SET imi = $1 WHERE id = $2"
        return await self.execute(sql, str(imi), int(id_auction), fetchrow=True)



    async def select_count_query(self, telegram_id):
        """  Смотрим сколько осталось запросов у пользователя  """
        sql = "select count_query from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchval=True)


    async def minus_count_query(self, telegram_id):
        """  Отнимаем 1 запрос у пользователя  """
        sql = "UPDATE users SET count_query = count_query - 1 WHERE telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchrow=True)


    async def minus_count_and_false(self, id_auction):
        """  Отнимаем 1 минуту и выключаем аукцион  """
        sql = "UPDATE items SET time = 0, enable = false WHERE id = $1"
        return await self.execute(sql, int(id_auction), fetchrow=True)


    async def minus_count_items(self, id_auction):
        """  Отнимаем 1 минуту аукциона  """
        sql = "UPDATE items SET time = time - 1 WHERE id = $1"
        return await self.execute(sql, int(id_auction), fetchrow=True)



    async def select_path(self, id_auction):
        """  Смотрим сколько осталось запросов у пользователя  """
        sql = "select path from items where id = $1"
        return await self.execute(sql, int(id_auction), fetchval=True)


    async def minus_minute_from_items(self):
        """  Отнимаем 1 минуту во всех активных аукционах  """
        sql = "UPDATE items SET time = time - 1 WHERE enable = true"
        return await self.execute(sql, fetchrow=True)


    async def update_count_from_user(self, count_query, telegram_id):
        """  Обновляем количество попыток у пользователя  """
        sql = "UPDATE users SET count_query = $1 WHERE telegram_id = $2"
        return await self.execute(sql, int(count_query), int(telegram_id), fetchrow=True)



    async def add_purchases(self, item, amount, bill_id, description, status, telegram_id):
        """  Добавляем покупку """
        now = datetime.datetime.now()
        sql = "INSERT INTO purchases (item, amount, bill_id, description, datetime, status, telegram_id) VALUES($1, $2, $3, $4, $5, $6, $7) returning *"
        return await self.execute(sql, item, amount, bill_id, description, now, str(status), int(telegram_id), fetchrow=True)



    async def update_steps_from_user(self, step_1, step_2, step_3, step_4, step_5, step_6, telegram_id):
        """  Обновляем шаги у пользователя  """
        sql = "UPDATE users SET step_1 = $1, step_2 = $2, step_3 = $3, step_4 = $4, step_5 = $5, step_6 = $6 WHERE telegram_id = $7"
        return await self.execute(sql, int(step_1), int(step_2), int(step_3), int(step_4), int(step_5), int(step_6), int(telegram_id), fetchrow=True)



    async def update_count_query(self, count_query, telegram_id):
        """  Обновляем количество попыток  """
        sql = "UPDATE users SET count_query = count_query + $1 WHERE telegram_id = $2"
        return await self.execute(sql, int(count_query), int(telegram_id), fetchrow=True)


    async def update_status_purchases(self, status, telegram_id):
        """  Обновляем статус  """
        sql = "UPDATE purchases SET status = $1 WHERE telegram_id = $2"
        return await self.execute(sql, str(status), int(telegram_id), fetchrow=True)


    async def check_admin(self, telegram_id):
        """ Проверяем является ли пользователь администратором"""
        sql = "SELECT * FROM users WHERE telegram_id = $1 AND admin = True"
        return await self.execute(sql, telegram_id, fetch=True)

    async def check_manager(self, telegram_id):
        """ Проверяем является ли пользователь менеджером"""
        sql = "SELECT * FROM users WHERE telegram_id = $1 AND manager = True"
        return await self.execute(sql, telegram_id, fetch=True)


    async def auction_equally_1(self):
        """ Берем аукционы равные 1 """
        sql = "SELECT * FROM items WHERE time = 1"
        return await self.execute(sql, fetch=True)


    async def auction_equally(self):
        """ Берем аукционы равные > 1 """
        sql = "SELECT * FROM items WHERE time > 1 and enable = True"
        return await self.execute(sql, fetch=True)



    async def select_status_auction(self, id_items):
        """  Достаем статус аукциона  """
        sql = "select enable from items where id = $1"
        return await self.execute(sql, int(id_items), fetchval=True)




    async def select_rules_auction(self, id_items):
        """  Достаем информацию аукциона  """
        sql = "select rules from items where id = $1"
        return await self.execute(sql, int(id_items), fetchval=True)


    async def select_username(self, telegram_id):
        """  Достаем username по telegram_id  """
        sql = "select user_name from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchval=True)


    async def select_first_name(self, telegram_id):
        """  Достаем first_name по telegram_id  """
        sql = "select first_name from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchval=True)


    async def select_phone(self, telegram_id):
        """  Достаем телефон по telegram_id  """
        sql = "select phone from users where telegram_id = $1"
        return await self.execute(sql, int(telegram_id), fetchval=True)



    async def search_all_tg(self):
        """    """
        sql = "select * from users"
        return await self.execute(sql, fetch=True)