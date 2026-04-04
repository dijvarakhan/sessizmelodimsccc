import aiohttp
import urllib.parse
from pyrogram import filters, types
from KumsalTR import app, queue, logger, lang

async def fetch_lyrics(title: str):
    try:
        q = urllib.parse.quote(title)
        url = f"https://lrclib.net/api/search?q={q}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': 'Mozilla/5.0'}) as res:
                if res.status == 200:
                    data = await res.json()
                    if data and len(data) > 0:
                        for item in data:
                            if item.get("plainLyrics"):
                                return f"<b>📝 {item['artistName']} - {item['trackName']}</b>\n\n<code>{item['plainLyrics']}</code>"
    except Exception as e:
        logger.error(f"Lyrics fetch error: {e}")
    return None

@app.on_message(filters.command(["soz"]) & ~app.blacklist_filter)
@lang.language()
async def soz_cmd(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text("<b>𝐊ᴜʟʟᴀɴɪᴍ:</b>\n\n<code>/soz [şarkı adı]</code>")
    
    query = " ".join(m.command[1:])
    sent = await m.reply_text("<b><tg-emoji emoji-id=\"5319230516929502602\">🔍</emoji> Şᴀʀᴋɪ sᴏ̈ᴢʟᴇʀɪ ᴀʀᴀɴɪʏᴏʀ...</b>")
    
    lyrics = await fetch_lyrics(query)
    if lyrics:
        if len(lyrics) > 4000:
            lyrics = lyrics[:4000] + "\n\n... (Dᴇᴠᴀᴍɪ sɪɢɢᴍᴀᴅɪ)"
        await sent.edit_text(lyrics)
    else:
        await sent.edit_text("<b>❌ Mᴀᴀʟᴇsᴇғ ʙᴜ şᴀʀᴋɪɴɪɴ sᴏ̈ᴢʟᴇʀɪ ʙᴜʟᴜɴᴀᴍᴀᴅɪ!</b>")

@app.on_callback_query(filters.regex(r"^lyrics ") & ~app.blacklist_filter)
async def lyrics_callback(_, cb: types.CallbackQuery):
    chat_id = int(cb.data.split()[1])
    
    media = queue.get_current(chat_id)
    if not media:
        return await cb.answer("Şᴜ ᴀɴ çᴀʟᴀɴ ʙɪʀ şᴀʀᴋɪ ʏᴏᴋ!", show_alert=True)
    
    title = media.title
    channel = getattr(media, "channel_name", "")
    
    # Clean up standard youtube suffixes
    clean_title = title.lower()
    for rm in ["(official video)", "[official video]", "official music video", "(lyrics)", "[lyrics]", "lyric video"]:
        clean_title = clean_title.replace(rm, "")
        
    await cb.answer("Şᴀʀᴋɪ sᴏ̈ᴢʟᴇʀɪ ᴀʀᴀɴɪʏᴏʀ, ʟᴜ̈ᴛғᴇɴ ʙᴇᴋʟᴇʏɪɴ...")
    
    search_query = f"{clean_title.strip()} {channel}".strip()
    lyrics = await fetch_lyrics(search_query)
    
    if lyrics:
        try:
            if len(lyrics) > 4000:
                lyrics = lyrics[:4000] + "\n\n... (Dᴇᴠᴀᴍɪ sɪɢɢᴍᴀᴅɪ)"
            await app.send_message(cb.from_user.id, lyrics)
            await cb.answer("✅ Şᴀʀᴋɪ sᴏ̈ᴢʟᴇʀɪ Öᴢᴇʟ Mᴇsᴀᴊʟᴀʀɪɴᴀ ɢᴏ̈ɴᴅᴇʀɪʟᴅɪ!", show_alert=True)
        except Exception as e:
            await cb.answer("❌ ÖZEL MESAJ GÖNDERİLEMEDİ! Öɴᴄᴇ ʙᴀɴᴀ ᴏ̈ᴢᴇʟᴅᴇɴ (DM) /start ʏᴀᴢɪɴ.", show_alert=True)
    else:
        await cb.answer("❌ Mᴀᴀʟᴇsᴇғ ʙᴜ şᴀʀᴋɪɴɪɴ sᴏ̈ᴢʟᴇʀɪ ʙᴜʟᴜɴᴀᴍᴀᴅɪ!", show_alert=True)
