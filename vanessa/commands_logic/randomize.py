"""Module for working with random commands"""
from random import randint

from vanessa.actions import Actions
from vanessa.connection import Connection


class RandomCommands:
    """Contains various methods one way or another using random and serving
    for commands
    """
    def __init__(self):
        self.Actions = Actions()
        self.vk_admin = Connection().vk_admin

        self.zmiysphrases = [
            'эно как',
            'тюй блин',
            'понял, спасибо',
            'кто былое помянет у того хрен отвянет',
            'тут не поспоришь',
            'не ну так-то да',
            'ясненько',
            'сбылась мечта',
            'мечта',
            'сбылась мечта идиота',
            'не ну а чо',
            'хап тьфу',
            'ужас',
            'кошмар',
            'не ну такое'
        ]
        self.position = [
            'верх лево',
            'верх право',
            'низ лево',
            'низ право'
        ]
        self.herofractions = [
            'орден порядка',
            'инферно',
            'лесной союз',
            'некрополис',
            'лига теней',
            'академия волшебства',
            'подгорный народ',
            'великая орда'
        ]

    def send_roll_dice(self, chat_id: int, msg: str) -> str:
        """Sends the result from 1 to the number after 'Д'"""
        dice_command = 'д'

        if msg.replace(dice_command, '').isdigit() and \
                msg.replace(dice_command, '') != '0':

            return self.Actions.send_text(
                chat_id,
                f'🎲 {randint(1, int(msg.replace(dice_command, "")))}'
            )

    def send_random_zmiysphrases(self, chat_id: int):
        """Selects and sends a random phrase of the good person to the chat"""
        return self.Actions.send_text(
            chat_id,
            f'{self.zmiysphrases[randint(0, 14)]}'
        )

    def send_random_fraction(self, chat_id: int):
        """Sends a random faction from the herofractions"""
        return self.Actions.send_text(
            chat_id,
            f'🎲 {self.herofractions[randint(0, 7)]}'
        )

    def send_random_rarity(self, chat_id: int):
        """Sends random art with rarity"""
        photos = self.vk_admin.photos.get(
            owner_id='-41670861',
            album_id='269289093',
            count=1000
        )

        random_choice = str(photos['items'][randint(0, 999)]['id'])

        return self.Actions.send_file(
            chat_id,
            f'photo-41670861_{random_choice}'
        )
