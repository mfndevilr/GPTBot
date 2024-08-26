from aiogram import types, F, Router
from aiogram.filters import Command

import keyboard

import sqlite3 as sq3
from secret import MASTER_ID
from aiogram.types import FSInputFile


router = Router()


@router.message(Command('adminpanel'))
async def admin_panel(message: types.Message):
    # Создание базы данных
    db_conn = sq3.connect("data/admin_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT admin_id FROM employees;"
    db_cur.execute(query)
    rows = db_cur.fetchall()
    token_user = []
    for row in rows:
        print(row[0])
        token_user.append(row[0])
    db_cur.close()
    db_conn.close()


    if message.from_user.id == MASTER_ID:
        await message.answer(text=f'Приветствую {message.from_user.full_name} это админ панель! \n',
                             reply_markup=keyboard.admin_menu)
    elif message.from_user.id in token_user:
        await message.answer(text=f'Приветствую {message.from_user.full_name} это админ панель! \n',
                             reply_markup=keyboard.admin_menu)

    else:
        await message.answer(text='У вас недостаточно прав!')


@router.callback_query(F.data == 'add_admin')
async def add_admin(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите ID пользователя')

    @router.message(F.text)
    async def add_user_admin(message: types.Message):
        db_conn = sq3.connect("data/admin_baze.db3")
        db_cur = db_conn.cursor()
        # db_cur.execute("""CREATE TABLE employees (
        # admin_id INTEGER
        # )""")
        db_cur.execute(f"INSERT INTO employees (admin_id) VALUES ({message.text})")
        db_conn.commit()
        db_cur.close()
        db_conn.close()
        await callback.message.answer(text=f'Пользователь с id {message.text} добавлен в администраторы')


@router.callback_query(F.data == 'get_admins')
async def get_admins(callback: types.CallbackQuery):
    # Создание базы данных
    db_conn = sq3.connect("data/admin_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT admin_id FROM employees;"
    db_cur.execute(query)
    rows = db_cur.fetchall()
    token_user = []
    for row in rows:
        print(row[0])
        token_user.append(row[0])
    db_cur.close()
    db_conn.close()
    await callback.message.answer(text=f'Список администраторов:\n{token_user}')

@router.callback_query(F.data == 'add_promocode')
async def add_promocode(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите промокод')

    @router.message(F.text)
    async def add_user_promocode(message: types.Message):
        db_conn = sq3.connect("data/promocode_baze.db3")
        db_cur = db_conn.cursor()
        db_cur.execute("""CREATE TABLE employees (
        promocode TEXT
        )""")
        db_cur.execute(f"INSERT INTO employees (promocode) VALUES ('{message.text}')")
        db_conn.commit()
        db_cur.close()
        db_conn.close()
        await callback.message.answer(text=f'Промокод {message.text} добавлен')

@router.callback_query(F.data == 'get_promocodes')
async def get_promocodes(callback: types.CallbackQuery):
    # Создание базы данных
    db_conn = sq3.connect("data/promocode_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT promocode FROM employees;"
    db_cur.execute(query)
    rows = db_cur.fetchall()
    promocode = []
    for row in rows:
        print(row[0])
        promocode.append(row[0])
    db_cur.close()
    db_conn.close()
    await callback.message.answer(text=f'Список промокодов:\n{promocode}')


@router.callback_query(F.data == 'get_users')
async def get_users(callback: types.CallbackQuery):
    db_conn = sq3.connect("data/user_baze.db3")
    # Создание курсора
    db_cur = db_conn.cursor()
    query = "SELECT id,username FROM employees;"
    db_cur.execute(query)
    rows = db_cur.fetchall()
    token_user = []
    for row in rows:
        token_user.append(row)
    db_conn.commit()
    db_cur.close()
    db_conn.close()
    with open('user.txt', 'w') as file:
        for user_id in token_user:
            file.write(f"{user_id}\n")

    await callback.message.reply_document(FSInputFile('user.txt'))



@router.callback_query(F.data == 'send_notification')
async def send_notification(callback: types.CallbackQuery):
    db_conn = sq3.connect("data/admin_baze.db3")
    db_cur = db_conn.cursor()
    query = "SELECT admin_id FROM employees WHERE admin_id = ?"
    db_cur.execute(query, (callback.from_user.id,))
    admin = db_cur.fetchone()
    db_cur.close()
    db_conn.close()

    if admin:
        await callback.message.answer(text='Введите текст рассылки')

        @router.message(F.content_type.in_({'text', 'photo'}))
        async def send_text(message: types.Message):
            if message.from_user.id == callback.from_user.id:
                db_conn = sq3.connect("data/user_baze.db3")
                db_cur = db_conn.cursor()
                query = "SELECT id FROM employees;"
                db_cur.execute(query)
                rows = db_cur.fetchall()
                for row in rows:
                    user_id = row[0]
                    if message.content_type == 'text':
                        await message.bot.send_message(chat_id=user_id, text=message.text)
                    elif message.content_type == 'photo':
                        await message.bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)
                db_conn.commit()
                db_cur.close()
                db_conn.close()
                await callback.message.answer(text='Рассылка отправлена')
    else:
        await callback.message.answer(text='У вас недостаточно прав!')

@router.callback_query(F.data == 'add_tiket_user')
async def add_tiket_user(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите ID пользователя')

    @router.message(F.text)
    async def add_user_tiket(message: types.Message):
        id_user = message.text
        await callback.message.answer(text=f'Введите количество тикетов')



        @router.message(F.text)
        async def add_user_tikets(msg: types.Message):
            conn = sq3.connect('data/user_baze.db3')
            cur = conn.cursor()
            query = "SELECT * FROM employees WHERE id = ?"
            cur.execute(query, (f'{id_user}',))
            rows = cur.fetchall()
            token_user = []
            for row in rows:
                print(row)
                token_user.append(row[-1])
            cur.execute(
                f"UPDATE employees SET token = '{token_user[0] + int(msg.text)}' WHERE id = '{msg.from_user.id}'")
            conn.commit()
            cur.close()
            conn.close()
            await msg.answer(text=f'Количество тикетов у пользователя {id_user} изменено на {token_user[0] + int(msg.text)}')



from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery




storage = MemoryStorage()


# Группа состояний для отправки сообщений пользователю
class SendMessageStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_message_text = State()


@router.callback_query(F.data == 'send_message_user')
async def send_message_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите ID пользователя')
    await state.set_state(SendMessageStates.waiting_for_user_id)


    @router.message(SendMessageStates.waiting_for_user_id, F.text)
    async def get_user_id(message: types.Message, state: FSMContext):
        await state.update_data(user_id=message.text)
        await message.answer(text='Введите текст сообщения')
        await state.set_state(SendMessageStates.waiting_for_message_text)


        @router.message(SendMessageStates.waiting_for_message_text, F.text)
        async def send_user_text(message: types.Message, state: FSMContext):
            data = await state.get_data()
            user_id = data['user_id']

            await message.bot.send_message(chat_id=user_id, text=f'Ответ от поддержки: {message.text}')
            await message.answer(text='Сообщение отправлено!')
            await state.clear()




