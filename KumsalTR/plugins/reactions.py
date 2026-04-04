# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

from pyrogram import filters, types
from KumsalTR import app
import random

# Komut ifadeleri listesi (Botun kullanacağı rastgele emojiler)
REACTION_EMOJIS = ["🔥", "⚡", "❤️", "👾", "🎵", "🎧", "🚀", "✨", "💎", "👍", "🌟", "🎹", "🎸", "🕺"]

@app.on_message(
    filters.group 
    & ~app.blacklist_filter
    & filters.regex(r"^[!/]") # Hem / hem ! ile başlayan tüm komutları yakalar
    , group=-1
)
async def auto_reaction_handler(_, m: types.Message):
    """
    Kullanıcı bir komut yazdığında botun otomatik olarak o mesaja ifade (reaksiyon) bırakmasını sağlar.
    """
    try:
        # Sadece metin içeren mesajlara reaksiyon bırak
        if not (m.text or m.caption):
            return
            
        # Rastgele bir emoji seçip reaksiyon olarak ekle
        emoji = random.choice(REACTION_EMOJIS)
        await m.add_reaction(emoji=emoji)
    except Exception:
        # Reaksiyon eklenemezse (yetki yoksa vs.) sessizce geç.
        pass
