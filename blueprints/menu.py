from vkbottle.bot import Message, Blueprint

from config import db
from states import States

bp = Blueprint("main_menu")


@bp.on.private_message(state=None)
async def start_menu(message: Message):
    if await db.check_user(message.peer_id):
        await message.answer('Приветственное сообщение')
        await bp.state_dispenser.set(message.peer_id, States.ACTIVE)
    else:
        await message.answer('Приветственное сообщение')
        await bp.state_dispenser.set(message.peer_id, States.TRAINING)
