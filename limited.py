# Jarvis - Userbot

"""
✘ Commands Available -

• `{i}limited`
   Check you are limited or not !
"""

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from . import jarvis_cmd


@jarvis_cmd(pattern="limited$")
async def demn(jar):
    chat = "@SpamBot"
    msg = await jar.eor("Checking If You Are Limited...")
    async with jar.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=178220800)
            )
            await conv.send_message("/start")
            response = await response
            await jar.client.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Boss! Please Unblock @SpamBot ")
            return
        await msg.edit(f"~ {response.message.message}")
