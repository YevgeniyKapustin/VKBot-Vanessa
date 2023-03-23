from vk_api import ApiError

from basic_actions.actions import send_text, send_file
from basic_actions.database import DataBase
from prepare.connection import Connection


class Mute(object):
    """Class for working with mutes and unmutes"""

    def __init__(self):
        self.img_no_power = ''
        self.vk = Connection().vk
        self.db = DataBase()

    def shut_up(self, chat_id: int, msg: str, peer_id: int, event):
        """Allows conversation admins to mute a non-admin conversation
        participant
        """
        members = self.__members_search(peer_id, chat_id)

        if self.__member_status_check(event, members):
            victim_id = self.__victim_id_search(msg, event)
            # vanessa can't shut up
            if victim_id == 'ub2121387' or victim_id == '-212138773':
                return send_text(chat_id, 'я бы сказала, что это '
                                          'несколько возмутительно')

            found = False

            for member in members['items']:
                try:
                    if str(member['member_id']) == victim_id:
                        found = True
                        if member['is_admin']:
                            return send_file(chat_id, self.img_no_power)
                        break
                except KeyError:
                    pass

            if not found:
                return send_text(chat_id, 'жертвы нету в этой беседе')

            elif victim_id == self.db.get_shut_up_person(victim_id):
                send_text(chat_id,
                          f'наш [id{victim_id}|друг] уже отдыхает')
                return f'наш [id{victim_id}|друг] уже отдыхает'

            else:
                self.db.set_shut_up_person(victim_id)
                send_text(chat_id,
                          f'наш [id{victim_id}|друг] пока что отдохнет')
                return f'наш [id{victim_id}|друг] пока что отдохнет'

        else:
            return send_file(chat_id, self.img_no_power)

    def redemption(self, chat_id, msg, event, peer_id):
        """Allows an admin to remove a member's mute"""
        members = self.__members_search(peer_id, chat_id)

        if self.__member_status_check(event, members):
            victim_id = self.__victim_id_search(msg, event)
            if int(victim_id) == self.db.get_shut_up_person(victim_id)[0]:
                self.db.remove_from_shut_up_people(victim_id)
                return send_text(
                    chat_id,
                    f'[id{victim_id}|друг], ты свободен, наслаждайся жизнью и '
                    'хорошего тебе дня'
                )
            else:
                return send_text(chat_id, 'да не то чтобы он сильно замучен')
        else:
            send_file(chat_id, self.img_no_power)

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
            return send_text(chat_id, 'ну знаете, могли бы админку чтоле '
                                      'дать для начала')

    @staticmethod
    def __id_definition_by_mention(mention):
        """Cut id from mention"""
        return mention.strip()[3:12]
