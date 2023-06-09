from datetime import datetime

from telegram.bot_core import BotDB

from telegram.settings.settings import ADMIN


class OneVisit:
    async def one_visit(self, message):
        self._time_msg = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if (not BotDB.user_exist(message.from_user.id)):

            self.msg = (
                f'{self._time_msg} Новый пользователь: '
                f'"/Anketa_{message.from_user.id}" "{message.from_user.mention}" добавил в DB')

            print(self.msg)

            BotDB.add_user(message.from_user.id, message.from_user.username,
                           message.from_user.full_name, message.from_user.mention, 'new', self._time_msg)

            for admin in ADMIN:
                try:
                    await message.bot.send_message(admin,
                                                   f'Админка: Новый пользователь "/Anketa_{message.from_user.id}" "{message.chat.mention}" добавил в DB',
                                                   disable_notification=True)
                except Exception as es:
                    print(f'Не могу отправить сообщение админу о новом пользователе "{es}"')

            return True

        else:
            BotDB.change_time(message.from_user.id, self._time_msg)
            return False
