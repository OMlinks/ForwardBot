import sys
from logging import DEBUG, WARNING, basicConfig, getLogger, INFO
import os

from telethon import TelegramClient
from distutils.util import strtobool as sb
from telethon import events
from telethon.sessions import StringSession
ENV = True

if ENV:
    from forwardbot.BotConfig import Config
else:
    from local_config import Development as Config

bot = TelegramClient('bot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)

client = TelegramClient(StringSession(Config.STRING_SESSION), Config.API_ID, Config.API_HASH)

if bool(ENV):
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
            level=DEBUG,
        )
    else:
        basicConfig(
            format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO
        )
    logger = getLogger(__name__)

if Config.API_ID is None:
    logger.info("API_ID is None. Bot Is Quiting")
    sys.exit(1)
if Config.API_HASH is None:
    logger.info("API_HASH is None. Bot Is Quiting")
    sys.exit(1)
if Config.BOT_TOKEN is None:
    logger.info("BOT_TOKEN is None. Bot Is Quiting")
    sys.exit(1)
if Config.STRING_SESSION is None:
    logger.info("STRING_SESSION is None. Bot Is Quiting")
    sys.exit(1)
if Config.SUDO_USERS is None:
    logger.info("STRING_SESSION is None. Bot Is Quiting")
    sys.exit(1)

async def is_sudo(event):
    if str(event.sender_id) in Config.SUDO_USERS:
        return True
    else:
        return False
@bot.on(events.NewMessage(pattern=r'/cancel'))
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    try:
        
        await event.respond('Cancelled and restarted.')
        client.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
    except:
        pass
        
from os import environ
class Config(object):
    API_ID = environ.get("API_ID", None)
    API_HASH = environ.get("API_HASH", None)
    BOT_TOKEN = environ.get("BOT_TOKEN", None)
    STRING_SESSION = environ.get("STRING", None)
    SUDO_USERS = environ.get("SUDO_USERS", None)
    COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "^/")
    HELP_MSG = """
    The Commands in the bot are:
    
    **Command :** /forward
    **Usage : ** Forwards messages from a channel to other.
    **Command :** /count
    **Usage : ** Returns the Total message sent using the bot.
    **Command :** /reset
    **Usage : ** Resets the message count to 0.
    **Command :** /restart
    **Usage : ** Updates and Restarts the Bot.
    **Command :** /join
    **Usage : ** Joins the channel.
    **Command :** /help
    **Usage : ** Get the help of this bot.
    **Command :** /status
    **Usage :** Check current status of Bot.
    **Command :** /uptime
    **Usage :** Check uptime of Bot.
    
    Bot is created by @lal_bakthan and @subinps
    """
