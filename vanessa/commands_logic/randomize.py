from random import randint

from vanessa.actions import send_text, send_file
from vanessa.connection_to_vk.connection import vk_admin

zmiysphrases = [
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
position = [
    'верх лево',
    'верх право',
    'низ лево',
    'низ право'
]
herofractions = [
    'орден порядка',
    'инферно',
    'лесной союз',
    'некрополис',
    'лига теней',
    'академия волшебства',
    'подгорный народ',
    'великая орда'
]


def send_roll_dice(chat_id: int, msg: str) -> str:
    """sends the result from 1 to the number after 'Д'"""
    dice_command = 'д'
    if msg.replace(dice_command, '').isdigit() and \
            msg.replace(dice_command, '') != '0':
        return send_text(chat_id,
                         f'🎲 {randint(1, int(msg.replace(dice_command, "")))}')


def send_random_zmiysphrases(chat_id: int):
    return send_text(chat_id, f'{zmiysphrases[randint(0, 14)]}')


def send_random_skill_position(chat_id: int):
    return send_text(chat_id, f'🎲 {position[randint(0, 3)]}')


def send_random_fraction(chat_id: int):
    return send_text(chat_id, f'🎲 {herofractions[randint(0, 7)]}')


def send_random_rarity(chat_id: int):
    photos = vk_admin.photos.get(owner_id='-41670861', album_id='269289093',
                                 count=1000)
    random_choice = str(photos['items'][randint(0, 999)]['id'])
    return send_file(chat_id, f'photo-41670861_{random_choice}')
