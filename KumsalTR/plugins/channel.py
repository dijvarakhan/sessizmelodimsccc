# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone

from pyrogram import filters, types, enums
from KumsalTR import app, db, lang
from KumsalTR.helpers._admins import admin_check

@app.on_message(filters.command(["channel", "kanal", "bagla"]) & filters.group & ~app.blacklist_filter)
@lang.language()
@admin_check
async def channel_hndlr(_, m: types.Message):
    if len(m.command) < 2:
        linked_chat = await db.get_linked_chat(m.chat.id)
        if linked_chat:
            try:
                chat = await app.get_chat(linked_chat)
                name = chat.title
            except:
                name = linked_chat
            return await m.reply_text(f"📡 **Mevcut Bağlı Kanal:** `{name}`\n\nKanalı değiştirmek için: `/kanal [Kanal ID veya Kullanıcı Adı]`\nBağlantıyı kesmek için: `/kanal unlink` yazın.")
        return await m.reply_text("📡 **Henüz bağlı bir kanal yok.**\n\nKanal bağlamak için: `/kanal [Kanal ID veya Kullanıcı Adı]`\n\n**Not:** Bot ve Asistanın kanalda yönetici olması gerekir.")

    if m.command[1].lower() == "unlink":
        await db.set_linked_chat(m.chat.id, None)
        return await m.reply_text("✅ Kanal bağlantısı başarıyla kesildi.")

    query = m.command[1]
    try:
        chat = await app.get_chat(query)
        if chat.type != enums.ChatType.CHANNEL:
            return await m.reply_text("❌ Belirttiğiniz ID/Kullanıcı adı bir kanal değil.")
        
        # Test permissions
        try:
            member = await app.get_chat_member(chat.id, app.id)
            if member.status != enums.ChatMemberStatus.ADMINISTRATOR:
                return await m.reply_text("❌ Bot bu kanalda yönetici değil.")
        except:
            return await m.reply_text("❌ Belirttiğiniz kanala erişilemiyor. Botun kanalda olduğundan emin olun.")

        await db.set_linked_chat(m.chat.id, chat.id)
        await m.reply_text(f"✅ **Kanal Bağlandı:** `{chat.title}`\n\nArtık `/cplay` komutunu kullanarak kanalda müzik çalabilirsiniz.")
    except Exception as e:
        await m.reply_text(f"❌ Kanal bulunamadı veya bir hata oluştu: {e}")
