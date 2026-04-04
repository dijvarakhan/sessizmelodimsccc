# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR


import re

from pyrogram import filters, types

from KumsalTR import anon, app, config, db, lang, queue, tg, yt
from KumsalTR.helpers import admin_check, buttons, can_manage_vc


@app.on_callback_query(filters.regex("cancel_dl") & ~app.blacklist_filter)
@lang.language()
async def cancel_dl(_, query: types.CallbackQuery):
    await query.answer()
    await tg.cancel(query)


@app.on_callback_query(filters.regex(r"^play_track") & ~app.blacklist_filter)
@lang.language()
async def play_track_handler(_, query: types.CallbackQuery):
    data = query.data.split()
    if len(data) < 3:
        return await query.answer()
    
    cmd, track_id = data[1], data[2]
    url = f"https://www.youtube.com/watch?v={track_id}"
    
    m = query.message
    m.from_user = query.from_user
    m.text = f"/{cmd} {url}"
    m.command = [cmd, url]
    setattr(m, "lang", query.lang)
    
    try:
        await query.message.delete()
    except:
        pass
    
    if cmd == "indir":
        from KumsalTR.plugins.downloader import indir_cmd
        await indir_cmd(_, m)
    elif cmd in ["oynat", "voynat"]:
        from KumsalTR.plugins.play import play_hndlr
        await play_hndlr(_, m, video=(cmd == "voynat"), url=url)


@app.on_callback_query(filters.regex("controls") & ~app.blacklist_filter)
@lang.language()
@can_manage_vc
async def _controls(_, query: types.CallbackQuery):
    args = query.data.split()
    action, chat_id = args[1], int(args[2])
    qaction = len(args) == 4
    user = query.from_user.mention

    if not await db.get_call(chat_id):
        return await query.answer(query.lang["not_playing"], show_alert=True)

    if action == "status":
        return await query.answer()
    await query.answer(query.lang["processing"], show_alert=True)

    if action == "pause":
        if not await db.playing(chat_id):
            return await query.answer(
                query.lang["play_already_paused"], show_alert=True
            )
        await anon.pause(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["paused"], False)
            )
        status = query.lang["paused"]
        reply = query.lang["play_paused"].format(user)

    elif action == "resume":
        if await db.playing(chat_id):
            return await query.answer(query.lang["play_not_paused"], show_alert=True)
        await anon.resume(chat_id)
        if qaction:
            return await query.edit_message_reply_markup(
                reply_markup=buttons.queue_markup(chat_id, query.lang["playing"], True)
            )
        reply = query.lang["play_resumed"].format(user)

    elif action == "skip":
        await anon.play_next(chat_id)
        status = query.lang["skipped"]
        reply = query.lang["play_skipped"].format(user)

    elif action == "force":
        pos, media = queue.check_item(chat_id, args[3])
        if not media or pos == -1:
            return await query.edit_message_text(query.lang["play_expired"])

        m_id = queue.get_current(chat_id).message_id
        queue.force_add(chat_id, media, remove=pos)
        try:
            await app.delete_messages(
                chat_id=chat_id, message_ids=[m_id, media.message_id], revoke=True
            )
            media.message_id = None
        except:
            pass

        msg = await app.send_message(chat_id=chat_id, text=query.lang["play_next"])
        if not media.file_path:
            media.file_path = await yt.download(media.id, video=media.video)
        media.message_id = msg.id
        return await anon.play_media(chat_id, msg, media)

    elif action == "replay":
        media = queue.get_current(chat_id)
        media.user = user
        await anon.replay(chat_id)
        status = query.lang["replayed"]
        reply = query.lang["play_replayed"].format(user)

    elif action == "stop":
        await anon.stop(chat_id)
        status = query.lang["stopped"]
        reply = query.lang["play_stopped"].format(user)

    try:
        if action in ["skip", "replay", "stop"]:
            await query.message.reply_text(reply, quote=False)
            await query.message.delete()
        else:
            mtext = re.sub(
                r"\n\n<blockquote>.*?</blockquote>",
                "",
                query.message.caption.html or query.message.text.html,
                flags=re.DOTALL,
            )
            keyboard = buttons.controls(
                chat_id, status=status if action != "resume" else None
            )
        await query.edit_message_text(
            f"{mtext}\n\n<blockquote>{reply}</blockquote>", reply_markup=keyboard
        )
    except:
        pass


@app.on_callback_query(filters.regex("help") & ~app.blacklist_filter)
@lang.language()
async def _help(_, query: types.CallbackQuery):
    data = query.data.split()
    if len(data) == 1:
        return await query.answer(url=f"https://t.me/{app.username}?start=help")

    action = data[1]

    if action == "back":
        return await query.edit_message_text(
            text=query.lang["help_menu"], reply_markup=buttons.help_markup(query.lang)
        )

    if action == "close":
        try:
            await query.message.delete()
        except:
            pass
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
        return

    help_key = f"help_{action}"
    help_text = query.lang.get(help_key)
    if not help_text:
        return await query.answer("Bu bölüm henüz mevcut değil.", show_alert=True)

    await query.edit_message_text(
        text=help_text,
        reply_markup=buttons.help_markup(query.lang, True),
    )


@app.on_callback_query(filters.regex("settings") & ~app.blacklist_filter)
@lang.language()
@admin_check
async def _settings_cb(_, query: types.CallbackQuery):
    cmd = query.data.split()
    if len(cmd) == 1:
        return await query.answer()
    await query.answer(query.lang["processing"], show_alert=True)

    chat_id = query.message.chat.id
    _admin = await db.get_play_mode(chat_id)
    _delete = await db.get_cmd_delete(chat_id)
    _language = await db.get_lang(chat_id)

    if cmd[1] == "delete":
        _delete = not _delete
        await db.set_cmd_delete(chat_id, _delete)
    elif cmd[1] == "play":
        await db.set_play_mode(chat_id, _admin)
        _admin = await db.get_play_mode(chat_id)
    await query.edit_message_reply_markup(
        reply_markup=buttons.settings_markup(
            query.lang,
            _admin,
            _delete,
            _language,
            chat_id,
        )
    )

@app.on_callback_query(filters.regex("check_joined") & ~app.blacklist_filter)
@lang.language()
async def check_joined_cb(_, query: types.CallbackQuery):
    if config.SUPPORT_CHANNEL:
        ch = config.SUPPORT_CHANNEL.strip("/").split("/")[-1]
        try:
            await app.get_chat_member(ch, query.from_user.id)
            # Katılmış, start mesajına dön
            _text = query.lang["start_pm"].format(query.from_user.first_name, app.name)
            key = buttons.start_key(query.lang, True)
            await query.edit_message_text(text=_text, reply_markup=key)
        except Exception as e:
            err = str(e)
            if "USER_NOT_PARTICIPANT" in err:
                await query.answer("⚠️ Henüz kanala katılmamışsınız!", show_alert=True)
            elif "CHAT_ADMIN_REQUIRED" in err:
                await query.answer("⚠️ Hata: Botun kanalda yönetici olması gerekiyor!", show_alert=True)
            else:
                await query.answer(f"⚠️ Hata: {err}", show_alert=True)
