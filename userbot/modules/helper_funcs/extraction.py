from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName


async def extract_user(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        print(previous_message.peer_id)
        print(previous_message.is_private)
        if previous_message.is_private:
            replied_user = await event.client(GetFullUserRequest(previous_message.peer_id.user_id))
        else:
            replied_user = await event.client(GetFullUserRequest(previous_message.from_id))

    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user