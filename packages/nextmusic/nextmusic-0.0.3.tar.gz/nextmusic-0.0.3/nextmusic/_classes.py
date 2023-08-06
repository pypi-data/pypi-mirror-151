from dataclasses import dataclass
from typing import Union
import discord

from wavelink import (SoundCloudTrack, YouTubeMusicTrack, YouTubePlaylist,
                      YouTubeTrack)
from wavelink.ext.spotify import SpotifyTrack

Provider = Union[
    YouTubeTrack, YouTubePlaylist, YouTubeMusicTrack, SoundCloudTrack, SpotifyTrack
]

# class SupportButton(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(discord.ui.Button(label='Support server', url=self.bot.support_server_url))

@dataclass
class Emojis:
    PREV = "⬅️"
    NEXT = "➡️"
    FIRST = "⏮️"
    LAST = "⏭️"


@dataclass
class Loop:
    NONE = "NONE"
    CURRENT = "CURRENT"
    PLAYLIST = "PLAYLIST"

    TYPES = [NONE, CURRENT, PLAYLIST]
