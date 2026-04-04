# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR

from pyrogram import Client

from KumsalTR import config, logger


class Userbot(Client):
    def __init__(self):
        """
        Asistan userbotları başlatır.
        Birden fazla yardımcı hesap çalıştırmak için kullanılır.
        """

        self.clients = []

        clients = {
            "one": "SESSION1",
            "two": "SESSION2",
            "three": "SESSION3"
        }

        for key, string_key in clients.items():
            name = f"KumsalTRUB{key[-1]}"
            session = getattr(config, string_key)

            setattr(
                self,
                key,
                Client(
                    name=name,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH,
                    session_string=session,
                ),
            )

    async def boot_client(self, num: int, ub: Client):
        """
        Asistanı başlatır ve ilk ayarları yapar.
        """

        clients = {
            1: self.one,
            2: self.two,
            3: self.three,
        }

        client = clients[num]

        await client.start()

        try:
            await client.send_message(config.LOGGER_ID, "✅ Asistan Başlatıldı")
        except:
            raise SystemExit(
                f"Asistan {num} log grubuna mesaj gönderemedi."
            )

        client.id = ub.me.id
        client.name = ub.me.first_name
        client.username = ub.me.username
        client.mention = ub.me.mention

        self.clients.append(client)

        # BOT BAŞLAYINCA DESTEK KANALINA KATILIR
        try:
            await client.join_chat("The_Team_Kumsal")
        except:
            pass

        logger.info(f"Asistan {num} başarıyla başlatıldı → @{client.username}")

    async def boot(self):
        """
        Asistanları başlatır.
        """

        if config.SESSION1:
            await self.boot_client(1, self.one)

        if config.SESSION2:
            await self.boot_client(2, self.two)

        if config.SESSION3:
            await self.boot_client(3, self.three)

    async def exit(self):
        """
        Asistanları kapatır.
        """

        if config.SESSION1:
            await self.one.stop()

        if config.SESSION2:
            await self.two.stop()

        if config.SESSION3:
            await self.three.stop()

        logger.info("⛔ Asistanlar durduruldu.")