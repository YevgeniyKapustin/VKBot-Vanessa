from src.services.events import Event
from src.utils.queries import get_commands


def answer_for_custom_msg(event: Event, is_inline: bool):
    data: list = get_commands(event.message.text, is_inline).json()
    if isinstance(data, list) and len(data) >= 1:
        type_ = data[0].get('type')
        command = data[0]
        prefix = 'внутристрочный_' if is_inline else ''
        if type_ == f'{prefix}текст':
            event.text_answer(command.get('response'))
        elif type_ == f'{prefix}текст':
            event.gif_answer(command.get('response'))