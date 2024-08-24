from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='ChatGPTBot', callback_data='chatgpt'),
         InlineKeyboardButton(text='Midjorni(не работает)', callback_data='images')]
    ]
)

subscribe_menu = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Перейти в канал', url='https://t.me/prostochatgpt')]]
)


reply_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Профиль💁'), KeyboardButton(text='Главная🏠')],
    [KeyboardButton(text='Получить билеты🏦')]
], resize_keyboard=True)

tiket_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Покупка💳', callback_data='pay_tiket')],
        [InlineKeyboardButton(text='Задания💼', callback_data='tasks_tiket')],
        [InlineKeyboardButton(text='Промокод🏷️', callback_data='promocode_tiket')],
        [InlineKeyboardButton(text='Пригласить друзей👬', callback_data='invite_tiket')]
    ]
)


pay_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='10🎟',callback_data='pay_tiket_10')],
        [InlineKeyboardButton(text='30🎟',callback_data='pay_tiket_30')],
        [InlineKeyboardButton(text='50🎟',callback_data='pay_tiket_50')],
        [InlineKeyboardButton(text='100🎟',callback_data='pay_tiket_100')],
        [InlineKeyboardButton(text='150🎟',callback_data='pay_tiket_150')],
        [InlineKeyboardButton(text='500🎟',callback_data='pay_tiket_500')],
    ]
)


pay_tiket_10 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 10🎟', callback_data='pay_tiket_10_pay')]
    ]
)

pay_tiket_30 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 30🎟', callback_data='pay_tiket_30_pay')]
    ]
)

pay_tiket_50 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 50🎟', callback_data='pay_tiket_50_pay')]
    ]
)
pay_tiket_100 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 100🎟', callback_data='pay_tiket_100_pay')]
    ]
)
pay_tiket_150 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 150🎟', callback_data='pay_tiket_150_pay')]
    ]
)
pay_tiket_500 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Оплатить 500🎟', callback_data='pay_tiket_500_pay')]
    ]
)

admin_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Добавть промокод', callback_data='add_promocode'),
         InlineKeyboardButton(text='Удалить промокод', callback_data='delete_promocode')],
        [InlineKeyboardButton(text='Вывести список промокодов', callback_data='get_promocodes')],
        [InlineKeyboardButton(text='Добавить администратора', callback_data='add_admin'),
         InlineKeyboardButton(text='Удалить администратора', callback_data='delete_admin')],
        [InlineKeyboardButton(text='Вывести список администраторов', callback_data='get_admins')],
        [InlineKeyboardButton(text='Рассылка', callback_data='send_notification'),
         InlineKeyboardButton(text='Cписок пользователей', callback_data='get_users')],
        [InlineKeyboardButton(text='Добавить тикеты юзеру', callback_data='add_tiket_user'),]
    ]
)







tasks_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Заданий пока нет❌', callback_data='no_tasks')]
    ]
)



