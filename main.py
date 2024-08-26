import g4f
from g4f.client import Client
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

import keyboard

import sqlite3 as sq3
import hendler
import pay_hendler
import admin_handler
from secret import token
import datetime


bot = Bot(token=token)

dp = Dispatcher()

print('Бот работает✅')

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Создание базы данных
    db_conn = sq3.connect("data/user_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT id FROM employees;"
    db_cur.execute(query)
    rows = db_cur.fetchall()
    token_user = []


    for row in rows:
        token_user.append(row[0])
    db_conn.commit()
    db_cur.close()
    db_conn.close()

    if message.from_user.id in token_user:
        pass
    else:
        refer = message.text[7:]
        conn = sq3.connect('data/user_baze.db3')
        cur = conn.cursor()
        query = "SELECT * FROM employees WHERE id = ?"
        cur.execute(query, (f'{refer}',))
        rows = cur.fetchall()
        token_user = []
        for row in rows:
            print(row)
            token_user.append(row[-1])
        cur.execute(
            f"UPDATE employees SET token = '{token_user[0] + int(5)}' WHERE id = '{refer}'")
        conn.commit()
        cur.close()
        conn.close()

    user_channel_status = await bot.get_chat_member(chat_id='@prostochatgpt', user_id=message.from_user.id)
    if user_channel_status.status != 'left':
        await message.answer(text=f'Привет {message.from_user.full_name} надеюсь тебе понравится бот',
                             reply_markup=keyboard.reply_menu)

        await message.answer_photo(photo='https://img.freepik.com/premium-photo/very-cute-anime-girl-with-big-eyes_670021-7.jpg',
                                   caption='Это бот ChatGPTBot 4o ,а также генератор изображений! \n                   Выбери режим!',
                                   reply_markup=keyboard.start_menu
                                   )

        try:
            # Создание базы данных
            db_conn = sq3.connect("data/user_baze.db3")
            # Создание курсора
            db_cur = db_conn.cursor()

            # Создание таблицы, если она еще не существует
            db_cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER,
                username TEXT,
                token INTEGER,
                UNIQUE(id, username)  -- Уникальное сочетание id и username
            )
            """)

            # Вставка данных
            db_cur.execute(
                f"INSERT OR IGNORE INTO employees (id, username, token) VALUES ({message.from_user.id}, '{message.from_user.username}', {10});")

            # Удаление дубликатов
            db_cur.execute("CREATE TABLE IF NOT EXISTS temp_employees AS SELECT * FROM employees GROUP BY id;")
            db_cur.execute("DELETE FROM employees;")
            db_cur.execute("INSERT INTO employees SELECT * FROM temp_employees;")
            db_cur.execute("DROP TABLE temp_employees;")


            # Фиксация внесенных изменений
            db_conn.commit()

            # Получение всех строк из таблицы
            db_cur.execute("SELECT * FROM employees;")
            result = db_cur.fetchall()

        finally:
            db_cur.close()
            db_conn.close()
    else:
        await message.answer('Чтобы пользоваться ботом, необходимо присоединиться к канал', reply_markup=keyboard.subscribe_menu)


# @dp.inline_query()
# async def handle_inline_query(query: types.InlineQuery):
#     requestgpt = query.query
#     client = Client()
#     response = client.chat.completions.create(
#         # model="gpt-3.5-turbo",
#         model=g4f.models.gpt_4o,
#         messages=[{"role": "user", "content": requestgpt}],
#     )
#     answers_gpt = response.choices[0].message.content
#     results = [
#         types.InlineQueryResultArticle(
#             id='1',
#             title='Выдать результат',
#             input_message_content=types.InputTextMessageContent(message_text='секунду')
#         ),
#     ]
#     await bot.answer_inline_query(query.id, results=results)
#     # await query.answer(answers_gpt)
#     @dp.message(F.text == 'секунду')
#     async def inline_rezult(message: types.Message):
#         await message.answer(text=answers_gpt)

@dp.callback_query(F.data == 'chatgpt')
async def gen_chatgpt(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите свой запрос')

    @dp.message(F.text)
    async def request_gpt(message: types.Message):
        conn = sq3.connect('data/user_baze.db3')
        cur = conn.cursor()
        query = "SELECT * FROM employees WHERE id = ?"
        cur.execute(query, (f'{message.from_user.id}',))
        rows = cur.fetchall()
        token_user = []
        for row in rows:
            token_user.append(row[-1])
        if token_user[0] > 0:
            cur.execute(f"UPDATE employees SET token = '{token_user[0] - 1}' WHERE id = '{message.from_user.id}'")
            conn.commit()
            cur.close()
            conn.close()

            requestgpt = message.text
            await message.answer(text='Подождите, идет генерация...')
            client = Client()
            response = client.chat.completions.create(
                # model="gpt-3.5-turbo",
                model=g4f.models.gpt_4o,
                messages=[{"role": "user", "content": requestgpt}],
            )
            answers_gpt = response.choices[0].message.content
            await message.answer(text=answers_gpt)
        else:
            await message.answer(text='У вас недостаточно билетов. Пополните баланс!')
            conn.commit()
            cur.close()
            conn.close()

@dp.callback_query(F.data == 'images')
async def images(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите запрос изображения')

    @dp.message(F.text)
    async def gen_image(message: types.Message):
        request_gpt = message.text
        client = Client()
        response = client.images.generate(
            model='gemini',
            prompt=request_gpt
        )
        image_url = response.data[0].url
        await message.answer(image_url)

@dp.message(F.text == 'Профиль💁')
async def profil(message: types.Message):
    # Создание базы данных
    db_conn = sq3.connect("data/user_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT * FROM employees WHERE id = ?"
    db_cur.execute(query, (f'{message.from_user.id}',))
    rows = db_cur.fetchall()
    token_user =[]
    for row in rows:
        token_user.append(row[-1])
    db_conn.commit()
    db_cur.close()
    db_conn.close()

    await message.answer(text=f'Это ваш профиль.\n'
                              f'Ник: {message.from_user.full_name}\n'
                              f'ID: {message.from_user.id}\n'
                              f'Количество билетов: {token_user[0]}🎟\n\n'
                              f'Если у вас меньше 3 билетов, вы можите раз в день получить 3 билета ',
                         reply_markup=keyboard.profile_menu)




# Словарь для хранения времени последнего получения билетов пользователями
last_ticket_time = {}


@dp.callback_query(F.data == 'get_tikets')
async def get_tikets_evriday(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_time = datetime.datetime.now()

    if user_id in last_ticket_time:
        time_diff = current_time - last_ticket_time[user_id]
    else:
        time_diff = datetime.timedelta(days=1)  # Если записи нет, разрешить получение билетов

    if time_diff >= datetime.timedelta(days=1):
        conn = sq3.connect('data/user_baze.db3')
        cur = conn.cursor()
        query = "SELECT * FROM employees WHERE id = ?"
        cur.execute(query, (f'{callback.from_user.id}',))
        rows = cur.fetchall()
        token_user = []
        for row in rows:
            token_user.append(row[-1])



        if token_user:
            if token_user[0] < 3:
                cur.execute(f"UPDATE employees SET token = '{token_user[0] + 3}' WHERE id = '{callback.from_user.id}'")
                conn.commit()
                await callback.message.answer(text='Вы успешно получили 3 билета!')
            else:
                await callback.message.answer(text='У вас вас больше 3 билетов. Вы не можете получить больше')
        else:
            await callback.message.answer(text='Ошибка...Проигнорируйте или напишите в поддержку')

        cur.close()
        conn.close()
        last_ticket_time[user_id] = current_time
    else:
        await callback.message.answer(text='Вы уже получали билеты сегодня. Попробуйте снова завтра.')




@dp.message(F.text == 'Главная🏠')
async def glavnoe(message: types.Message):
    await message.answer_photo(
        photo='https://img.freepik.com/premium-photo/very-cute-anime-girl-with-big-eyes_670021-7.jpg',
        caption='Это бот ChatGPTBot 4o ,а также генератор изображений! \n                   Выбери режим!',
        reply_markup=keyboard.start_menu
        )

@dp.message(F.text == 'Получить билеты🏦')
async def work_tickets(message: types.Message):
    await message.answer('Ввыберите способ получения билетов',
                         reply_markup=keyboard.tiket_menu)





async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(hendler.router)
    dp.include_router(pay_hendler.router)
    dp.include_router(admin_handler.router)
    asyncio.run(main())