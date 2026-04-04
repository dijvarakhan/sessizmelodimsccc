# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR

import pyrogram
from pyrogram import filters

from KumsalTR import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="HumayMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=pyrogram.types.LinkPreviewOptions(is_disabled=True),
        )

        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID

        # Dinamik kullanıcı listeleri
        self.bl_users: set[int] = set()
        self.sudoers: set[int] = {self.owner}

        # Dinamik filtreler
        self.blacklist_filter = filters.create(
            lambda _, __, update: bool(
                getattr(getattr(update, "from_user", None), "id", None) in self.bl_users
            )
        )
        self.sudo_filter = filters.create(
            lambda _, __, update: bool(
                getattr(getattr(update, "from_user", None), "id", None) in self.sudoers
            )
        )

    async def boot(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                self.logger,
                "✨ <b>Humay Music Bot Başlatıldı</b>\n\n"
                "⚡ Sistem Aktif\n"
                "🎧 Müzik Motoru Hazır\n"
                "🚀 Bot başarıyla çalışıyor.",
            )
            get = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(
                f"\n❌ LOG GRUBUNA ERİŞİM HATASI\n\nBot log grubuna erişemedi.\n\nLOG ID: {self.logger}\nHata: {ex}"
            )

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("❌ Bot log grubunda ADMIN olmalıdır.")

        logger.info(f"✨ Humay Music Bot başlatıldı → @{self.username}")

    async def exit(self):
        await super().stop()
        logger.info("⛔ Humay Music Bot durduruldu.")
