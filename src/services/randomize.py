"""Contains various functions that somehow use random."""
from random import randint, choice

from src.utils import vk
from src.utils.actions import send_text, send_file

_vk_admin = vk.get_admin_api()
civilizations = [
    'Россия/Пётр I',
    'Англия/Виктория',
    'Англия/Алиенора Аквитанская',
    'Франция/Екатерина Медичи',
    'Франция/Екатерина Медичи "Великолепная"',
    'Франция/Алиенора Аквитанская',
    'Рим/Траян',
    'Германия/Фридрих I Барбаросса',
    'США/Теодор Рузвельт',
    'США/Теодор Рузвельт "Мужественный всадник"',
    'Индия/Мохандас Карамчад Ганди',
    'Индия/Чандрагупта Маурья',
    'Скифия/Томирис',
    'Греция/Перикл',
    'Греция/Горго',
    'Китай/Цинь Шихуанди',
    'Китай/Хубилай',
    'Египет/Клеопатра VII',
    'Ацтеки/Монтесума I',
    'Бразилия/Педру II',
    'Испания/Филипп II',
    'Япония/Ходзё Токимунэ',
    'Конго/Мвемба а Нзинга',
    'Аравия/Салах ад-Дин',
    'Норвегия/Харальд III Суровый',
    'Шумеры/Гильгамеш',
    'Польша/Ядвига',
    'Австралия/Джон Кэртин',
    'Персия/Кир II Великий',
    'Македония/Александр III Македонский',
    'Нубия/Аманиторе',
    'Индонезия/Трибхувана',
    'Кхмеры/Джайаварман VII',
    'Корея/Сондок',
    'Нидерланды/Вильгельмина',
    'Монголия/Чингисхан',
    'Монголия/Хубилай',
    'Кри/ПаундМейкер',
    'Грузия/Тамара',
    'Шотландия/Роберт I Брюс',
    'Мапуче/Лаутаро',
    'Зулусы/Чака',
    'Венгрия/Матьяш I Корвин',
    'Маори/Купе',
    'Канада/Уилфрид Лорье',
    'Инки/Пачакутек',
    'Мали/Муса I',
    'Швеция/Кристина',
    'Османы/Сулейман I Великолепный',
    'Финикия/Дидона',
    'Майя/Иш-Вак-Чан-Ахав',
    'Великая колумбия/Симон Боливар',
    'Эфиопия/Менелик II',
    'Византия/Василий II',
    'Галлия/Амбиорикс',
    'Вавилон/Хаммурапи',
    'Вьетнам/Чьеу Тхи Чинь',
    'Португалия/Жуан III',
]
zmiys_phrases = [
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
hero_fractions = [
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
    """Send the result from 1 to the number after 'Д'.

    :param chat_id: id of the chat to which the message will be sent
    :param msg: message sent by user
    """
    digital = msg.replace('д', '')
    if digital.isdigit() and digital != '0':
        return send_text(chat_id, f'🎲 {randint(1, int(digital))}')


def send_random_civ_from_civ6(chat_id: int) -> str:
    """Select and sends a random phrase of the good person to the chat.

    :param chat_id: id of the chat to which the message will be sent
    """
    return send_text(chat_id, f'🎲 {choice(civilizations)}')


def send_random_zmiys_phrases(chat_id: int) -> str:
    """Select and sends a random phrase of the good person to the chat.

    :param chat_id: id of the chat to which the message will be sent
    """
    return send_text(chat_id, f'{choice(zmiys_phrases)}')


def send_random_fraction(chat_id: int) -> str:
    """Send a random faction from the herofractions.

    :param chat_id: id of the chat to which the message will be sent
    """
    return send_text(chat_id, f'🎲 {choice(hero_fractions)}')


def send_random_rarity(chat_id: int) -> str:
    """Send random art with rarity.

    :param chat_id: id of the chat to which the message will be sent
    """
    photos = _vk_admin.photos.get(
        owner_id='-41670861',
        album_id='269289093',
        count=1000
    )
    random_choice = str(photos['items'][randint(0, 999)]['id'])
    return send_file(chat_id, f'photo-41670861_{random_choice}')
