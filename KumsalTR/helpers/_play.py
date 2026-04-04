# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR


import asyncio

from pyrogram import enums, errors, types

from KumsalTR import app, config, db, logger, queue, yt
from KumsalTR.helpers import utils


from functools import wraps

def checkUB(play):
    @wraps(play)
    async def wrapper(_, m: types.Message, *args, **kwargs):
        if not m.from_user:
            return await m.reply_text(m.lang["play_user_invalid"])

        # Resolve target chat_id for channel play
        if m.command and m.command[0].startswith("c") and m.chat.type != enums.ChatType.CHANNEL:
            chat_id = await db.get_linked_chat(m.chat.id)
            if not chat_id:
                return await m.reply_text("📡 **Önce bir kanal bağlamalısınız!**\n\nKullanım: `/kanal [Kanal ID]`")
        else:
            chat_id = m.chat.id

        if m.chat.type not in [enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
            await m.reply_text(m.lang["play_chat_invalid"])
            try:
                if m.chat.type == enums.ChatType.PRIVATE:
                     pass
                else: 
                     await app.leave_chat(m.chat.id)
            except:
                pass
            return

        if not m.reply_to_message and (
            len(m.command) < 2 or (len(m.command) == 2 and m.command[1] == "-f")
        ) and not kwargs.get("url"):
            return await m.reply_text(m.lang["play_usage"])

        if len(queue.get_queue(chat_id)) >= config.QUEUE_LIMIT:
            return await m.reply_text(m.lang["play_queue_full"].format(config.QUEUE_LIMIT))

        # Use passed arguments if available, otherwise calculate from message
        force = kwargs.get("force")
        if force is None:
            force = m.command[0].endswith("force") or (
                len(m.command) > 1 and "-f" in m.command[1]
            )
            
        video = kwargs.get("video")
        if video is None:
            video = m.command[0][0] == "v" and config.VIDEO_PLAY
            
        url = kwargs.get("url") or utils.get_url(m)
        
        m3u8 = kwargs.get("m3u8")
        if m3u8 is None:
            m3u8 = url and not yt.valid(url)

        play_mode = await db.get_play_mode(chat_id)
        if play_mode or force:
            adminlist = await db.get_admins(chat_id)
            if (
                m.from_user.id not in adminlist
                and not await db.is_auth(chat_id, m.from_user.id)
                and not m.from_user.id in app.sudoers
            ):
                return await m.reply_text(m.lang["play_admin"])

        if chat_id not in db.active_calls:
            client = await db.get_client(chat_id)
            try:
                member = await app.get_chat_member(chat_id, client.id)
                if member.status in [
                    enums.ChatMemberStatus.BANNED,
                    enums.ChatMemberStatus.RESTRICTED,
                ]:
                    try:
                        await app.unban_chat_member(
                            chat_id=chat_id, user_id=client.id
                        )
                    except:
                        return await m.reply_text(
                            m.lang["play_banned"].format(
                                app.name,
                                client.id,
                                client.mention,
                                f"@{client.username}" if client.username else None,
                            )
                        )
            except errors.ChatAdminRequired:
                return await m.reply_text(m.lang["admin_required"])
            except (errors.UserNotParticipant, errors.exceptions.bad_request_400.UserNotParticipant):
                chat = await app.get_chat(chat_id)
                if chat.username:
                    invite_link = chat.username
                    try:
                        await client.resolve_peer(invite_link)
                    except:
                        pass
                else:
                    try:
                        invite_link = chat.invite_link
                        if not invite_link:
                            invite_link = await app.export_chat_invite_link(chat_id)
                    except errors.ChatAdminRequired:
                        return await m.reply_text(m.lang["admin_required"])
                    except Exception as ex:
                        return await m.reply_text(
                            m.lang["play_invite_error"].format(type(ex).__name__)
                        )

                umm = await m.reply_text(m.lang["play_invite"].format(app.name))
                await asyncio.sleep(2)
                try:
                    await client.join_chat(invite_link)
                except errors.UserAlreadyParticipant:
                    pass
                except errors.InviteRequestSent:
                    await asyncio.sleep(2)
                    try:
                        await client.approve_chat_join_request(chat_id, client.id)
                    except errors.HideRequesterMissing:
                        pass
                    except Exception as ex:
                        return await umm.edit_text(
                            m.lang["play_invite_error"].format(type(ex).__name__)
                        )
                except Exception as ex:
                    logger.error(f"Error joining chat - {chat_id}: {ex}")
                    return await umm.edit_text(
                        m.lang["play_invite_error"].format(type(ex).__name__)
                    )

                await umm.delete()
                await client.resolve_peer(chat_id)

        if await db.get_cmd_delete(chat_id):
            try:
                await m.delete()
            except:
                pass

        return await play(_, m, force, m3u8, video, url)

    return wrapper
