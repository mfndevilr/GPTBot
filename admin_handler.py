from aiogram import types, F, Router
from aiogram.filters import Command

import keyboard

import sqlite3 as sq3
from secret import MASTER_ID


router = Router()




@router.message(Command('adminpanel'))
async def admin_panel(message: types.Message):
    # Создание базы данных
    db_conn = sq3.connect("admin_baze.db3")
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
        db_conn = sq3.connect("admin_baze.db3")
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
    db_conn = sq3.connect("admin_baze.db3")
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
        db_conn = sq3.connect("promocode_baze.db3")
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
    db_conn = sq3.connect("promocode_baze.db3")
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
    db_conn = sq3.connect("user_baze.db3")
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
    with open('user.txt', 'w') as file:
        for user_id in token_user:
            file.write(f"{user_id}\n")

    await callback.message.answer_document(document='user.txt', caption='Список пользователей')

