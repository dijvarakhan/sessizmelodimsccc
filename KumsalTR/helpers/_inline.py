import re
from pyrogram import types
from pyrogram.enums import ButtonStyle
from KumsalTR import app, config, lang
from KumsalTR.core.lang import lang_codes

# ─── Gerçek Custom Emoji ID'leri (Telegram Premium) ───
EMOJI_DOTS = 5319293665833656034        # ➕ Yeni hareketli artı emojisi
EMOJI_WAVE = 5972211849687470465        # 🎼 Ses dalgası / ekolayzer
EMOJI_MOON = 5316599188035740602        # 🏆 Sahibi (Kupa)
EMOJI_BOOM = 5276032951342088188        # 💥 Patlama / yıldız
EMOJI_NOTE = 5470135030393090150        # 🎵 Müzik notaları
EMOJI_FIRE = 5244892192178189077        # 🔥 Ateş / Aktiflik
EMOJI_LOAD = 5974235702701853774        # 🔄 Yükleniyor / Yenile
EMOJI_HORN = 5298609030321691620        # 📢 Duyuru / Megafon
EMOJI_GUY  = 5971889748615105853        # 👨‍💻 Laptop adam
EMOJI_CHART = 5231200819986047254       # 📊 Grafik
EMOJI_SKIP  = 5314606606678237326       # ↪️ Atla (Mavi ok)
EMOJI_PAUSE = 5319190934510904031       # ⏳ Dur (Kum saati)
EMOJI_STOP  = 5314346928660554905       # ⚠️ Durdur (Uyarı)
EMOJI_REPLAY = 5316553657087435063       # 🎧 Kulaklık (Kullanıcı isteği)


def _get_enum_style(style_str: str):
    if not style_str:
        return None
    style_str = str(style_str).lower()
    if style_str == "primary":
        return getattr(ButtonStyle, "PRIMARY", None)
    elif style_str == "success":
        return getattr(ButtonStyle, "SUCCESS", None)
    elif style_str == "danger":
        return getattr(ButtonStyle, "DANGER", None)
    return getattr(ButtonStyle, "DEFAULT", None)


def _ikb(text, style=None, icon_custom_emoji_id=None, **kwargs):
    """
    InlineKeyboardButton oluşturur.
    Kurigram (Pyrogram fork) üzerinde Buton renkleri ve Emoji ID ekler.
    Etiketleri (tg-emoji vb.) butondan temizler çünkü butonlar HTML desteklemez.
    """
    try:
        # HTML etiketlerini temizle
        clean_text = re.sub(r'<[^>]*>', '', str(text)).strip()
        
        extra = {}
        if style:
            enum_style = _get_enum_style(style)
            if enum_style:
                extra["style"] = enum_style
        if icon_custom_emoji_id:
            extra["icon_custom_emoji_id"] = int(icon_custom_emoji_id)
            
        return types.InlineKeyboardButton(text=clean_text, **extra, **kwargs)
    except Exception as e:
        import logging
        logging.error(f'InlineKeyboard Error: {e}')
        clean_text = re.sub(r'<[^>]*>', '', str(text)).strip()
        return types.InlineKeyboardButton(text=clean_text, **kwargs)


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def force_subscribe_markup(self, lang: dict):
        return self.ikm(
            [
                [
                    _ikb(
                        text=lang["join_ch_btn"],
                        url=config.SUPPORT_CHANNEL,
                        style="danger", # Kırmızı (Dikkat çekici)
                        icon_custom_emoji_id=EMOJI_HORN, # Megafon
                    )
                ],
                [
                    _ikb(
                        text=lang["joined_btn"],
                        callback_data="check_joined",
                        style="success", # Yeşil (Onay)
                        icon_custom_emoji_id=EMOJI_LOAD, # Yenile / Kontrol Et
                    )
                ]
            ]
        )

    def cancel_dl(self, text):
        return self.ikm(
            [[_ikb(
                text="ɪ̇ᴘᴛᴀʟ ᴇᴛ",
                callback_data="cancel_dl",
                style="danger",
                icon_custom_emoji_id=EMOJI_BOOM,
            )]]
        )

    def controls(self, chat_id: int, status=None, timer=None, remove=False):
        keyboard = []

        if status:
            keyboard.append(
                [_ikb(
                    text=status,
                    callback_data=f"controls status {chat_id}",
                    style="primary",
                    icon_custom_emoji_id=EMOJI_NOTE,
                )]
            )
        elif timer:
            keyboard.append(
                [_ikb(
                    text=timer,
                    callback_data=f"controls status {chat_id}",
                )]
            )

        if not remove:
            keyboard.append(
                [
                    _ikb(
                        text="ᴛᴇᴋʀᴀʀ",
                        callback_data=f"controls replay {chat_id}",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_REPLAY,
                    ),
                    _ikb(
                        text="ᴅᴜʀ",
                        callback_data=f"controls pause {chat_id}",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_PAUSE,
                    ),
                    _ikb(
                        text="ᴀᴛʟᴀ",
                        callback_data=f"controls skip {chat_id}",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_SKIP,
                    ),
                ]
            )

            keyboard.append(
                [
                    _ikb(
                        text="ᴅᴜʀᴅᴜʀ",
                        callback_data=f"controls stop {chat_id}",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_STOP,
                    ),
                    _ikb(
                        text="ɢʀᴜʙᴀ ᴇᴋʟᴇ",
                        url=f"https://t.me/{app.username}?startgroup=true",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_DOTS,
                    ),
                ]
            )

            keyboard.append(
                [
                    _ikb(
                        text="Sᴏ̈ᴢʟᴇʀ",
                        callback_data=f"lyrics {chat_id}",
                        style="success",
                        icon_custom_emoji_id=EMOJI_NOTE,
                    )
                ]
            )

            keyboard.append(
                [
                    _ikb(
                        text="ᴅᴇsᴛᴇᴋ",
                        url=config.SUPPORT_CHAT,
                        style="danger",
                        icon_custom_emoji_id=EMOJI_HORN,
                    ),
                    _ikb(
                        text="ᴋᴀᴘᴀᴛ",
                        callback_data="help close",
                        style="danger",
                        icon_custom_emoji_id=EMOJI_BOOM,
                    ),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(self, _lang: dict, back=False):
        if back:
            rows = [
                [
                    _ikb(
                        text="ɢᴇʀɪ ᴅᴏ̈ɴ",
                        callback_data="help back",
                        style="danger",
                        icon_custom_emoji_id=EMOJI_MOON,
                    )
                ]
            ]
        else:
            # Resimlerdeki MANTIK (2'li kolon dizilimi) ama KumsalXMusic buton isimleriyle.
            # Kodun asıl komutları: play, admins, queue, extras (daha önce ekledik), etiket, eglence vb.
            # KumsalXMusic özel fontunu koruyarak yapıyoruz:
            rows = [
                # 1. Satır: Oynatma + Yönetim
                [
                    _ikb(text="ᴄ̧ᴀʟ ᴋᴇᴋᴇ", callback_data="help play", style="primary", icon_custom_emoji_id=EMOJI_NOTE),
                    _ikb(text="ʏᴏ̈ɴᴇᴛɪᴍ", callback_data="help admins", style="primary", icon_custom_emoji_id=EMOJI_WAVE)
                ],
                # 2. Satır: Sıra + Veri(Ekstralar)
                [
                    _ikb(text="sɪʀᴀ", callback_data="help queue", style="primary", icon_custom_emoji_id=EMOJI_LOAD),
                    _ikb(text="ᴅɪɢ̆ᴇʀ", callback_data="help extras", style="primary", icon_custom_emoji_id=EMOJI_CHART)
                ],
                # 3. Satır: Etiket + Eğlence
                [
                    _ikb(text="ᴇᴛɪᴋᴇᴛ", callback_data="help etiket", style="primary", icon_custom_emoji_id=EMOJI_DOTS),
                    _ikb(text="ᴇɢ̆ʟᴇɴᴄᴇ", callback_data="help eglence", style="primary", icon_custom_emoji_id=EMOJI_FIRE)
                ],
                # 4. Satır: Geliştirici (Sudo) + İndirici
                [
                    _ikb(text="ᴘᴀᴛʀᴏɴ", callback_data="help sudo", style="primary", icon_custom_emoji_id=EMOJI_GUY),
                    _ikb(text="ɪ̇ɴᴅɪʀɪᴄɪ", callback_data="help indir", style="primary", icon_custom_emoji_id=EMOJI_LOAD)
                ],
                # 5. Satır: Ana Menü / Kapat - Tam Genişlik Kırmızı
                [
                    _ikb(text="ᴀɴᴀ ᴍᴇɴᴜ̈ʏᴇ ᴅᴏ̈ɴ", callback_data="help close", style="danger", icon_custom_emoji_id=EMOJI_BOOM)
                ],
            ]

        return self.ikm(rows)

    def lang_markup(self, _lang: str):
        langs = lang.get_languages()
        buttons = [
            _ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
                style="success" if code == _lang else "primary",
                icon_custom_emoji_id=EMOJI_DOTS,
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str):
        return self.ikm(
            [[_ikb(
                text="ᴅᴇsᴛᴇᴋ",
                url=config.SUPPORT_CHAT,
                style="success",
                icon_custom_emoji_id=EMOJI_HORN,
            )]]
        )

    def play_queued(self, chat_id: int, item_id: str, _text: str):
        return self.ikm(
            [
                [
                    _ikb(
                        text="şɪᴍᴅɪ ᴏʏɴᴀᴛ",
                        callback_data=f"controls force {chat_id} {item_id}",
                        style="success",
                        icon_custom_emoji_id=EMOJI_FIRE,
                    )
                ]
            ]
        )

    def play_markup(self, chat_id: int, track_id: str, duration: str, media_type: str = "audio"):
        cmd = "voynat" if media_type == "video" else "oynat"
        return self.ikm(
            [
                [
                    _ikb(
                        text="ᴏʏɴᴀᴛ",
                        callback_data=f"play_track {cmd} {track_id}",
                        style="success",
                        icon_custom_emoji_id=EMOJI_NOTE,
                    ),
                    _ikb(
                        text="ɪ̇ɴᴅɪʀ",
                        callback_data=f"play_track indir {track_id}",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_LOAD,
                    ),
                ],
                [
                    _ikb(
                        text="ᴅᴇsᴛᴇᴋ",
                        url=config.SUPPORT_CHAT,
                        style="danger",
                        icon_custom_emoji_id=EMOJI_HORN,
                    ),
                ],
            ]
        )

    def queue_markup(self, chat_id: int, _text: str, playing: bool):
        action = "pause" if playing else "resume"
        return self.ikm(
            [[_ikb(
                text=_text,
                callback_data=f"controls {action} {chat_id} q",
                style="success" if playing else "primary",
                icon_custom_emoji_id=EMOJI_NOTE if playing else EMOJI_MOON,
            )]]
        )

    def playlist_help(self, lang: dict):
        return self.ikm(
            [
                [
                    _ikb(text="▶️ OYNAT", callback_data="play_playlist", style="success", icon_custom_emoji_id=EMOJI_NOTE),
                    _ikb(text="🎲 KARIŞIK", callback_data="play_playlist_random", style="primary", icon_custom_emoji_id=EMOJI_SKIP),
                ],
                [
                    _ikb(text="⏪ GERİ DÖN", callback_data="help back", style="danger")
                ]
            ]
        )

    def settings_markup(self, lang: dict, admin_only, cmd_delete, language, chat_id):
        return self.ikm(
            [
                [
                    _ikb(
                        text="ᴏʏɴᴀᴛᴍᴀ ᴍᴏᴅᴜ",
                        callback_data="settings",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_NOTE,
                    ),
                    _ikb(
                        text=admin_only,
                        callback_data="settings play",
                        style="success" if admin_only else "danger",
                    ),
                ],
                [
                    _ikb(
                        text="ᴋᴏᴍᴜᴛ sɪʟᴍᴇ",
                        callback_data="settings",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_LOAD,
                    ),
                    _ikb(
                        text=cmd_delete,
                        callback_data="settings delete",
                        style="success" if cmd_delete else "danger",
                    ),
                ],
                [
                    _ikb(
                        text="ᴅɪʟ sᴇᴄ̧",
                        callback_data="settings play",
                        style="primary",
                        icon_custom_emoji_id=EMOJI_DOTS,
                    ),
                    _ikb(
                        text=lang_codes[language],
                        callback_data="language",
                        style="success",
                        icon_custom_emoji_id=EMOJI_MOON,
                    ),
                ],
            ]
        )

    def start_key(self, lang: dict, private=False):
        if private:
            # Resim 2'deki MANTIK (Kaynak kodsuz):
            rows = [
                # 1. Satır: Beni Ekle (Tam Genişlik - Yeşil)
                [
                    _ikb(text=lang["add_me"], url=f"https://t.me/{app.username}?startgroup=true", style="success", icon_custom_emoji_id=EMOJI_DOTS)
                ],
                # 2. Satır: Destek + Duyuru (Yan Yana - Yeşil)
                [
                    _ikb(text=lang["support"], url=config.SUPPORT_CHAT, style="success", icon_custom_emoji_id=EMOJI_HORN),
                    _ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL, style="success", icon_custom_emoji_id=EMOJI_WAVE)
                ],
                # 3. Satır: Sahibi (Tam Genişlik - Kırmızı/Kahve)
                [
                    _ikb(text=lang["aloneowner"], user_id=config.OWNER_ID, style="danger", icon_custom_emoji_id=EMOJI_MOON)
                ],
                # 4. Satır: Yardım ve Komutlar (Tam Genişlik - Mavi)
                [
                    _ikb(text=lang["help"], callback_data="help back", style="primary", icon_custom_emoji_id=EMOJI_GUY)
                ]
            ]
        else:
            rows = [
                [
                    _ikb(text=lang["add_me"], url=f"https://t.me/{app.username}?startgroup=true", style="success", icon_custom_emoji_id=EMOJI_DOTS)
                ],
                [
                    _ikb(text=lang["help"], callback_data="help", style="primary", icon_custom_emoji_id=EMOJI_GUY)
                ],
                [
                    _ikb(text=lang["language"], callback_data="language", style="primary", icon_custom_emoji_id=EMOJI_MOON)
                ]
            ]
        return self.ikm(rows)

    def yt_key(self, link: str):
        return self.ikm(
            [
                [
                    _ikb(
                        text="ᴅɪɴʟᴇ",
                        url=link,
                        style="success",
                        icon_custom_emoji_id=EMOJI_NOTE,
                    ),
                    _ikb(
                        text="ᴅᴇsᴛᴇᴋ",
                        url=config.SUPPORT_CHAT,
                        style="primary",
                        icon_custom_emoji_id=EMOJI_HORN,
                    ),
                ]
            ]
        )
