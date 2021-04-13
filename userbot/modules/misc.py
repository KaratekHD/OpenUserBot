import os

import requests

from userbot.modules import register
from userbot.modules.helper_funcs import extraction
from userbot.strings import string_helper


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    await alive.edit("`Bot is up and running.`")


@register(outgoing=True, pattern="^.runs$")
async def runner_lol(run):
    reply_text = string_helper.get_random_string("runs", "en")
    await run.edit(reply_text)


@register(outgoing=True, pattern="^.ip$")
async def get_bot_ip(ip):
    await ip.edit("`Getting ip...`")
    res = requests.get("http://ipinfo.io/ip")
    await ip.edit(res.text)


async def fetch_info(replied_user, event):
    """ Get details from the User object. """
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    last_name = replied_user.user.last_name
    username = replied_user.user.username
    user_bio = replied_user.about
    is_bot = replied_user.user.bot
    restricted = replied_user.user.restricted
    verified = replied_user.user.verified
    first_name = first_name.replace(
        "\u2060", "") if first_name else ("This User has no First Name")
    if last_name:
        last_name = last_name.replace(
            "\u2060", "")
    user_bio = "This User has no About" if not user_bio else user_bio

    if user_id != (await event.client.get_me()).id:
        common_chat = f"I've seen them in <code>{replied_user.common_chats_count}</code> chats in total."
    else:
        common_chat = "I've seen them in... Wow. Are they stalking me? "
        common_chat += "They're in all the same places I am... oh. It's me."

    caption = "<b>User info:</b> \n"
    caption += f"ID: <code>{user_id}</code> \n"
    caption += f"First Name: {first_name} \n"
    if last_name:
        caption += f"Last Name: {last_name} \n"
    if username:
        caption += f"Username: @{username} \n"
    caption += f"Permanent user link: <a href=\"tg://user?id={user_id}\">link</a>\n"
    caption += f"Is Bot: {is_bot} \n"
    caption += f"Is Restricted: {restricted} \n"
    caption += f"Is Verified by Telegram: {verified} \n\n"
    caption += f"Bio: \n<code>{user_bio}</code> \n \n"
    caption += f"{common_chat} \n"

    return caption


@register(pattern="^.info(?: |$)(.*)", outgoing=True)
async def who(event):
    """ For .whois command, get info about a user. """
    if event.fwd_from:
        return


    replied_user = await extraction.extract_user(event)

    caption = await fetch_info(replied_user, event)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    await event.edit(caption, parse_mode="html")

__mod_name__ = "Misc"

__help__ = " - .`runs`: reply a random string from an array of replies.\n" \
    "- .`info`: get information about a user."
