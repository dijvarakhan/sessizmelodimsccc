# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

from pyrogram import filters, types, enums
from KumsalTR import app, config, db, lang, yt, anon, queue
from KumsalTR.helpers import buttons, utils
from KumsalTR.helpers._dataclass import Media
import asyncio

@app.on_message(filters.command(["ekle"]) & ~app.blacklist_filter)
@lang.language()
async def add_playlist_cmd(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text(m.lang["playlist_add_usage"])
    
    query = " ".join(m.command[1:])
    sent = await m.reply_text(m.lang["play_searching"])
    
    file = await yt.search(query, sent.id)
    if not file:
        return await sent.edit_text(m.lang["play_not_found"].format(config.SUPPORT_CHAT))
    
    song = {
        "id": file.id,
        "title": file.title,
        "url": file.url,
        "duration": file.duration
    }
    
    await db.add_playlist(m.from_user.id, song)
    await sent.edit_text(m.lang["playlist_add_success"].format(file.title))

@app.on_message(filters.command(["cikar"]) & ~app.blacklist_filter)
@lang.language()
async def rm_playlist_cmd(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text(m.lang["playlist_rm_usage"])
    
    try:
        index = int(m.command[1]) - 1
    except ValueError:
        return await m.reply_text(m.lang["playlist_rm_usage"])
    
    playlist = await db.get_playlist(m.from_user.id)
    if not playlist or index < 0 or index >= len(playlist):
        return await m.reply_text(m.lang["playlist_empty"])
    
    song_id = playlist[index]["id"]
    await db.rm_playlist(m.from_user.id, song_id)
    await m.reply_text(m.lang["playlist_rm_success"])

@app.on_message(filters.command(["listemisil"]) & ~app.blacklist_filter)
@lang.language()
async def del_playlist_cmd(_, m: types.Message):
    await db.del_playlist(m.from_user.id)
    await m.reply_text(m.lang["playlist_del_success"])

@app.on_message(filters.command(["playlist", "poynat"]) & ~app.blacklist_filter)
@lang.language()
async def playlist_cmd(_, m: types.Message):
    if m.command[0] == "poynat" or (len(m.command) > 1 and m.command[1] == "play"):
        return await play_playlist_handler(m.chat.id, m.from_user.id, m)

    # Liste gösterimi
    playlist = await db.get_playlist(m.from_user.id)
    if not playlist:
        return await m.reply_text(m.lang["playlist_menu"])
    
    text = f"{m.lang['playlist_menu']}\n\n<b>𝐋𝐈̇𝐒𝐓𝐄𝐍𝐈̇𝐙:</b>\n"
    for i, song in enumerate(playlist, 1):
        text += f"<b>{i}.</b> {song['title']} ({song['duration']})\n"
    
    if len(playlist) > 30:
        text += f"\n... ve {len(playlist) - 30} şarkı daha."

    await m.reply_text(
        text,
        reply_markup=buttons.playlist_help(m.lang)
    )

@app.on_message(filters.command(["rplay"]) & ~app.blacklist_filter)
@lang.language()
async def rplay_cmd(_, m: types.Message):
    await play_playlist_handler(m.chat.id, m.from_user.id, m, random_play=True)

async def play_playlist_handler(chat_id: int, user_id: int, m: types.Message, random_play=False):
    lang_mod = await lang.get_lang(chat_id)
    
    if m.chat.type == enums.ChatType.PRIVATE:
        return await m.reply_text(lang_mod["play_chat_invalid"])
        
    playlist = await db.get_playlist(user_id)
    if not playlist:
        return await m.reply_text(lang_mod["playlist_empty"])
    
    if random_play:
        import random
        random.shuffle(playlist)
        sent_text = f"<b>🎲 {len(playlist)} şᴀʀᴋɪ ᴘʟᴀʏʟɪsᴛɪɴᴅᴇɴ ᴋᴀʀɪşɪᴋ sɪʀᴀʏᴀ ᴇᴋʟᴇɴɪʏᴏʀ...</b>"
    else:
        sent_text = f"<b>💿 {len(playlist)} şᴀʀᴋɪ ᴘʟᴀʏʟɪsᴛɪɴᴅᴇɴ sɪʀᴀʏᴀ ᴇᴋʟᴇɴɪʏᴏʀ...</b>"

    sent = await m.reply_text(sent_text)
    
    for i, song in enumerate(playlist):
        file = Media(
            id=song["id"],
            title=song["title"],
            url=song["url"],
            duration=song["duration"],
            duration_sec=utils.to_seconds(song["duration"]) if song.get("duration") else 0,
            file_path=None,
            message_id=0,
            user=m.from_user.mention,
        )
        
        if i == 0 and not await db.get_call(chat_id):
            file.file_path = await yt.download(file.id)
            await anon.play_media(chat_id=chat_id, message=sent, media=file)
        else:
            queue.add(chat_id, file)
        
    await m.reply_text(f"<b>✅ {len(playlist)} şᴀʀᴋɪ ʙᴀşᴀʀɪʏʟᴀ sɪʀᴀʏᴀ ᴇᴋʟᴇɴᴅɪ!</b>")

@app.on_callback_query(filters.regex("^play_playlist(_random)?$") & ~app.blacklist_filter)
async def play_playlist_callback(_, cb: types.CallbackQuery):
    random_play = "_random" in cb.data
    await cb.answer("Playlist hazırlanıyor...")
    await cb.message.delete()
    await play_playlist_handler(cb.message.chat.id, cb.from_user.id, cb.message, random_play)

