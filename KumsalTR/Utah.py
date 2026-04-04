# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
#
# All rights reserved.
#
# Bu kod, Nand Yaduwanshi'nin fikrî mülkiyetidir.
# Açık izin olmadan kopyalamak, değiştirmek, yeniden dağıtmak veya
# ticari/kişisel projelerde kullanmak yasaktır.
#
# İzin Verilen:
# - Kişisel öğrenme amacıyla fork etmek
# - Pull request ile iyileştirme göndermek
#
# Yasak:
# - Kodu kendine aitmiş gibi göstermek
# - İzin veya kredi vermeden yeniden yüklemek
# - Satmak veya ticari amaçla kullanmak
#
# İzin için iletişim:
# E-posta: badboy809075@gmail.com

import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter, ParseMode
from pyrogram.errors import FloodWait
import random
import re

from KumsalTR import app

SPAM_CHATS = []
EMOJI = [
    "🦋🦋🦋🦋🦋",
    "🧚🌸🧋🍬🫖",
    "🥀🌷🌹🌺💐",
    "🌸🌿💮🌱🌵",
    "❤️💚💙💜🖤",
    "💓💕💞💗💖",
    "🌸💐🌺🌹🦋",
    "🍔🦪🍛🍲🥗",
    "🍎🍓🍒🍑🌶️",
    "🧋🥤🧋🥛🍷",
    "🍬🍭🧁🎂🍡",
    "🍨🧉🍺☕🍻",
    "🥪🥧🍦🍥🍚",
    "🫖☕🍹🍷🥛",
    "☕🧃🍩🍦🍙",
    "🍁🌾💮🍂🌿",
    "🌨️🌥️⛈️🌩️🌧️",
    "🌷🏵️🌸🌺💐",
    "💮🌼🌻🍀🍁",
    "🧟🦸🦹🧙👸",
    "🧅🍠🥕🌽🥦",
    "🐷🐹🐭🐨🐻‍❄️",
    "🦋🐇🐀🐈🐈‍⬛",
    "🌼🌳🌲🌴🌵",
    "🥩🍋🍐🍈🍇",
    "🍴🍽️🔪🍶🥃",
    "🕌🏰🏩⛩️🏩",
    "🎉🎊🎈🎂🎀",
    "🪴🌵🌴🌳🌲",
    "🎄🎋🎍🎑🎎",
    "🦅🦜🕊️🦤🦢",
    "🦤🦩🦚🦃🦆",
    "🐬🦭🦈🐋🐳",
    "🐔🐟🐠🐡🦐",
    "🦩🦀🦑🐙🦪",
    "🐦🦂🕷️🕸️🐚",
    "🥪🍰🥧🍨🍨",
    "🥬🍉🧁🧇🔮",
]

def clean_text(text):
    """Markdown özel karakterlerini kaçışla temizle"""
    if not text:
        return ""
    return re.sub(r'([_*()~`>#+-=|{}.!])', r'\\1', text)

async def is_admin(chat_id, user_id):
    admin_ids = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admin_ids

async def process_members(chat_id, members, text=None, replied=None):
    tagged_members = 0
    usernum = 0
    usertxt = ""
    emoji_sequence = random.choice(EMOJI)
    emoji_index = 0

    for member in members:
        if chat_id not in SPAM_CHATS:
            break
        if member.user.is_deleted or member.user.is_bot:
            continue

        tagged_members += 1
        usernum += 1

        emoji = emoji_sequence[emoji_index % len(emoji_sequence)]
        usertxt += f"[{emoji}](tg://user?id={member.user.id}) "
        emoji_index += 1

        if usernum == 5:
            try:
                if replied:
                    await replied.reply_text(
                        usertxt,
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await app.send_message(
                        chat_id,
                        f"{text}\n{usertxt}",
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.MARKDOWN
                    )
                await asyncio.sleep(2)  # Daha hızlı akış için 2 sn
                usernum = 0
                usertxt = ""
                emoji_sequence = random.choice(EMOJI)
                emoji_index = 0
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)  # Biraz tampon
            except Exception as e:
                await app.send_message(chat_id, f"Etiketleme sırasında hata: {str(e)}")
                continue

    if usernum > 0 and chat_id in SPAM_CHATS:
        try:
            if replied:
                await replied.reply_text(
                    usertxt,
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await app.send_message(
                    chat_id,
                    f"{text}\n\n{usertxt}",
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.MARKDOWN
                )
        except Exception as e:
            await app.send_message(chat_id, f"Son part gönderilirken hata: {str(e)}")

    return tagged_members

# /utag alias'ı eklendi (herkesi etiketle)
@app.on_message(
    filters.command(["all", "allmention", "mentionall", "tagall", "utag"], prefixes=["/", "@"])
)
async def tag_all_users(_, message):
    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "Etiketleme zaten çalışıyor. Durdurmak için /cancel yazın."
        )

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text(
            "Herkesi etiketlemek için bir metin verin veya bir mesaja yanıt verin.\nÖrnek: `@utag Merhaba arkadaşlar!`"
        )

    try:
        # Üyeleri tek seferde topla
        members = []
        async for m in app.get_chat_members(message.chat.id):
            members.append(m)

        total_members = len(members)
        SPAM_CHATS.append(message.chat.id)

        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])

        tagged_members = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )

        summary_msg = f"""
✅ Etiketleme tamamlandı!

Toplam üye: {total_members}
Etiketlenen: {tagged_members}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await app.send_message(message.chat.id, f"Bir hata oluştu: {str(e)}")
    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass

@app.on_message(
    filters.command(["admintag", "adminmention", "admins", "report"], prefixes=["/", "@"])
)
async def tag_all_admins(_, message):
    if not message.from_user:
        return

    admin = await is_admin(message.chat.id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if message.chat.id in SPAM_CHATS:
        return await message.reply_text(
            "Etiketleme zaten çalışıyor. Durdurmak için /cancel yazın."
        )

    replied = message.reply_to_message
    if len(message.command) < 2 and not replied:
        return await message.reply_text(
            "Yöneticileri etiketlemek için bir metin verin veya bir mesaja yanıt verin.\nÖrnek: `@admins Acil bakabilir misiniz?`"
        )

    try:
        # Tüm yöneticileri topla
        members = []
        async for m in app.get_chat_members(
            message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            members.append(m)

        total_admins = len(members)
        SPAM_CHATS.append(message.chat.id)

        text = None
        if not replied:
            text = clean_text(message.text.split(None, 1)[1])

        tagged_admins = await process_members(
            message.chat.id,
            members,
            text=text,
            replied=replied
        )

        summary_msg = f"""
✅ Yönetici etiketleme tamamlandı!

Toplam yönetici: {total_admins}
Etiketlenen: {tagged_admins}
"""
        await app.send_message(message.chat.id, summary_msg)

    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await app.send_message(message.chat.id, f"Bir hata oluştu: {str(e)}")
    finally:
        try:
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass

@app.on_message(
    filters.command(
        [
            "stopmention",
            "cancel",
            "cancelmention",
            "offmention",
            "mentionoff",
            "cancelall",
        ],
        prefixes=["/", "@"],
    )
)
async def cancelcmd(_, message):
    chat_id = message.chat.id
    admin = await is_admin(chat_id, message.from_user.id)
    if not admin:
        return await message.reply_text("Bu komutu yalnızca yöneticiler kullanabilir.")

    if chat_id in SPAM_CHATS:
        try:
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass
        return await message.reply_text("Etiketleme başarıyla durduruldu!")
    else:
        return await message.reply_text("Şu anda çalışan bir etiketleme yok!")

MODULE = "Tᴀɢᴀʟʟ"
HELP = """
<b>🧿 Toplu Etiket Komutları</b>

• <code>@all</code> | <code>/all</code> | <code>/tagall</code> | <code>/mentionall</code> | <code>/utag</code> [metin] veya [bir mesaja yanıt]
  → Gruptaki TÜM üyeleri 5'erli paketler halinde rastgele emoji dizisiyle etiketler.

• <code>/admintag</code> | <code>/adminmention</code> | <code>/admins</code> [metin] veya [yanıt]
  → Gruptaki TÜM yöneticileri etiketler (5'erli paketler, rastgele emoji dizisi).

• <code>/stopmention</code> | <code>/cancel</code> | <code>/offmention</code> | <code>/mentionoff</code> | <code>/cancelall</code>
  → Çalışan etiketlemeyi durdurur.

<b>Notlar</b>
1) Bu komutları yalnızca yöneticiler kullanabilir.
2) Botun ve asistanın grupta yönetici olması gerekir.
3) Etiketler, kullanıcı profillerine link veren rastgele emoji dizileriyle yapılır.
4) İşlem bittiğinde toplam/etiketlenen sayılarıyla özet gönderilir.
5) Her partide 5 kullanıcı etiketlenir ve her partinin emojisi değişir.
"""

# ©️ Copyright Reserved - @NoxxOP  Nand Yaduwanshi
# ===========================================
# ©️ 2025 Nand Yaduwanshi (aka @NoxxOP)
# 🔗 GitHub : https://github.com/NoxxOP/ShrutiMusic
# 📢 Telegram Kanalı : https://t.me/ShrutiBots
# ===========================================
# ❤️ ShrutiBots'tan sevgiler