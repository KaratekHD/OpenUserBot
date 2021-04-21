__mod_name__ = "Message Deletion"

from userbot.modules import register
from telethon.errors import rpcbaseerrors
from userbot import LOGGER
from asyncio import sleep
from userbot.modules.helper_funcs.args import get_args

@register(outgoing=True, pattern="^.del$")
async def delete(delete):
    # LOGGER.debug(delete.message.message)
    msg_src = await delete.get_reply_message()
    if delete.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delete.delete()
        except:
            await delete.edit("`Couldn't delete message.`")
    else:
        await delete.edit("`Message not found.`")
        
    
@register(outgoing=True, pattern="^.purge")
@register(outgoing=True, pattern="^.p")
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    # TODO: Parsing args and deleting x messages
    args = get_args(purg)
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0
    if purg.reply_to_msg_id is None:
        await purg.edit("`Reply to a message to select where to start purging from.`", )
        return
    async for msg in itermsg:
        msgs.append(msg)
        count = count + 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await purg.client.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(purg.chat_id, "Purge complete!\n\nPurged {} messages. **This auto-generated message shall be self destructed in 2 seconds.**".format(count))
    await sleep(2)
    await done.delete()

# TODO: change
__help__ = " - `.purge <int>`: Reply to a message to delete all/ all x messages sent after it.\n" \
        " - `.p <int>`: Same as above.\n" \
        " - `.del`: Answer to a message to delete it."
