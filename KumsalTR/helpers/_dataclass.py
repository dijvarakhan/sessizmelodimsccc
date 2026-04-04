# @The_Team_kumsal tarafından yasal olarak geliştirildi keyifli kullanımlar #kumsalteam
# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of KumsalTR


from dataclasses import dataclass
from typing import Optional


@dataclass
class Media:
    id: str
    duration: str
    duration_sec: int
    file_path: str
    message_id: int
    title: str
    url: str
    time: int = 0
    user: Optional[str] = None
    user_id: int = 0
    video: bool = False


@dataclass
class Track:
    id: str
    channel_name: str
    duration: str
    duration_sec: int
    title: str
    url: str
    file_path: Optional[str] = None
    message_id: int = 0
    time: int = 0
    thumbnail: Optional[str] = None
    user: Optional[str] = None
    user_id: int = 0
    view_count: Optional[str] = None
    video: bool = False
