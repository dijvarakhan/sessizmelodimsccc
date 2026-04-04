# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone

from pyrogram import filters, types, enums
from KumsalTR import anon, app, config, db, lang, queue, tg, yt
from KumsalTR.helpers import buttons, utils
from KumsalTR.helpers._play import checkUB
from pathlib import Path

def playlist_to_queue(chat_id: int, tracks: list) -> str:
    text = "<blockquote expandable>"
    for track in tracks:
        pos = queue.add(chat_id, track)
        text += f"<b>{pos}.</b> {track.title}\n"
    text = text[:1948] + "</blockquote>"
    return text

@app.on_message(
    filters.command(["coynat", "cplay", "cvoynat", "cvplay", "coynatforce", "cplayforce", "cvoynatforce", "cvplayforce"])
    & (filters.group | filters.channel)
    & ~app.blacklist_filter
)
@lang.language()
@checkUB
async def cplay_hndlr(
    _,
    m: types.Message,
    force: bool = False,
    m3u8: bool = False,
    video: bool = False,
    url: str = None,
) -> None:
    # Resolve target chat id
    if m.chat.type == enums.ChatType.CHANNEL:
        chat_id = m.chat.id
    else:
        linked_chat = await db.get_linked_chat(m.chat.id)
        if not linked_chat:
            return await m.reply_text("📡 **Önce bir kanal bağlamalısınız!**\n\nKullanım: `/kanal [Kanal ID]`")
        chat_id = linked_chat
    
    sent = await m.reply_text(m.lang["play_searching"])
    file = None
    mention = m.from_user.mention if m.from_user else "Kanal"
    media = tg.get_media(m.reply_to_message) if m.reply_to_message else None
    tracks = []

    if url or utils.get_url(m):
        url = url or utils.get_url(m)
        if "playlist" in url:
            await sent.edit_text(m.lang["playlist_fetch"])
            tracks = await yt.playlist(
                config.PLAYLIST_LIMIT, mention, m.from_user.id if m.from_user else 0, url, video
            )

            if not tracks:
                return await sent.edit_text(m.lang["playlist_error"])

            file = tracks[0]
            tracks.remove(file)
            file.message_id = sent.id
        else:
            file = await yt.search(url, sent.id, user=mention, user_id=m.from_user.id if m.from_user else 0, video=video)

        if not file:
            return await sent.edit_text(
                m.lang["play_not_found"].format(config.SUPPORT_CHAT)
            )

    elif len(m.command) >= 2:
        query = " ".join(m.command[1:])
        file = await yt.search(query, sent.id, user=mention, user_id=m.from_user.id if m.from_user else 0, video=video)
        if not file:
            return await sent.edit_text(
                m.lang["play_not_found"].format(config.SUPPORT_CHAT)
            )

    elif media:
        setattr(sent, "lang", m.lang)
        file = await tg.download(m.reply_to_message, sent)

    if not file:
        return await sent.edit_text("🎵 **Kanalda oynatmak için:** `/cplay şarkı adı` yazın veya bir medyayı yanıtlayın.")

    if file.duration_sec > config.DURATION_LIMIT:
        return await sent.edit_text(
            m.lang["play_duration_limit"].format(config.DURATION_LIMIT // 60)
        )

    if await db.is_logger():
        await utils.play_log(m, file.title, file.duration)

    file.user = mention
    if force:
        queue.force_add(chat_id, file)
    else:
        position = queue.add(chat_id, file)

        if position != 0 or await db.get_call(chat_id):
            await sent.edit_text(
                f"<blockquote><u><b><tg-emoji emoji-id=\"5972211849687470465\">➕</emoji> 𝐊𝐚𝐧𝐚𝐥 𝐒𝐢𝐫𝐚𝐬𝐢𝐧𝐚 𝐄𝐤𝐥𝐞𝐧𝐝𝐢 • #{position}</b></u></blockquote>\n"
                f"<b><blockquote><b>➣ 𝐁𝐚𝐬𝐥ɪ𝐤 :</b> <a href={file.url}>{file.title}</a>\n"
                f"<b>➦ 𝐁𝐞𝐤𝐥𝐞𝐦𝐞 : </b> {file.duration} 𝐃𝐚𝐤𝐢ᴋ𝐚 <tg-emoji emoji-id=\"5276032951342088188\">⏳</emoji></b></blockquote>",
                reply_markup=buttons.play_queued(
                    chat_id, file.id, m.lang["play_now"]
                ),
            )
            if tracks:
                added = playlist_to_queue(chat_id, tracks)
                await m.reply_text(
                    text=m.lang["playlist_queued"].format(len(tracks)) + added,
                )
            return

    if not file.file_path:
        fname = f"downloads/{file.id}.{'mp4' if video else 'webm'}"
        if Path(fname).exists():
            file.file_path = fname
        else:
            await sent.edit_text(m.lang["play_downloading"])
            file.file_path = await yt.download(file.id, video=video)

    await anon.play_media(chat_id=chat_id, message=sent, media=file)
    if not tracks:
        return
    added = playlist_to_queue(chat_id, tracks)
    await m.reply_text(
        text=m.lang["playlist_queued"].format(len(tracks)) + added,
    )
