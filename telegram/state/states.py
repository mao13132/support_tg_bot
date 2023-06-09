from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from sql.sql_connector import BotDB

from telegram.keyboard.keyboards import Admin_keyb
from telegram.sendler.sendler import Sendler_msg
from telegram.settings.settings import GOOD_SCREEN_MSG, LOGO, ADMIN, ERROR_SCREEN, ERROR_PHONE, GOOD_BONUS, ERROR_SUMM


class States(StatesGroup):
    screen_state = State()

    get_support = State()

    msend = State()

    ad_phone = State()

    ad_token = State()

    set_summ = State()

async def screen_state(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)


    if message.photo == []:
        keyboard = Admin_keyb().cansel()
        await message.reply(ERROR_SCREEN, reply_markup=keyboard)
        return False

    await Sendler_msg().sendler_photo_message(message, LOGO, GOOD_SCREEN_MSG, Admin_keyb().cansel())

    async with state.proxy() as data:
        data['image'] = message.photo[-1].file_id


    await States.ad_phone.set()




async def ad_phone(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)

    phone_number = message.text

    if not phone_number[1:].isdigit():
        keyboard = Admin_keyb().cansel()
        await message.reply(ERROR_PHONE, reply_markup=keyboard)
        return False

    if phone_number[:2] != '+7':
        keyboard = Admin_keyb().cansel()
        await message.reply(ERROR_PHONE, reply_markup=keyboard)
        return False
    if len(phone_number) != 12:
        keyboard = Admin_keyb().cansel()
        await message.reply(ERROR_PHONE, reply_markup=keyboard)
        return False

    await Sendler_msg().sendler_photo_message(message, LOGO, GOOD_BONUS, Admin_keyb().start_keyb())


    image = ''

    async with state.proxy() as data:
        image = data['image']

    admin_text = f'Админка: пользователь прислал скриншот и телефон\n\nID: {message.from_user.id} ' \
                 f'login: {message.from_user.username}\n\n' \
                 f'Телефон: {phone_number}'

    for admin in ADMIN:


        try:
            await message.bot.send_photo(admin, image, caption=admin_text,
                                         reply_markup=Admin_keyb().screen_phone(message.from_user.id, phone_number))
        except Exception as es:
            print(
                f'Критическая ошибка при отправке админу скриншота с подтверждением отзыва и телефона ошибка: {es}')


    await state.finish()


async def get_support(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)

    msg_user = '✅ Ваше обращение принято в работу. В ближайшее время с Вами свяжутся, ожидайте.'

    await message.reply(msg_user)

    admin_text = f'Админка: написал пользователь по кнопке\n\n' \
                 f'ID: {message.from_user.id} login: {message.from_user.username}\n\n' \
                 f'Текст: "{message.text}"'

    for admin in ADMIN:

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

    await state.finish()

async def msend(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)

    async with state.proxy() as data:
        data['msg_client'] = message.text

    good_msg = f'Админка: ОТПРАВКА СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЮ\n\nID:"{data["id_client"]}"\n\n' \
               f'Текст: "{data["msg_client"]}"\n\n' \
               f'⚠️ ПОДТВЕРЖДАЕТЕ?'

    keyb_admin = Admin_keyb().sendler_key()

    try:
        await message.reply(good_msg, reply_markup=keyb_admin)
    except Exception as es:
        print(f'Ошибка админ отправке смс через бота send_msg {es}')

async def ad_token(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)

    token = message.text

    response_add = BotDB.set_token(token)

    if not response_add:
        msg_user = f'⛔️ Ошибка при установке токена.\n\n{token}'
    else:
        msg_user = f'✅ Токен установлен.\n\n{token}'

    await message.reply(msg_user)

    await state.finish()


async def set_summ(message: Message, state: FSMContext):

    await Sendler_msg.log_client_message(message)

    summa_client = message.text

    if not summa_client.isdigit():
        keyboard = Admin_keyb().cansel()
        await message.reply(ERROR_SUMM, reply_markup=keyboard)
        return False

    keyb = ''
    msg = ''

    async with state.proxy() as data:
        data['summa'] = message.text

        keyb = Admin_keyb().approve_pay(data['phone'], data['user_id'], data['summa'])

        msg = f'⚠️ Подтвердите оплату клиенту\n\n' \
              f'ID: {data["user_id"]}\n\n' \
              f'номер: {data["phone"]}\n\n' \
              f'Cумма: {data["summa"]}'

    await Sendler_msg().sendler_photo_message(message, LOGO, msg, keyb)


    await state.finish()

def register_state(dp: Dispatcher):
    dp.register_message_handler(screen_state, state=States.screen_state, content_types=[types.ContentType.ANY])
    dp.register_message_handler(get_support, state=States.get_support, content_types=[types.ContentType.ANY])

    dp.register_message_handler(msend, state=States.msend)

    dp.register_message_handler(ad_phone, state=States.ad_phone)

    dp.register_message_handler(ad_token, state=States.ad_token)

    dp.register_message_handler(set_summ, state=States.set_summ)
