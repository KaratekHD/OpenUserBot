import importlib

from telethon.errors import PhoneNumberInvalidError

from userbot import LOGGER, bot
from userbot.modules import ALL_MODULES
from userbot.modules.helper_funcs.args import get_args
from userbot.modules import register


INVALID_PH = 'The phone no. entered is incorrect' \
             '\nTip: Use country code (eg +44) along with num.' \
             '\n Recheck your phone number'

try:
    bot.start()
except PhoneNumberInvalidError:
    LOGGER.fatal(INVALID_PH)
    exit(1)

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
HELPS = []
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("userbot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    LOGGER.debug("Loaded Module {}".format(imported_module.__mod_name__))
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two helper_funcs with the same name! Please change one") # NO_TWO_MODULES

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module
        HELPS.append(imported_module.__mod_name__.lower())
        LOGGER.debug(HELPS)

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

def get_text():
    return "test"

@register(outgoing=True, pattern="^.help")
async def help(update):
    args = get_args(update)
    if len(args) >= 1:
        module = ""
        for arg in args:
            if arg == ".help":
                pass
            else:
                if module == "":
                    module = arg.lower()
                else:
                    module = module + " " + arg.lower()
        if module in HELPS:
            await update.edit(f"Below is the help for the `{module}` module.\n\n" + HELPABLE[module].__help__)
        else: await update.edit("I can not find that module! Please check for typos and make sure the module is loaded.")
    else:
        string = ""
        for i in HELPABLE.values():
            string += f"`{str(i.__mod_name__)}`, "
        string = string[:-2]
        await update.edit("Please specify which module you want help for!\n\n"
                         f"{string}")
    
LOGGER.info("Bot is alive! Test it by typing .alive on any chat.")
bot.run_until_disconnected()
