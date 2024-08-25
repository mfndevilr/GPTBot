from aiogram.types import LabeledPrice, Message
from aiogram import types, F, Router
from main import bot
import sqlite3 as sq3


router = Router()

@router.callback_query(F.data == 'pay_tiket_10')
async def create_invoice_10(callback: types.CallbackQuery):
    pay_10 = LabeledPrice(label='10🎟', amount=10)
    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 10🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_10],
        start_parameter="one-more",
        payload="10"
    )




@router.callback_query(F.data == 'pay_tiket_30')
async def create_invoice_30(callback: types.CallbackQuery):
    pay_30 = LabeledPrice(label='30🎟', amount=30)

    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 30🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_30],
        start_parameter="one-more",
        payload="30"
    )

@router.callback_query(F.data == 'pay_tiket_50')
async def create_invoice_50(callback: types.CallbackQuery):
    pay_50 = LabeledPrice(label='50🎟', amount=50)

    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 50🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_50],
        start_parameter="one-more",
        payload="50"
    )

@router.callback_query(F.data == 'pay_tiket_100')
async def create_invoice(callback: types.CallbackQuery):
    pay_100 = LabeledPrice(label='100🎟', amount=100)

    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 100🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_100],
        start_parameter="one-more",
        payload="100"
    )

@router.callback_query(F.data == 'pay_tiket_150')
async def create_invoice(callback: types.CallbackQuery):
    pay_150 = LabeledPrice(label='150🎟', amount=150)

    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 150🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_150],
        start_parameter="one-more",
        payload="150"
    )

@router.callback_query(F.data == 'pay_tiket_500')
async def create_invoice(callback: types.CallbackQuery):
    pay_500 = LabeledPrice(label='500🎟', amount=500)

    await bot.send_invoice(
        callback.message.chat.id,
        title="Оплата",
        description="купить 500🎟",
        provider_token="",
        currency="XTR",
        is_flexible=False,
        prices=[pay_500],
        start_parameter="one-more",
        payload="500"
    )


@router.pre_checkout_query()
async def checkout_handler(checkout_query: types.PreCheckoutQuery):
    await checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def star_payment(message: Message):
    # Извлекаем payload из успешного платежа
    payload = message.successful_payment.invoice_payload


    conn = sq3.connect('data/user_baze.db3')
    cur = conn.cursor()
    query = "SELECT * FROM employees WHERE id = ?"
    cur.execute(query, (f'{message.from_user.id}',))
    rows = cur.fetchall()
    token_user = []
    for row in rows:
        print(row)
        token_user.append(row[-1])
    cur.execute(f"UPDATE employees SET token = '{token_user[0] + int(payload)}' WHERE id = '{message.from_user.id}'")
    conn.commit()
    cur.close()
    conn.close()
    await message.answer(text=f'Ваш баланс пополнился на {int(payload)}🎟')


