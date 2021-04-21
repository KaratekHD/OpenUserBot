__mod_name__ = "Spotify"

from userbot.modules.helper_funcs.args import get_args
from userbot.modules import register
from asyncio import create_subprocess_exec
from asyncio.subprocess import PIPE
import os
from userbot import LOGGER

is_downloading = False

@register(outgoing=True, pattern=r"^.spotdl(?: |$)(\S*)")
async def download(update):
    global is_downloading
    path = "/tmp/{}".format(os.getpid())
    if not os.path.exists(path):
        os.mkdir(path)
    args = get_args(update)
    if len(args) < 1:
        await update.edit("`Usage: .spotdl <link>`")
        return
    link = args[0]
    if not "track" in link:
        await update.edit("Invalid link.")
        return
    if is_downloading:
        await update.edit("Already downloading a song, please wait.")
        return
    else:
        is_downloading = True
        try:
            await update.edit("`Downloading song, please wait...`")
            LOGGER.info("Starting download of " + link + ".")
            fetch = await create_subprocess_exec(
                "spotdl",
                link,
                "--output",
                path,
                stdout=PIPE,
                stderr=PIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())
            
            directory = os.fsencode(path)
            for file in os.listdir(directory):
                filename = os.fsdecode(file)
                if filename.endswith(".mp3"):
                    await update.edit("`Sucessfully downloaded " + filename.replace(".mp3", "") + "`")
                    LOGGER.info("Serving " + filename.replace(".mp3", "") + "...")
                    await update.client.send_file(update.chat_id, path + "/" + filename)
                    LOGGER.info("Serving " + filename.replace(".mp3", "") + " - Done.")
                    LOGGER.debug("Deleting old files...")
                    os.remove(path + "/" + filename)
                    LOGGER.debug("Done deleting old files.")
                
        except FileNotFoundError:
            await update.edit("`Spotify-downloader is not installed.`")
        is_downloading = False
