# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR


import asyncio
import os
import time

from pyrogram import types

from KumsalTR import config
from KumsalTR.helpers import Media, buttons, utils


class Telegram:
    def __init__(self):
        self.active = []
        self.events = {}
        self.last_edit = {}
        self.active_tasks = {}
        self.sleep = 5

    def get_media(self, msg: types.Message) -> bool:
        return any([msg.video, msg.audio, msg.document, msg.voice])

    async def download(self, msg: types.Message, sent: types.Message) -> Media | None:
        lang = getattr(sent, "lang", getattr(msg, "lang", {}))
        msg_id = sent.id
        event = asyncio.Event()
        self.events[msg_id] = event
        self.last_edit[msg_id] = 0
        start_time = time.time()

        media = msg.audio or msg.voice or msg.video or msg.document
        file_id = getattr(media, "file_unique_id", None)
        file_ext = getattr(media, "file_name", "").split(".")[-1]
        file_size = getattr(media, "file_size", 0)
        file_title = getattr(media, "title", "Telegram File") or "Telegram File"
        duration = getattr(media, "duration", 0)
        video = bool(getattr(media, "mime_type", "").startswith("video/"))

        if duration > config.DURATION_LIMIT:
            await sent.edit_text(lang.get("play_duration_limit", "Song too long").format(config.DURATION_LIMIT // 60))
            return None

        if file_size > 2048 * 1024 * 1024:
            await sent.edit_text(lang.get("dl_limit", "File too large"))
            return None

        async def progress(current, total):
            if event.is_set():
                return

            now = time.time()
            if now - self.last_edit[msg_id] < self.sleep:
                return

            self.last_edit[msg_id] = now
            percent = current * 100 / total
            speed = current / (now - start_time or 1e-6)
            eta = utils.format_eta(int((total - current) / speed))
            text = lang.get("dl_progress", "Downloading...").format(
                utils.format_size(current),
                utils.format_size(total),
                percent,
                utils.format_size(speed),
                eta,
            )

            await sent.edit_text(
                text, reply_markup=buttons.cancel_dl(lang.get("cancel", "Cancel"))
            )

        try:
            file_path = f"downloads/{file_id}.{file_ext}"
            if not os.path.exists(file_path):
                if file_id in self.active:
                    await sent.edit_text(lang.get("dl_active", "Download already active"))
                    return None

                self.active.append(file_id)
                task = asyncio.create_task(
                    msg.download(file_name=file_path, progress=progress)
                )
                self.active_tasks[msg_id] = task
                await task
                self.active.remove(file_id)
                self.active_tasks.pop(msg_id, None)
                await sent.edit_text(
                    lang.get("dl_complete", "Download complete").format(round(time.time() - start_time, 2))
                )

            return Media(
                id=file_id,
                duration=time.strftime("%M:%S", time.gmtime(duration)),
                duration_sec=duration,
                file_path=file_path,
                message_id=sent.id,
                url=msg.link,
                title=file_title[:25],
                video=video,
            )
        except asyncio.CancelledError:
            return None
        finally:
            self.events.pop(msg_id, None)
            self.last_edit.pop(msg_id, None)
            self.active = [f for f in self.active if f != file_id]

    async def cancel(self, query: types.CallbackQuery):
        lang = getattr(query, "lang", {})
        event = self.events.get(query.message.id)
        task = self.active_tasks.pop(query.message.id, None)
        if event:
            event.set()

        if task and not task.done():
            task.cancel()
        if event or task:
            await query.edit_message_text(
                lang.get("dl_cancel", "Cancelled").format(query.from_user.mention)
            )
        else:
            await query.answer(lang.get("dl_not_found", "Not found"), show_alert=True)
