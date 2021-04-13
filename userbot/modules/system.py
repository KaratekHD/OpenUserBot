from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
from userbot.modules import register
from userbot import LOGGER

__mod_name__ = "System"


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    await sysd.edit("`Gathering information...`")
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await create_subprocess_exec(
                "neofetch",
                "--stdout",
                stdout=PIPE,
                stderr=PIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Neofetch is not installed.`")
            
            
@register(outgoing=True, pattern="^.halt$")
async def shutdown(update):
    await update.edit("`Shutting down...`")
    LOGGER.info("Bot shutting down...")
    try:
        await update.client.disconnect()
    except:
        pass

__help__ = " - `.halt`: Stops the bot.\n" \
    " - `.sysd`: Print system information using neofetch."
