# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

import os
from pyrogram import filters, types
from KumsalTR import app, yt, config, lang

@app.on_message(filters.command(["cookie", "cerezkoy"]) & filters.user(config.OWNER_ID))
@lang.language()
async def update_cookie(_, m: types.Message):
    if not m.reply_to_message or not m.reply_to_message.document:
        return await m.reply_text("<b>🍪 Lᴜ̈ᴛғᴇɴ ʙɪʀ .ᴛxᴛ ᴄ̧ᴇʀᴇᴢ (ᴄᴏᴏᴋɪᴇ) ᴅᴏsʏᴀsɪɴɪ ʏᴀɴɪᴛʟᴀʏᴀʀᴀᴋ <code>/cookie</code> ʏᴀᴢɪɴ.</b>")
    
    doc = m.reply_to_message.document
    if not doc.file_name.endswith(".txt"):
        return await m.reply_text("<b>❌ Dᴏsʏᴀ .ᴛxᴛ ғᴏʀᴍᴀᴛɪɴᴅᴀ ᴏʟᴍᴀʟɪᴅɪʀ.</b>")
    
    sent = await m.reply_text("<b>🔄 Çᴇʀᴇᴢʟᴇʀ ɪşʟᴇɴɪʏᴏʀ...</b>")
    
    try:
        # Eski çerezleri temizle veya üzerine yaz
        path = "KumsalTR/cookies/cookie.txt"
        await m.reply_to_message.download(path)
        
        # YouTube core'u tetikle
        yt.checked = False
        yt.cookies = []
        yt.get_cookies()
        
        await sent.edit_text("<b>✅ YᴏᴜTᴜʙᴇ ᴄ̧ᴇʀᴇᴢʟᴇʀɪ ʙᴀşᴀʀɪʏʟᴀ ɢᴜ̈ɴᴄᴇʟʟᴇɴᴅɪ ᴠᴇ sɪsᴛᴇᴍᴇ ᴛᴀɴɪᴍʟᴀɴᴅɪ!</b>")
    except Exception as e:
        await sent.edit_text(f"<b>❌ Hᴀᴛᴀ: {e}</b>")

@app.on_message(filters.command(["clearcache"]) & filters.user(config.OWNER_ID))
async def clear_cache_cmd(_, m: types.Message):
    count = 0
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    for file in os.listdir("downloads"):
        try:
            os.remove(f"downloads/{file}")
            count += 1
        except:
            continue
    await m.reply_text(f"<b>🧹 {count} ᴀᴅᴇᴛ ᴏ̈ɴʙᴇʟʟᴇᴋ ᴅᴏsʏᴀsɪ ᴛᴇᴍɪᴢʟᴇɴᴅɪ.</b>")
