from aiogram import Router,types,F
import keyboard
import sqlite3 as sq3


router = Router()

@router.callback_query(F.data == 'promocode_tiket')
async def promocode_tiket(callback: types.CallbackQuery):
    await callback.message.answer(text='Введите промокод выданный админом')
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

    @router.message(F.text)
    async def prom_1(message: types.Message):
        if message.text in promocode:
            conn = sq3.connect('user_baze.db3')
            cur = conn.cursor()
            query = "SELECT * FROM employees WHERE id = ?"
            cur.execute(query, (f'{message.from_user.id}',))
            rows = cur.fetchall()
            token_user = []
            for row in rows:
                print(row)
                token_user.append(row[-1])
            cur.execute(f"UPDATE employees SET token = '{token_user[0] + 10}' WHERE id = '{message.from_user.id}'")
            conn.commit()
            cur.close()
            conn.close()
            await message.answer(text='Ваш баланс пополнился на 10🎟')
        else:
            await message.answer(text='Неверный промокод')



@router.callback_query(F.data == 'pay_tiket')
async def pay_tiket(callback: types.CallbackQuery):
    await callback.message.answer(text='Оплата билета происходит через telegram stars⭐ \n1 stars⭐ = 1 билет🎟',
                                  reply_markup=keyboard.pay_menu)

@router.callback_query(F.data == 'tasks_tiket')
async def tasks_tiket(callback: types.CallbackQuery):
    await callback.message.answer(text='Выполнять задания и зарабатывай билеты 1 задание = 1 билет', reply_markup=keyboard.tasks_menu)


@router.callback_query(F.data == 'invite_tiket')
async def invite_tiket(callback: types.CallbackQuery):
    link = f't.me/gptandpicturebot?start={callback.from_user.id}'
    await callback.message.answer(text=f'Это твоя ссылка для приглашения друзей в канал: \n{link}')