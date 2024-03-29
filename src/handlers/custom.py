from requests import Response

from src.rules.rules import Any, Text, Prefix
from src.services.commads_list import update_command_list
from src.services.events import Event
from src.services.schemas import Command
from src.services.custom_commands import (
    answer_for_custom_msg, create_command_obj, get_command_id
)
from src.utils.decorators import handle_message
from src.utils.queries import create_command, delete_command
from src.utils.status_cods import OK_200, CREATE_201, NOT_FOUND_404


@handle_message(Text('команды'))
def handler_get_commands(event: Event):
    event.text_answer('https://vk.com/topic-212138773_49520072')


@handle_message(Any())
def handler_any_message(event: Event):
    answer_for_custom_msg(event, False)


@handle_message(Any())
def handler_any_message_inline(event: Event):
    answer_for_custom_msg(event, True)


@handle_message(Prefix('добавить команду '))
def handler_add_command(event: Event):
    command: Command = create_command_obj(event)
    query_response: Response = create_command(
        request=command.request,
        response=command.response,
        type_=command.type
    )
    if query_response.status_code == OK_200:
        event.text_answer(f'Команда "{command.request}" уже существует')
    elif query_response.status_code == CREATE_201:
        event.text_answer(f'Команда "{command.request}" создана')
        update_command_list()


@handle_message(Prefix('удалить команду'))
def handler_delete_command(event: Event):
    request: str = event.message.text.replace('удалить команду', '').strip()
    query_response: Response = delete_command(id_=get_command_id(request))
    if query_response.status_code == OK_200:
        event.text_answer(f'Команда "{request}" удалена')
        update_command_list()
    elif query_response.status_code == NOT_FOUND_404:
        event.text_answer(f'Команда "{request}" не существует')
