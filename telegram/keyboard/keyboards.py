from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from telegram.settings.settings import KEYB_TEXT1, KEYB_TEXT2, KEYB_TEXT3, KEYB_TEXT4


class Admin_keyb:
    def start_keyb(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT1, callback_data='bonus'))

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT2, callback_data='quest'))


        return self._start_key

    def start_keyb_admin(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT1, callback_data='bonus'))

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT2, callback_data='quest'))

        self._start_key.add(InlineKeyboardButton(text=f'🥝 Установить токен оплаты', callback_data='tokenq'))


        return self._start_key

    def bonus(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT3, callback_data='isend'))

        self._start_key.add(InlineKeyboardButton(text=KEYB_TEXT4, callback_data='back_menu'))


        return self._start_key

    def cansel(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'❌Отмена', callback_data='back-i'))



        return self._start_key

    def back_menu(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'❌Отмена', callback_data='back_menu'))



        return self._start_key

    def client_otvet(self, id_user):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'⌨️ Ответить клиенту', callback_data=f'msend-{id_user}'))

        return self._start_key

    def screen_phone(self, id_user, phone):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'⌨️ Ответить клиенту', callback_data=f'msend-{id_user}'))

        self._start_key.add(InlineKeyboardButton(text=f'💵 Оплатить бонус', callback_data=f'qiwi-{phone[1:]}-{id_user}-100'))

        self._start_key.add(InlineKeyboardButton(text=f'💵 Оплатить бонус', callback_data=f'qiwi-{phone[1:]}-{id_user}-200'))

        self._start_key.add(InlineKeyboardButton(text=f'💵 Оплатить бонус', callback_data=f'qiwi-{phone[1:]}-{id_user}'))

        return self._start_key

    def ower_state(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'❌Отмена', callback_data=f'ower_state'))

        return self._start_key

    def sendler_key(self):
        self._start_key = InlineKeyboardMarkup(row_width=1)

        self._start_key.add(InlineKeyboardButton(text=f'✅ Подтверждаю', callback_data=f'gsen-'))

        self._start_key.add(InlineKeyboardButton(text=f'❌Отмена', callback_data=f'ower_state'))

        return self._start_key

