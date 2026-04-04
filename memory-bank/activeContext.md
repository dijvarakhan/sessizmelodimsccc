# Active Context

## Current Status
- **Recent Fixes**:
  - Fixed animated Telegram emojis not rendering: `emoji-id` attributes in `<tg-emoji>` HTML tags were missing double quotes. Added proper quotes across `en.json`, `calls.py`, `cplay.py`, and `lyrics.py`. Bot already uses `parse_mode=HTML` as default.
  - Fixed TikTok regex in `downloader.py` allowing subdomains like `vt.tiktok.com` and `vm.tiktok.com`.
  - Overhauled `/yarisma` in `quiz.py` to add interactive language and genre selection menus using Pyrogram callbacks.
  - Rewrote quiz snippet downloader to use python `yt_dlp` API natively with `download_ranges` to fix the 60-second timeouts and output 0-byte invalid files.

## Recent Changes
- `downloader.py`: Updated `RE_MEDIA` to allow any subdomain before `tiktok.com`.
- `quiz.py`: Complete rewrite of `/yarisma` command. Added multiple song pools (`TR_POP`, `TR_ARABESK`, `EN_POP`), inline callback menus, and direct `yt_dlp` slice fetching.
- `callbacks.py`: Restructured help callback to safely handle missing locale keys
- `youtube.py`: Complete rewrite of download function with multi-format fallback loop; Added search cache and Spotify link support
- `config.py`: Increased `DURATION_LIMIT` to 3 hours and `QUEUE_LIMIT` to 50 for film support
- `telegram.py`: Increased file size limit to 2 GB for large media support
- `play.py`: Added Spotify URL resolution and updated limits info
- Rebranding: Completed "fizy" to "humay" transition across all files, README, and setup scripts
- Cleanup: Removed redundant scripts (`convert.py`, `test_*.py`, etc.) and root `__pycache__`

## Work in Focus
- Stability improvements across all command flows
- Support long-duration films (up to 3 hours) and large file sizes (up to 2 GB)
- Ensuring all features work end-to-end without crashes

## Next Steps
1. Test all help menu buttons to ensure no missing key errors
2. Monitor PyTgCalls streaming stability using direct yt-dlp extracted URLs
3. Test quiz feature with new song pool
4. Consider adding missing keys to other locale files (ar, de, etc.)
5. Test playlist play command in group chats

## Active Decisions & Patterns
- Use `.get()` with fallback for all locale key access in dynamic contexts
- PyTgCalls now streams audio/video directly from YT URLs instead of downloading locally first, making playback nearly instant.
- Quiz downloads still use local chunk downloads (with timeout protection) as they require FFmpeg slicing.
- All `play_not_found` calls include `.format(config.SUPPORT_CHAT)` argument
