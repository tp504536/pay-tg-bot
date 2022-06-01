import re
import time
from datetime import datetime, timedelta

import aiocron
from aiogram import Bot, Dispatcher, executor
import logging

from aiogram.utils.exceptions import ChatNotFound

from keyboards import *
from database import User
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

storage = MemoryStorage()
db = User('user.db')
bot = Bot(token="1926597228:AAH7_6Ymsqc_EWLohGphyi9jTOEeWE84tZg")
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)


class FSMall_user(StatesGroup):
    sms = State()


class FSMsub_user(StatesGroup):
    sub_buy = State()


class FSMall_sub_user(StatesGroup):
    sub_all = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    admin_id = 1912165183
    if message.from_user.id == admin_id:
        await message.answer('Привет, давай приступим к работе.', reply_markup=admin_menu)
    else:
        await message.answer('hello', reply_markup=user_menu)
        if not db.all_user(message.from_user.id):
            db.add_user(message.from_user.id)


@dp.message_handler(content_types='text')
async def amin_menu(message: types.Message):
    admin_id = 1912165183
    if message.from_user.id == admin_id:
        if message.text == 'Заявки':
            if len(db.photo_sub()):
                for i in db.photo_sub():
                    global img, user_id
                    img = i[1]
                    user_id = i[0]
                    count = len(db.lenrec())
                    print(i[1])
                    await bot.send_photo(message.from_user.id, i[1], i[0], reply_markup=ok)
                    await message.answer('Неразобранных заявок: ' + str(count))
            else:
                await message.answer('Заявок больше нет')
        elif message.text == 'Статистика':
            user_all = (db.lenuser())
            sub_all = (db.len_sub_user())
            await message.answer(
                'Количесвто пользоватлей заходивших в бота:\n ' + str(
                    user_all) + '\nКоличесвто активных подписок:\n' + str(sub_all))
        elif message.text == 'Рассылка':
            await message.answer(
                'Выбери категорию!\nНЕ ЗАБЫВАЙ, ЧТО У ТЕЛЕГРАМА ЕСТЬ ЛИМИТ\nПосле окончание рассылки тебе придет отчет!',
                reply_markup=sms)
        else:
            await message.answer('Пожалуйста используй только клавиатуру!')
    if message.text == 'Купить подписку💰':
        await message.answer('Текст о подписке', reply_markup=in_buy)
    elif message.text == 'Статус подписки📄':
        status = (re.sub(r"[',(),\]\[]", '', str(db.status_sub(message.from_user.id))))
        print(status)
        await message.answer(
            'Подписка действительна до: ' + str(status) + '\nЗа 2 дня до конца попдписки придет напоминание ')
    elif message.text == 'О проекте👨‍💻':
        await message.answer('Текст')
    else:
        if message.from_user.id != admin_id:
            await message.answer('Уважаемый пользователь используй только клавиатуру!!')


@dp.message_handler(content_types='text', state=FSMall_user.sms)
async def msg(message: types.Message, state: FSMContext):
    global data
    async with state.proxy() as data:
        data['text'] = message.text
        await state.finish()
        await message.answer('Текс для рассылки: ' + data['text'] + '\nДля отправки нажми кнопку',
                             reply_markup=send_msg)


@dp.message_handler(content_types='text', state=FSMall_sub_user.sub_all)
async def msg(message: types.Message, state: FSMContext):
    global data_sub
    async with state.proxy() as data_sub:
        data_sub['text'] = message.text
        await state.finish()
        await message.answer('Текс для рассылки: ' + data_sub['text'] + '\nДля отправки нажми кнопку',
                             reply_markup=send_sub_msg)


@dp.message_handler(content_types='photo', state=FSMsub_user.sub_buy)
async def sub(message: types.Message, state: FSMContext):
    global sub
    async with state.proxy() as sub:
        sub['photo'] = message.photo
        await state.finish()
        photo_id = message.photo[-1].file_id
        if not db.buy_user_check(message.from_user.id):
            await message.answer('Вы отправили скрин оплаты, ожидайте подтверждения! ', )
            db.add_sub(message.from_user.id, photo_id)
            await bot.send_message(1912165183, 'У вас новая заявка')
        else:
            await message.answer('Вы уже отправляли скрин, ждите подтверждения менеджера')


@dp.callback_query_handler(text='sub')
async def send_buy(call: types.CallbackQuery):
    main_menu = types.InlineKeyboardMarkup(row_width=1)
    main_menu.add(back)
    await call.message.answer('Отправь скрин оплаты', reply_markup=main_menu)
    await FSMsub_user.sub_buy.set()
    if not FSMsub_user.sub_buy:
        print('a')


@dp.callback_query_handler(text='back')
async def back_menu(call: types.CallbackQuery):
    await call.message.answer('Вы вернулись в главное меню')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(text='all_user')
async def back_menu(call: types.CallbackQuery):
    await call.message.answer('Напишите текст для рассылки\nДопустил ошибку позже бдует кнопка отмены))')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await FSMall_user.sms.set()


@dp.callback_query_handler(text='no')
async def no(call: types.CallbackQuery):
    await call.message.answer('Вы не подтвердили оплату, пользователю придет ссылка на чат с вами))')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await bot.send_message(user_id, 'Ваша оплата не прошла')
    db.del_sub(img)


@dp.callback_query_handler(text='yes')
async def yes(call: types.CallbackQuery):
    await call.message.answer(
        'Вы подтвердили оплату, пользователю придет ссылка на канал. Срок действия ссылки 24 часа ))')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    my_chat = -1001268450666
    expire_date = datetime.now() + timedelta(days=1)
    link = await bot.create_chat_invite_link(my_chat, expire_date, 1)
    inline = types.InlineKeyboardMarkup()
    url_btn = types.InlineKeyboardButton(text='Ссылка на канал', url=link.invite_link)
    inline.add(url_btn)
    await bot.send_message(user_id, 'Ваша оплата подтверждена! Ссылка действительна 24 часа', reply_markup=inline)
    db.del_sub(img)
    if not db.all_subuser(user_id):
        db.add_subuser(user_id)
    else:
        db.update_subusers(user_id)


@dp.callback_query_handler(text='sub_user')
async def back_menu(call: types.CallbackQuery):
    await call.message.answer('Напишите текст для рассылки\n Допустил ошибку позже бдует кнопка отмены))')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await FSMall_sub_user.sub_all.set()


@dp.callback_query_handler(text='send')
async def back_menu(call: types.CallbackQuery):
    await call.message.answer('Отпрвка сообщений началась')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    err = 0
    okk = 0
    for c in db.id_user():
        try:
            id_us = (re.sub(r"[',()]", '', str(c)))
            time.sleep(1)
            await bot.send_message(id_us, data['text'])
            okk += 1
            f = open('send.txt', "w+")
            f.write(str(okk))
            f.close()
            a = open('send.txt')
            b = a.read()
            a.close()
        except ChatNotFound:
            err += 1
            e = open('error.txt', 'w+')
            e.write(str(err))
            e.close()
            er = open('error.txt')
            g = er.read()
            er.close()
    await call.message.answer(
        'Рассылка закончилась:\nОтправлено: ' + b + ' subscriber' '\nПокинули бота: ' + g + ' subscriber')


@dp.callback_query_handler(text='send_sub')
async def back_menu(call: types.CallbackQuery):
    await call.message.answer('Отпрвка сообщений началась')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    for c in db.id_sub_user():
        try:
            id_us = (re.sub(r"[',()]", '', str(c)))
            time.sleep(1)
            await bot.send_message(id_us, data_sub['text'])
        except ChatNotFound:
            pass
    await call.message.answer('Рассылка закончилась:')


@aiocron.crontab('30 11  * * *')
async def days():
    for i in db.two_day():
        try:
            day_user = (re.sub(r"[',()]", '', str(i)))
            time.sleep(3)
            await bot.send_message(day_user, 'Осталось  2 дня пописки')
        except ChatNotFound:
            pass


@aiocron.crontab('30 12 * * *')
async def kick_sving():
    for kik in db.all_finish():
        chat = -1001268450666
        try:
            time.sleep(3)
            unsub_id = (re.sub(r"[',()]", '', str(kik)))
            await bot.kick_chat_member(chat_id=chat, user_id=int(unsub_id))
        except ChatNotFound:
            pass


@aiocron.crontab('30 13 * * *')
async def del_black_list():
    for unban in db.all_finish():
        chat = -1001268450666
        try:
            time.sleep(3)
            unsub_id = (re.sub(r"[',()]", '', str(unban)))
            await bot.unban_chat_member(chat_id=chat, user_id=int(unsub_id))
        except ChatNotFound:
            pass


@aiocron.crontab('0 17 * * *')
async def days():
    for i in db.del_day_sub():
        print(i)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
