# System Patterns

## Architecture Overview
The bot is built on a modular architecture using the Python-based Kurigram library:
- **Core (`KumsalTR/core/`)**: Handles bot initialization, database (MongoDB), and essential services.
- **Plugins (`KumsalTR/plugins/`)**: Command handlers and feature-specific logic (e.g., `start.py`, `play.py`).
- **Helpers (`KumsalTR/helpers/`)**: Utility functions, UI button generators, and queue management.
- **Locales (`KumsalTR/locales/`)**: JSON/YAML strings for internationalization.

## Key Technical Decisions
1. **Kurigram Fork**: Chosen for advanced UI features like animated emojis, colored buttons, and extended `Message` objects.
2. **PyTgCalls Integration**: Used for real-time voice chat audio/video streaming.
3. **MongoDB Backend**: Reliable and flexible data storage for user settings and chat configurations.
4. **Localization Strategy**: JSON-based localization files with a custom `Language` class for simplified access.
5. **Logging System**: Rotating file logs for production debugging.

## Design Patterns & Component Relationships
- **Message Chaining**: (Important) When using Kurigram extensions like `add_reaction` on resulting messages, ensure the original message sending call is fully awaited.
- **Queue Management**: Shared queue object handled in `KumsalTR/helpers/Queue.py`.
- **Bot/Userbot Hybrid**: Uses both a bot and a userbot for voice chat integration (`core/bot.py` and `core/userbot.py`).

## Critical Implementation Paths
- `start_cmd` -> User verification -> Welcome message (with UI and reactions).
- `play_cmd` -> Quality check -> Queueing -> Voice chat stream initialization.
