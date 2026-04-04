# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

import asyncio
import importlib

from pyrogram import idle

from KumsalTR import anon, app, config, db, logger, stop, userbot, yt
from KumsalTR.plugins import all_modules


def load_plugins() -> None:
    for module in all_modules:
        importlib.import_module(f"KumsalTR.plugins.{module}")

    # Ek modüller
    for extra in ("KumsalTR.Utah", "KumsalTR.av"):
        try:
            importlib.import_module(extra)
        except Exception as exc:
            logger.warning(f"Ek modül yüklenemedi: {extra} -> {exc}")


async def start_webserver():
    from aiohttp import web
    import os
    
    webapp = web.Application()
    async def handle_ping(request):
        return web.Response(text="Bot is running successfully!")
        
    webapp.router.add_get("/", handle_ping)
    runner = web.AppRunner(webapp)
    await runner.setup()
    
    port = int(os.environ.get("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main() -> None:
    load_plugins()
    await db.connect()

    # Önbelleği bottaki dinamik listelere yükle
    app.bl_users.update(await db.get_blacklisted())
    app.sudoers.update(await db.get_sudoers())
    app.sudoers.add(app.owner)

    await app.boot()
    await userbot.boot()
    await anon.boot()
    
    # Otomatik çerez güncelleme (eğer yapılandırılmışsa)
    if config.COOKIES_URL:
        try:
            await yt.save_cookies(config.COOKIES_URL)
            yt.checked = False # Çerezlerin yeniden taranmasını sağla
        except Exception as e:
            logger.warning(f"Otomatik çerez güncelleme başarısız: {e}")

    # Railway vb. servisler için dummy web server başlatılıyor.
    # Aksi takdirde port bağlamadığı için container 60sn sonra öldürülür.
    await start_webserver()

    logger.info("Humay Music tamamen başlatıldı ve sağlık sunucusu aktifleştirildi.")
    await idle()
    await stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
