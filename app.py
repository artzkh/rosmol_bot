from vkbottle import Bot

from blueprints import bps

from config import api, db
from middlewares import EventMiddleware, MessageMiddleware
from states import state_dispenser


def setup_blueprints(bot_: Bot):
    for bp in bps:
        bp.load(bot_)


def setup_middlewares(bot_: Bot):
    bot_.labeler.raw_event_view.register_middleware(EventMiddleware)
    bot_.labeler.message_view.register_middleware(MessageMiddleware)


def init_bot():
    bot_ = Bot(api=api)
    bot_.state_dispenser = state_dispenser
    setup_middlewares(bot_)
    setup_blueprints(bot_)
    return bot_


async def init_db():
    await db.create()
    await db.create_table_users()
    await db.create_table_drones()


bot = init_bot()
bot.loop_wrapper.on_startup.append(init_db())
