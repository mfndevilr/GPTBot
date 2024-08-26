from aiogram.filters.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram import Router,types,F
import keyboard
import sqlite3 as sq3

router = Router()




storage_1 = MemoryStorage()

# Группа состояний для поддержки
class SupportStatess(StatesGroup):
    waiting_for_message = State()

@router.callback_query(F.data == 'promocode_tiket')
async def promocode_tiket(callback: types.CallbackQuery,  state: FSMContext):
    await callback.message.answer(text='Введите промокод выданный админом')
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
    await state.set_state(SupportStatess.waiting_for_message)


    @router.message(F.text, SupportStates.waiting_for_message)
    async def prom_1(message: types.Message,  state: FSMContext):
        if message.text in promocode:
            conn = sq3.connect('data/user_baze.db3')
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
        await state.clear()

@router.callback_query(F.data == 'pay_tiket')
async def pay_tiket(callback: types.CallbackQuery):
    await callback.message.answer(text='Оплата билета происходит через telegram stars⭐ \n 1 билет🎟 = 0.5 stars⭐',
                                  reply_markup=keyboard.pay_menu)

@router.callback_query(F.data == 'tasks_tiket')
async def tasks_tiket(callback: types.CallbackQuery):
    await callback.message.answer(text='Выполнять задания и зарабатывай билеты 1 задание = 1 билет', reply_markup=keyboard.tasks_menu)


@router.callback_query(F.data == 'invite_tiket')
async def invite_tiket(callback: types.CallbackQuery):
    link = f't.me/gptandpicturebot?start={callback.from_user.id}'
    await callback.message.answer(text=f'Это твоя ссылка для приглашения друзей в канал: \n{link}')



storage = MemoryStorage()

# Группа состояний для поддержки
class SupportStates(StatesGroup):
    waiting_for_message = State()

@router.message(F.text == 'Поддержка🧑‍🔧')
async def get_content(message: types.Message, state: FSMContext):
    await message.answer(text='Введите обращение к поддержке')
    # Устанавливаем состояние ожидания сообщения от пользователя
    await state.set_state(SupportStates.waiting_for_message)

    @router.message(SupportStates.waiting_for_message, F.text)
    async def support_1(msg: types.Message, state: FSMContext):
        await msg.bot.send_message(chat_id='@poderjkabota',
                                   text=f'Пользователь: {msg.from_user.full_name}\n'
                                        f'id: {msg.from_user.id}\n'
                                        f'написал: {msg.text}')
        await msg.answer(text='Обращение отправлено администратору')
        # Сбрасываем состояние
        await state.clear()



