from aiogram.types import Message

from aiogram import Dispatcher, types

from telegram.keyboard.keyboards import Admin_keyb
from telegram.one_visit import OneVisit
from telegram.sendler.sendler import Sendler_msg

from telegram.settings.settings import START_MESSAGE, LOGO, NO_TEXT, ADMIN

"""@mao1312"""


async def start(message: Message):
    await Sendler_msg.log_client_message(message)

    new_user = await OneVisit().one_visit(message)

    keyb = Admin_keyb().start_keyb()

    if str(message.from_user.id) in ADMIN:
        keyb = Admin_keyb().start_keyb_admin()

    await Sendler_msg().sendler_photo_message(message, LOGO, START_MESSAGE, keyb)


async def no_text(message: Message):
    await Sendler_msg.log_client_message(message)

    admin_text = f'Админка: написал пользователь без кнопки\n\n' \
                 f'ID: {message.from_user.id} login: {message.from_user.username}\n\n'

    for admin in ADMIN:
        admin = int(admin)

        if message.photo != []:

            try:
                await message.bot.send_photo(admin, message.photo[-1].file_id, caption=f'{admin_text}'
                                                                                       f'текст: {message.caption}',
                                             reply_markup=Admin_keyb().client_otvet(message.from_user.id))
            except Exception as es:
                print(
                    f'Критическая ошибка при отправке админу скриншота с подтверждением оплаты ошибка: {es}')

        if message.document is not None:
            try:
                await message.bot.send_document(admin,
                                                document=message.document.file_id,
                                                caption=f'{admin_text} текст: {message.caption}',
                                                reply_markup=Admin_keyb().client_otvet(message.from_user.id))
            except Exception as es:
                print(
                    f'Критическая ошибка при отправке админу скриншота с подтверждением оплаты ошибка: {es}')

        if message.video is not None:
            try:
                await message.bot.send_video(admin,
                                             video=message.video.file_id,
                                             caption=f'{admin_text} текст: {message.caption}',
                                             reply_markup=Admin_keyb().client_otvet(message.from_user.id))
            except Exception as es:
                print(
                    f'Критическая ошибка при отправке админу видео: {es}')

        if message.photo == [] and message.document is None and message.video is None:

            try:
                await message.bot.send_message(admin, f'{admin_text} текст: {message.text}',
                                               reply_markup=Admin_keyb().client_otvet(message.from_user.id))
            except Exception as es:
                print(
                    f'Критическая ошибка при переадресации сообщения пользователя: {es}')


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, text_contains='/start')
    dp.register_message_handler(no_text, text_contains='', content_types=[types.ContentType.ANY])
