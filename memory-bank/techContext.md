# Tech Context

## Technologies Used
- **Language**: Python 3.10+ (Running on 3.13 in current environment).
- **Core Library**: `kurigram` (Pyrogram fork).
- **Voice Chat**: `py-tgcalls`.
- **Database**: `pymongo` (MongoDB).
- **Search & Download**: `yt-dlp`, `py-yt-search`.
- **Utilities**: `aiohttp`, `Pillow`, `psutil`, `python-dotenv`.

## Development Setup
- **Dependencies**: `requirements.txt` lists all necessary packages.
- **Environment**: Configured via `config.py` and potentially `.env`.
- **Operating System**: (Current) Windows.

## Technical Constraints & Considerations
- **Pyrogram/Kurigram Differences**: Chaining methods on coroutines will fail; always await the primary message object.
- **Voice Chat Limits**: 7 maximum concurrent transmissions (`max_concurrent_transmissions=7` in `bot.py`).
- **Permissions**: Bot MUST be administrator in the log group.
- **Dependency Management**: Ensure consistent library versions across development and production.

## Tool Usage Patterns
- Use `npx` (if applicable) for scripts.
- Use `npm run dev` or equivalent if web-related (not for this bot).
- Use Python's standard logging for all core components.
