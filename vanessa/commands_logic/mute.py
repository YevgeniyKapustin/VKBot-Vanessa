"""Module for class mute"""
import json
from os import path

from vk_api import ApiError

from vanessa.actions import Actions
from vanessa.connection import Connection


class Mute:
    """Class for working with mutes and unmutes"""

    def __init__(self):
        self.img_no_power = ''
        self.vk = Connection().vk
        self.actions = Actions()
        self.send_text = self.actions.send_text
        self.send_file = self.actions.send_file

    def shut_up(self, chat_id: int, msg: str, peer_id: int, event):
        """Allows conversation admins to mute a non-admin conversation
        participant
        """
        members = self.__members_search(peer_id, chat_id)

        if self.__member_status_check(event, members):
            victim_id = self.__victim_id_search(msg, event)
            # vanessa can't shut up
            if victim_id == 'ub2121387' or victim_id == '-212138773':
                return self.send_text(chat_id, 'я бы сказала, что это '
                                               'несколько возмутительно')

            found = False

            for member in members['items']:
                # тут бы сделать что-то вроде бинарного поиска, элементов
                # довольно много
                try:
                    if str(member['member_id']) == victim_id:
                        found = True
                        if member['is_admin']:
                            return self.send_file(chat_id, self.img_no_power)
                        break
                except KeyError:
                    pass

            if not found:
                return self.send_text(chat_id, 'жертвы нету в этой беседе')

            elif victim_id in self.get_shut_up_people_list():
                self.send_text(chat_id,
                               f'наш [id{victim_id}|друг] уже отдыхает')
                return f'наш [id{victim_id}|друг] уже отдыхает'

            else:
                self.__supplement_shut_up_people_list(victim_id)
                self.send_text(chat_id,
                               f'наш [id{victim_id}|друг] пока что отдохнет')
                return f'наш [id{victim_id}|друг] пока что отдохнет'

        else:
            return self.send_file(chat_id, self.img_no_power)

    def redemption(self, chat_id, msg, event, peer_id):
        """Allows an admin to remove a member's mute"""
        members = self.__members_search(peer_id, chat_id)
        shut_up_people = self.get_shut_up_people_list()

        if self.__member_status_check(event, members):
            victim_id = self.__victim_id_search(msg, event)
            if victim_id in shut_up_people:
                self.__remove_from_shut_up_people_list(victim_id)
                self.send_text(
                    chat_id,
                    f'[id{victim_id}|друг], ты свободен, наслаждайся жизнью и '
                    'хорошего тебе дня'
                )
                return f'[id{victim_id}|друг], ты свободен, наслаждайся ' \
                       f'жизнью и хорошего тебе дня'
            else:
                self.send_text(chat_id, 'да не то чтобы он сильно замучен')
                return 'да не то чтобы он сильно замучен'
        else:
            self.send_file(chat_id, self.img_no_power)

    @staticmethod
    def get_shut_up_people_list():
        if not path.isfile('shut_up_people.json'):
            with open('shut_up_people.json', 'w') as f:
                json.dump([], f, indent=4)

        with open('shut_up_people.json', 'r') as f:
            shut_up_people = json.load(f)

        return shut_up_people

    def __supplement_shut_up_people_list(self, victim_id):
        shut_up_people = self.get_shut_up_people_list()
        shut_up_people.append(victim_id)

        return self.__dump_shut_up_people(shut_up_people)

    def __remove_from_shut_up_people_list(self, victim_id):
        shut_up_people = self.get_shut_up_people_list()
        shut_up_people.remove(victim_id)

        return self.__dump_shut_up_people(shut_up_people)

    def __victim_id_search(self, msg, event):
        if 'раз' in msg:
            msg = msg.replace('раз', '')
        msg = msg.replace('мут', '')
        if msg == '' and 'reply_message' in event.object.message:
            victim_id = str(event.object.message['reply_message']['from_id'])
        else:
            victim_id = self.__id_definition_by_mention(msg)

        return victim_id

    @staticmethod
    def __dump_shut_up_people(shut_up_people):
        with open('shut_up_people.json', 'w') as f:
            json.dump(shut_up_people, f, indent=4)

        return shut_up_people

    @staticmethod
    def __member_status_check(event, members) -> bool:
        """Returns true if the requester is an administrator"""
        from_admin = False
        member_id = event.object.message['from_id']

        for member in members['items']:
            try:
                if member['member_id'] == member_id and member['is_admin']:
                    from_admin = True
                    return from_admin
            except KeyError:
                pass

        return from_admin

    def __members_search(self, peer_id, chat_id):
        """Return object members or send about error"""
        try:
            return self.vk.messages.getConversationMembers(peer_id=peer_id)

        except ApiError:
            return self.send_text(chat_id, 'ну знаете, могли бы админку чтоле '
                                           'дать для начала')

    @staticmethod
    def __id_definition_by_mention(mention):
        """Cut id from mention"""
        return mention.strip()[3:12]
