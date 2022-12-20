from itertools import count
from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from MarkMusic import app
from MarkMusic.misc import SUDO_USERS as SUDOERS
from MarkMusic.plugins.markbots.database.limitsdb import add_to_approved_user, remove_approved_user, get_approved_users, is_approved
from MarkMusic.utils.decorators.language import language

@app.on_message(
    filters.command("ᴀᴘᴘʀᴏᴠᴇ") & filters.user(SUDOERS)
)
@language
async def userapprove(client, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**ᴅᴜᴇ ᴛᴏ ʙᴏᴛ'ꜱ ᴘʀɪᴠᴀᴄʏ ɪꜱꜱᴜᴇꜱ, ʏᴏᴜ ᴄᴀɴ'ᴛ ᴍᴀɴᴀɢᴇ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ ᴡʜᴇɴ ʏᴏᴜ'ʀᴇ ᴜꜱɪɴɢ ᴍᴀʀᴋ'ꜱ ᴅᴀᴛᴀʙᴀꜱᴇ.\n\n ᴘʟᴇᴀꜱᴇ ꜰɪʟʟ ʏᴏᴜʀ. MONGO_DB_UR ɪɴ ʏᴏᴜʀ ᴠᴀʀꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("💠 ɢɪᴠᴇ ᴍᴇ ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴛʜᴇ ᴜꜱᴇʀ...")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if await is_approved(user.id):
            return await message.reply_text(
                "{} ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ".format(user.mention)
            )
        added = await add_to_approved_user(user.id)
        if added:            
            await message.reply_text("ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ.".format(user.mention))
        else:
            await message.reply_text("ғᴀɪʟᴇᴅ")
        return
    if await is_approved(message.reply_to_message.from_user.id):
        return await message.reply_text(
            "{} ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴀᴘᴘʀᴏᴠᴇᴅ".format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_to_approved_user(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            "ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ".format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ")
    return


@app.on_message(
    filters.command("ᴜɴᴀᴘᴘʀᴏᴠᴇ") & filters.user(SUDOERS)
)
@language
async def userunapprove(client, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "**ᴅᴜᴇ ᴛᴏ ʙᴏᴛ'ꜱ ᴘʀɪᴠᴀᴄʏ ɪꜱꜱᴜᴇꜱ, ʏᴏᴜ ᴄᴀɴ'ᴛ ᴍᴀɴᴀɢᴇ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ ᴡʜᴇɴ ʏᴏᴜ'ʀᴇ ᴜꜱɪɴɢ ᴍᴀʀᴋ'ꜱ ᴅᴀᴛᴀʙᴀꜱᴇ.\n\n ᴘʟᴇᴀꜱᴇ ꜰɪʟʟ ʏᴏᴜʀ. MONGO_DB_UR ɪɴ ʏᴏᴜʀ ᴠᴀʀꜱ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("💠 ɢɪᴠᴇ ᴍᴇ ᴜꜱᴇʀɴᴀᴍᴇ ᴏꜰ ᴛʜᴇ ᴜꜱᴇʀ.")
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if await is_approved(user.id):
            return await message.reply_text("{} ɪꜱ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ".format(
                message.from_user.mention
            ))
        removed = await remove_approved_user(user.id)
        if removed:
            await message.reply_text("ʀᴇᴍᴏᴠᴇᴅ **{0}** ᴛᴏ ꜰʀᴏᴍ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ".format(
                message.from_user.mention
            ))
            return
        await message.reply_text(f"ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")
        return
    user_id = message.reply_to_message.from_user.id
    if await is_approved(user_id):
        return await message.reply_text("{} ɪꜱ ɴᴏᴛ ᴀᴘᴘʀᴏᴠᴇᴅ".format(
                message.reply_to_message.from_user.mention
            ))
    removed = await remove_approved_user(user_id)
    if removed:
        await message.reply_text("ʀᴇᴍᴏᴠᴇᴅ **{0}** ᴛᴏ ꜰʀᴏᴍ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ".format(
                message.reply_to_message.from_user.mention
            ))
        return
    await message.reply_text(f"ꜱᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")


@app.on_message(filters.command("ᴀᴘᴘʀᴏᴠᴇᴅ") & filters.user(SUDOERS))
@language
async def approved_list(client, message: Message, _):
    count = 0
    smex = 0
    text = ""
    for user_id in await get_approved_users():
        if 1 == 1:
            try:
                user = await app.get_users(user_id)
                user = (
                    user.first_name
                    if not user.mention
                    else user.mention
                )
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ:**</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("ɴᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴜꜱᴇʀꜱ")
    else:
        await message.reply_text(text)