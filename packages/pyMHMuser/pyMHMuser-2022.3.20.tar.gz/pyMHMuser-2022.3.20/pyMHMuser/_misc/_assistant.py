# MHMuser
# Copyright (C) 2021-2022 MHMuser
#
# This file is a part of < https://github.com/Dev-MHM/MHMuser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Dev-MHM/pyMHMuser/blob/main/LICENSE>.

import inspect
import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery, NewMessage
from telethon.tl.types import InputWebDocument

from .. import LOGS, asst, MHMup_bot
from . import append_or_update, owner_and_sudos

OWNER = MHMup_bot.full_name

MSG = f"""
**MHMuser - UserBot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{OWNER}](tg://user?id={MHMup_bot.uid})
**Support**: @MHMuser
➖➖➖➖➖➖➖➖➖➖
"""

IN_BTTS = [
    [
        Button.url(
            "Repository",
            url="https://github.com/Dev-MHM/MHMuser",
        ),
        Button.url("Support", url="https://t.me/MHMuserSupport"),
    ]
]


# decorator for assistant


def asst_cmd(pattern=None, load=None, owner=False, **kwargs):
    """Decorator for assistant's command"""
    name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")
    kwargs["forwards"] = False

    def ult(func):
        if pattern:
            kwargs["pattern"] = re.compile("^/" + pattern)
        if owner:
            kwargs["from_users"] = owner_and_sudos
        asst.add_event_handler(func, NewMessage(**kwargs))
        if load is not None:
            append_or_update(load, func, name, kwargs)

    return ult


def callback(data=None, from_users=[], owner=False, **kwargs):
    """Assistant's callback decorator"""
    if "me" in from_users:
        from_users.remove("me")
        from_users.append(MHMup_bot.uid)

    def ultr(func):
        async def wrapper(event):
            if from_users and event.sender_id not in from_users:
                return await event.answer("Not for You!", alert=True)
            if owner and event.sender_id not in owner_and_sudos():
                return await event.answer(f"This is {OWNER}'s bot!!")
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

    return ultr


def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and event.sender_id not in owner_and_sudos():
                res = [
                    await event.builder.article(
                        title="MHMuser Userbot",
                        url="https://t.me/MHMuser",
                        description="(c) MHMuser",
                        text=MSG,
                        thumb=InputWebDocument(
                            "https://telegra.ph/file/6a24e2541c3cf2325a939.jpg",
                            0,
                            "image/jpeg",
                            [],
                        ),
                        buttons=IN_BTTS,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"🤖: Assistant of {OWNER}",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don
