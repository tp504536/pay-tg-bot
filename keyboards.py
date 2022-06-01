from aiogram import types

user_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
key = types.KeyboardButton(text='Купить подписку💰')
key2 = types.KeyboardButton(text='Статус подписки📄')
key3 = types.KeyboardButton(text='О проекте👨‍💻')
user_menu.add(key).add(key2).add(key3)

admin_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
ad_key = types.KeyboardButton(text='Заявки')
ad_key2 = types.KeyboardButton(text='Статистика')
ad_key3 = types.KeyboardButton(text='Рассылка')
admin_menu.add(ad_key).add(ad_key2).add(ad_key3)

in_buy = types.InlineKeyboardMarkup()
buy = types.InlineKeyboardButton(text='Купить', callback_data='sub')
back = types.InlineKeyboardButton(text='Отмена', callback_data='back')
in_buy.add(buy).add(back)

sms = types.InlineKeyboardMarkup(row_width=1)
all = types.InlineKeyboardButton(text='Всем пользователям', callback_data='all_user')
sub = types.InlineKeyboardButton(text='Подписчикам', callback_data='sub_user')
sms.add(all).add(sub).add(back)

send_msg = types.InlineKeyboardMarkup(row_width=1)
all_msg = types.InlineKeyboardButton(text='Отправить', callback_data='send')
send_msg.add(all_msg).add(back)

send_sub_msg = types.InlineKeyboardMarkup(row_width=1)
sub_msg = types.InlineKeyboardButton(text='Отправить подписчикам', callback_data='send_sub')
send_sub_msg.add(sub_msg).add(back)

ok = types.InlineKeyboardMarkup(row_width=1)
yes = types.InlineKeyboardButton(text='Подтвердить', callback_data='yes')
no = types.InlineKeyboardButton(text='Отказать', callback_data='no')
ok.add(yes).add(no)
