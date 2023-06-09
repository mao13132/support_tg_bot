from aiogram import Dispatcher, types

from payments.paiments import Paiments
from telegram.sendler.sendler import *

from telegram.keyboard.keyboards import *
from telegram.state.states import States

from sql.sql_connector import BotDB


async def bonus(call: types.CallbackQuery):

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().bonus()

    await Sendler_msg.send_msg_call(call, BONUS_MESSAGE, keyb)



async def back_menu(call: types.CallbackQuery, state: FSMContext):

    await state.finish()

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().start_keyb()

    if str(call.from_user.id) in ADMIN:
        keyb = Admin_keyb().start_keyb_admin()

    await Sendler_msg.send_msg_call(call, START_MESSAGE, keyb)


async def isend(call: types.CallbackQuery):

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().cansel()

    await Sendler_msg().sendler_photo_call(call, SCREEN, SCREEN_MSG, keyb)

    await States.screen_state.set()


async def back_i(call: types.CallbackQuery, state: FSMContext):

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().bonus()

    await Sendler_msg().sendler_photo_call(call, LOGO, BONUS_MESSAGE, keyb)

    await state.finish()


async def quest(call: types.CallbackQuery, state: FSMContext):

    await Sendler_msg.log_client_call(call)

    keyb = Admin_keyb().back_menu()

    await Sendler_msg().sendler_photo_call(call, LOGO, QUEST_MSG, keyb)

    await States.get_support.set()


async def ower_state(call: types.CallbackQuery, state: FSMContext):
    await Sendler_msg.log_client_call(call)

    await state.finish()

async def msend(call: types.CallbackQuery, state: FSMContext):

    await Sendler_msg.log_client_call(call)

    try:
        _, id_tg = str(call.data).split('-')
        if id_tg == '':
            await call.answer(f'Устаревшая кнопка', show_alert=True)
            return False
    except:
        print(f'Ошибка при разборе msend')
        return False

    async with state.proxy() as data:
        data['id_client'] = id_tg

    admin_text = (f'Пришлите мне следующим сообщением текст обращения к клиенту и я перешлю его ему!')

    keyboard = Admin_keyb().ower_state()

    try:
        await call.message.reply(admin_text, reply_markup=keyboard)

    except Exception as es:
        print(f'Ошибка отправки сообщение о msend "{es}"')


    await States.msend.set()

async def gsen(call: types.CallbackQuery, state: FSMContext):

    await Sendler_msg.log_client_call(call)

    async with state.proxy() as data:
        pass

    try:
        await call.message.bot.send_message(int(data['id_client']), data["msg_client"])
        await call.message.reply(f'✅ Сообщение успешно отправленно')
        # await call.message.delete()


    except Exception as es:

        await call.answer(f'Ошибка при отправки сообщения клиенту', show_alert=True)
        print(f'Ошибка при отправки сообщения клиенту {es}')

    await state.finish()

async def tokenq(call: types.CallbackQuery):

    await Sendler_msg.log_client_call(call)

    admin_text = (f'Пришлите мне токен и я его установлю')

    keyboard = Admin_keyb().ower_state()

    try:
        await call.message.reply(admin_text, reply_markup=keyboard)

    except Exception as es:
        print(f'Ошибка отправки сообщение о ad_token "{es}"')

    await States.ad_token.set()


async def qiwi(call: types.CallbackQuery):

    await Sendler_msg.log_client_call(call)

    if not str(call.from_user.id) in ADMIN:
        await call.message.reply(f'Ошибка доступа')
        return False

    try:
        _, phone, user_id, SUMMA = str(call.data).split('-')

    except:
        print(f'Ошибка при разборе qiwi')
        return False




    api_access_token = BotDB.get_token()

    if api_access_token == []:
        await call.message.reply(f'⚠️🥝 Не установлен токен QIWI')
        return False

    # api_access_token = 'cbd80a132bcc2252caa5c3a88fa18ce9'

    qiwi_core = Paiments(api_access_token, phone, SUMMA)

    operator_data = qiwi_core.qiwi_com_search_mobile()

    if not operator_data:
        await call.message.reply(f'⛔️ Ошибка токена обновите токен QIWI')
        return False

    operator_name = operator_data[0]['shortName']
    operator_code = operator_data[0]['id']

    await call.message.reply(f'♻️ Начал оплату {SUMMA} рублей на номер +{phone} оператор: {operator_name}')

    response_payments = qiwi_core.send_mobile(operator_code)

    try:
        response_payments = response_payments['transaction']['state']['code']
        if response_payments == 'Accepted':

            msg = f'✅ Оплатил {SUMMA} рублей на номер +{phone} оператор: {operator_name}'


            msg_client = f'✅ Номер указанного Вами телефона успешно пополнен на {SUMMA} рублей.' \
                         f'Спасибо, что обратились в нашу службу поддержки клиентов!'

            with open(BONUS, 'rb') as file:
                user_msg = await call.message.bot.send_photo(user_id, file,  msg_client)

            try:
                await call.bot.pin_chat_message(chat_id=user_id,
                                                    message_id=user_msg['message_id'])
            except:
                pass


        else:
            msg = f'⛔️ Ошибка при оплате {SUMMA} рублей на номер +{phone} оператор: {operator_name}'
    except Exception as es:
        msg = f'⛔️ Ошибка при оплате {SUMMA} рублей на номер +{phone} оператор: {operator_name} "{es}"'



    await call.message.reply(msg)

async def pay(call: types.CallbackQuery, state: FSMContext):

    await Sendler_msg.log_client_call(call)

    if not str(call.from_user.id) in ADMIN:
        await call.message.reply(f'Ошибка доступа')
        return False

    try:
        _, phone, user_id, summa = str(call.data).split('-')

    except:
        print(f'Ошибка при разборе pay')
        return False

    if summa == 'set':
        msg = '🤲 Пришлите следующим сообщением сумму которые необходимо оплатить клиенту'
        await call.message.reply(msg)

        await States.set_summ.set()

        async with state.proxy() as data:
            data['phone'] = phone
            data['user_id'] = user_id






def register_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(bonus, text_contains='bonus')
    dp.register_callback_query_handler(back_menu, text_contains='back_menu', state='*')

    dp.register_callback_query_handler(isend, text_contains='isend')
    dp.register_callback_query_handler(back_i, text_contains='back-i', state='*')


    dp.register_callback_query_handler(quest, text_contains='quest')
    dp.register_callback_query_handler(ower_state, text_contains='ower_state')

    dp.register_callback_query_handler(msend, text_contains='msend-')
    dp.register_callback_query_handler(gsen, text_contains='gsen-', state='*')

    dp.register_callback_query_handler(qiwi, text_contains='qiwi-', state='*')

    dp.register_callback_query_handler(tokenq, text_contains='tokenq')

    dp.register_callback_query_handler(pay, text_contains='pay-', state='*')
