# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam

import os
import time
import asyncio
import yt_dlp
from pyrogram import filters, types, enums
from KumsalTR import app, yt, lang, logger, config
from KumsalTR.helpers import utils
import re
import random

# Platform regexleri
RE_MEDIA = re.compile(
    r"(https?://)?(?:[a-zA-Z0-9-]+\.)*(instagram\.com|tiktok\.com|facebook\.com|pinterest\.com|snapchat\.com|likee\.video|threads\.net|youtube\.com|youtu\.be)/[^\s]+"
)

class Downloader:
    def __init__(self):
        self.opts = {
            "quiet": True,
            "no_warnings": True,
            "outtmpl": "downloads/%(title).50s_%(id)s.%(ext)s",
            "format": "bestaudio/best",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "concurrent_fragment_downloads": 10,
            "socket_timeout": 10,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "web"],
                    "skip": ["web_safari", "ios"]
                }
            },
            "http_headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
        }

    async def download(self, url: str, progress_fn=None):
        yt.get_cookies()
        opts = self.opts.copy()
        opts["cookiefile"] = random.choice(yt.cookies) if yt.cookies else None
        
        # User-Agent rotation
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        ]
        opts["http_headers"]["User-Agent"] = random.choice(user_agents)

        loop = asyncio.get_running_loop()
        
        def _progress_hook(d):
            if progress_fn:
                asyncio.run_coroutine_threadsafe(progress_fn(d), loop)

        opts["progress_hooks"] = [_progress_hook]
        
        def _dl():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
        
        return await asyncio.to_thread(_dl)

dl = Downloader()

async def progress(d, m, start_time):
    if d["status"] == "downloading":
        percentage = d.get("_percent_str", "0%").replace("%", "")
        speed = d.get("_speed_str", "0s")
        total = d.get("_total_bytes_str", d.get("_total_bytes_estimate_str", "0"))
        downloaded = d.get("_downloaded_bytes_str", "0")
        
        now = time.time()
        if now - start_time < 2:
            return
        
        try:
            if total == "0" or not percentage:
                await m.edit_text("<b>📥 İɴᴅɪʀɪʟɪʏᴏʀ...</b>")
            else:
                await m.edit_text(
                    m.lang["dl_progress"].format(
                        downloaded, total, float(percentage) if percentage else 0, speed
                    )
                )
        except Exception:
            pass

@app.on_message(filters.command(["indir"]) & ~app.blacklist_filter)
@lang.language()
async def indir_cmd(_, m: types.Message):
    if len(m.command) < 2:
        return await m.reply_text("<b>𝐊ᴜʟʟᴀɴɪᴍ:</b>\n\n<code>/indir [şᴀʀᴋɪ ᴀᴅɪ ᴠᴇʏᴀ ʟɪɴᴋ]</code>")
    
    query = " ".join(m.command[1:])
    sent = await m.reply_text(m.lang["play_searching"])
    
    # Eğer linkse direkt indir, değilse YouTube'dan ara
    if RE_MEDIA.match(query):
        url = query
        if "tiktok.com/foryou" in url or ("@" in url and "/video/" not in url):
            return await sent.edit_text("❌ <b>Gᴇᴄ̧ᴇʀsɪᴢ TɪᴋTᴏᴋ Lɪɴᴋɪ.</b> Lᴜ̈ᴛғᴇɴ ʙɪʀ ᴠɪᴅᴇᴏ ʟɪɴᴋɪ ɢᴏ̈ɴᴅᴇʀɪɴ.")
    else:
        track = await yt.search(query, sent.id)
        if not track:
            return await sent.edit_text(m.lang["play_not_found"].format(config.SUPPORT_CHAT))
        url = track.url

    await sent.edit_text(m.lang["play_downloading"])
    
    try:
        start_time = time.time()
        file_path = await dl.download(url, lambda d: progress(d, sent, start_time))
        
        if not file_path or not os.path.exists(file_path):
            return await sent.edit_text(m.lang["dl_not_found"])
        
        await sent.edit_text(m.lang["dl_complete"])
        
        if file_path.lower().endswith((".mp4", ".mkv", ".mov", ".webm")):
            await m.reply_video(file_path, caption="✅ İɴᴅɪʀɪʟᴅɪ")
        else:
            await m.reply_audio(file_path, caption="✅ İɴᴅɪʀɪʟᴅɪ")
        
        await sent.delete()
        if os.path.exists(file_path): os.remove(file_path)
            
    except Exception as e:
        logger.error(f"Download error: {e}")
        await sent.edit_text(f"❌ <b>Hᴀᴛᴀ Oʟᴜşᴛᴜ:</b> {str(e)[:100]}")

@app.on_message(filters.regex(RE_MEDIA) & filters.group & ~app.blacklist_filter)
@lang.language()
async def auto_dl(_, m: types.Message):
    match = RE_MEDIA.search(m.text or m.caption)
    if not match: return
    url = match.group(0)
    if "tiktok.com/foryou" in url or ("@" in url and "/video/" not in url): return
    sent = await m.reply_text(m.lang["play_downloading"], quote=True)
    
    try:
        start_time = time.time()
        file_path = await dl.download(url, lambda d: progress(d, sent, start_time))
        
        if not file_path or not os.path.exists(file_path):
            return await sent.delete()
            
        await sent.edit_text(m.lang["dl_complete"])
        
        if file_path.lower().endswith((".mp4", ".mkv", ".mov", ".webm")):
            await m.reply_video(file_path, caption="✅ İɴᴅɪʀɪʟᴅɪ")
        else:
            await m.reply_audio(file_path, caption="✅ İɴᴅɪʀɪʟᴅɪ")
            
        await sent.delete()
        if os.path.exists(file_path): os.remove(file_path)
            
    except Exception as e:
        logger.error(f"Auto download error: {e}")
        try:
            await sent.delete()
        except Exception:
            pass

