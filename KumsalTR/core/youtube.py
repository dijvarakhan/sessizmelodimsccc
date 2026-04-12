import os
import re
import yt_dlp
import random
import asyncio
import aiohttp
from typing import Optional
from pathlib import Path

from py_yt import Playlist, VideosSearch

from KumsalTR import config, logger
from KumsalTR.helpers import Track, utils


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "KumsalTR/cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )
        self.search_cache = {} # Cache for search results

    def get_cookies(self):
        if not self.checked:
            self.cookies = []
            if not os.path.exists(self.cookie_dir):
                os.makedirs(self.cookie_dir)
            
            for file in os.listdir(self.cookie_dir):
                if file.endswith(".txt"):
                    path = os.path.join(self.cookie_dir, file)
                    # Normalize on load to ensure compatibility
                    if self.normalize_cookie_file(path):
                        self.cookies.append(path)
            self.checked = True
        return self.cookies

    def normalize_cookie_file(self, path: str) -> bool:
        """Fixes cookie file formatting to tab-separated Netscape format"""
        if not os.path.exists(path):
            return False
            
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fr:
                content = fr.read()
            
            lines = ["# Netscape HTTP Cookie File"]
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Split by any whitespace, but at most 6 times to keep the 7th field (Value) intact
                parts = line.split(None, 6)
                if len(parts) >= 7:
                    lines.append("\t".join(parts[:7]))
            
            # Write with explicit tabs and LF
            with open(path, "w", encoding="utf-8", newline="\n") as fw:
                fw.write("\n".join(lines) + "\n")
            return True
        except Exception as e:
            logger.warning(f"Failed to normalize cookies in {path}: {e}")
            return False

    async def save_cookies(self, urls: list[str]) -> None:
        logger.info("Saving cookies from urls...")
        os.makedirs(self.cookie_dir, exist_ok=True)
        saved = 0
        async with aiohttp.ClientSession() as session:
            for i, url in enumerate(urls):
                try:
                    path = os.path.join(self.cookie_dir, f"cookie_{i}.txt")
                    slug = url.strip("/").split("/")[-1]
                    link = f"https://batbin.me/api/v2/paste/{slug}"
                    async with session.get(link, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                        if resp.status != 200:
                            logger.warning(f"Cookie fetch failed for {slug}: HTTP {resp.status}")
                            continue
                        data = await resp.read()
                        
                        raw_content = ""
                        try:
                            import json
                            j = json.loads(data)
                            raw_content = j.get("content", "")
                        except (json.JSONDecodeError, ValueError):
                            raw_content = data.decode("utf-8", errors="ignore")
                        
                        if not raw_content or len(raw_content) < 50:
                            logger.warning(f"Cookie data too small for {slug}, skipping")
                            continue
                        
                        with open(path, "w", encoding="utf-8") as fw:
                            fw.write(raw_content)
                        
                        if self.normalize_cookie_file(path):
                            saved += 1
                except Exception as e:
                    logger.warning(f"Failed to save cookie from URL #{i}: {e}")
        logger.info(f"Saved {saved}/{len(urls)} cookies in {self.cookie_dir}.")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    async def search(self, query: str, m_id: int, user: Optional[str] = None, user_id: int = 0, video: bool = False) -> Track | None:
        cache_key = f"{query}_{video}"
        if cache_key in self.search_cache:
            cached = self.search_cache[cache_key]
            # Create a new Track instance with updated user/message info
            return Track(
                id=cached.id,
                channel_name=cached.channel_name,
                duration=cached.duration,
                duration_sec=cached.duration_sec,
                message_id=m_id,
                title=cached.title,
                thumbnail=cached.thumbnail,
                url=cached.url,
                view_count=cached.view_count,
                user=user,
                user_id=user_id,
                video=video,
            )

        _search = VideosSearch(query, limit=1, with_live=False)
        results = await _search.next()
        if results and results["result"]:
            data = results["result"][0]
            duration = data.get("duration") or "0:00"
            thumbnails = data.get("thumbnails") or [{}]
            thumb_url = thumbnails[-1].get("url", "")
            if "?" in thumb_url:
                thumb_url = thumb_url.split("?")[0]
            
            track = Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name", "Unknown"),
                duration=duration,
                duration_sec=utils.to_seconds(duration),
                message_id=m_id,
                title=(data.get("title") or "Unknown")[:25],
                thumbnail=thumb_url,
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short", "0"),
                user=user,
                user_id=user_id,
                video=video,
            )
            self.search_cache[cache_key] = track
            return track
        return None

    async def playlist(self, limit: int, user: str, user_id: int, url: str, video: bool) -> list[Track | None]:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                duration = data.get("duration") or "0:00"
                thumbnails = data.get("thumbnails") or [{}]
                thumb_url = thumbnails[-1].get("url", "")
                if "?" in thumb_url:
                    thumb_url = thumb_url.split("?")[0]
                link = data.get("link", "")
                if "&list=" in link:
                    link = link.split("&list=")[0]
                
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=duration,
                    duration_sec=utils.to_seconds(duration),
                    title=(data.get("title") or "Unknown")[:25],
                    thumbnail=thumb_url,
                    url=link,
                    user=user,
                    user_id=user_id,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except Exception as e:
            logger.warning(f"Playlist fetch failed: {e}")
        return tracks

    async def resolve_spotify(self, url: str) -> str | None:
        if "spotify.com/track/" in url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            html = await resp.text()
                            if match := re.search(r"<title>(.*?) - song by (.*?) \| Spotify</title>", html):
                                return f"{match.group(1)} {match.group(2)}"
                            if match := re.search(r"<title>(.*?) \| Spotify</title>", html):
                                title = match.group(1).replace(" | Spotify", "")
                                return title
            except: pass
        return None


    async def download(self, video_id: str, video: bool = False) -> str | None:
        url = self.base + video_id
        # Define base path without extension to check for existing files
        base_path = f"downloads/{video_id}"
        
        # Check if already exists in any common format
        for ext in ["mp4", "mkv", "webm", "m4a", "mp3"]:
            if os.path.exists(f"{base_path}.{ext}"):
                return f"{base_path}.{ext}"

        if not self.cookies:
            self.get_cookies()
            
        if not self.cookies and config.COOKIES_URL:
            logger.info("Cookie pool empty, refreshing from cloud...")
            try:
                await self.save_cookies(config.COOKIES_URL)
                self.checked = False
                self.get_cookies()
            except: pass

        # Robust format selection in a single string to avoid redundant extraction attempts
        if video:
            fmt = "best[height<=?720]/best"
        else:
            fmt = "bestaudio/best"

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]

        attempts = [None] + list(self.cookies)
        random.shuffle(attempts)

        # Optimization: Limit cookie attempts to avoid long delays
        for cookie in attempts[:5]:
            opts = {
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "cookiefile": cookie,
                "format": fmt,
                "socket_timeout": 10,
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "web"],
                        "skip": ["web_safari", "ios"]
                    }
                },
                "http_headers": {
                    "User-Agent": random.choice(user_agents),
                    "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
                    "Connection": "keep-alive",
                },
            }
            
            try:
                def _dl():
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        if 'url' in info:
                            return info['url']
                        # Desteği olmayan formatlar için fallback
                        for f in info.get('formats', []):
                            if f.get('format_id') == info.get('format_id'):
                                return f.get('url')
                        return info.get('requested_formats', [{}])[0].get('url')

                res_url = await asyncio.wait_for(asyncio.to_thread(_dl), timeout=30)
                if res_url:
                    return res_url
            except Exception as e:
                err = str(e).lower()
                if "403" in err or "429" in err:
                    continue
                if "sign in to confirm" in err:
                    if cookie:
                        logger.error(f"YouTube block detected for cookie: {os.path.basename(cookie)}")
                        if cookie in self.cookies:
                            try:
                                self.cookies.remove(cookie)
                                os.remove(cookie)
                            except: pass
                    else:
                        logger.error("YouTube block detected (No cookie used)")
                    continue
        return None










