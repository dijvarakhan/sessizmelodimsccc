# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR

import os
from pathlib import Path
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance,
                 ImageFilter, ImageFont, ImageOps)

from KumsalTR import config
from KumsalTR.helpers import Track


class Thumbnail:
    def __init__(self):
        self.rect = (914, 514)
        self.fill = (255, 255, 255)
        self.mask = Image.new("L", self.rect, 0)
        # Font yolları ve boyutları
        font_dir = Path(__file__).resolve().parent
        self.font1 = ImageFont.truetype(str(font_dir / "Raleway-Bold.ttf"), 30)
        self.font2 = ImageFont.truetype(str(font_dir / "Inter-Light.ttf"), 30)
        self.font3 = ImageFont.truetype(str(font_dir / "Raleway-Bold.ttf"), 25)

    async def save_thumb(self, output_path: str, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(output_path, "wb") as f:
                        f.write(await resp.read())
            return output_path

    async def generate(self, song: Track, size=(1280, 720)) -> str:
        try:
            temp = f"cache/temp_{song.id}.jpg"
            output = f"cache/{song.id}.png"
            if os.path.exists(output):
                return output

            await self.save_thumb(temp, song.thumbnail)
            thumb = Image.open(temp).convert("RGBA").resize(size, Image.Resampling.LANCZOS)
            blur = thumb.filter(ImageFilter.GaussianBlur(25))
            image = ImageEnhance.Brightness(blur).enhance(.40)

            _rect = ImageOps.fit(thumb, self.rect, method=Image.LANCZOS, centering=(0.5, 0.5))
            ImageDraw.Draw(self.mask).rounded_rectangle((0, 0, self.rect[0], self.rect[1]), radius=15, fill=255)
            _rect.putalpha(self.mask)
            image.paste(_rect, (183, 30), _rect)

            draw = ImageDraw.Draw(image)
            
            # --- YANILGI FEDERASYONU EKLEMESİ (Sağ Üst Köşe) ---
            federasyon_text = "Yanılgı Federasyonu"
            # Metin boyutunu hesaplayıp sağa yaslıyoruz
            draw.text((1000, 30), federasyon_text, font=self.font3, fill=(255, 255, 255, 180)) 
            # --------------------------------------------------

            draw.text((50, 560), f"{song.channel_name[:25]} | {song.view_count}", font=self.font2, fill=self.fill)
            draw.text((50, 600), song.title[:50], font=self.font1, fill=self.fill)
            draw.text((40, 650), "0:01", font=self.font1)
            draw.line([(140, 670), (1160, 670)], fill=self.fill, width=5, joint="curve")
            draw.text((1185, 650), song.duration, font=self.font1, fill=self.fill)

            image.save(output)
            os.remove(temp)
            return output
        except Exception:
            return config.DEFAULT_THUMB
