# MHMuser
# Copyright (C) 2021-2022 MHMuser
#
# This file is a part of < https://github.com/Dev-MHM/MHMuser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Dev-MHM/pyMHMuser/blob/main/LICENSE>.

import sys

from .version import __version__

run_as_module = False

if sys.argv[0] == "-m":
    run_as_module = True

    import time

    from .configs import Var
    from .startup import *
    from .startup._database import MHMuserDB
    from .startup.BaseClient import MHMuserClient
    from .startup.connections import session_file, vc_connection
    from .startup.funcs import _version_changes, autobot, enable_inline, update_envs
    from .version import MHMup_version

    start_time = time.time()
    _ult_cache = {}

    udB = MHMuserDB()
    update_envs()

    LOGS.info(f"Connecting to {udB.name}...")
    if udB.ping():
        LOGS.info(f"Connected to {udB.name} Successfully!")

    BOT_MODE = udB.get_key("BOTMODE")
    DUAL_MODE = udB.get_key("DUAL_MODE")

    if BOT_MODE:
        if DUAL_MODE:
            udB.del_key("DUAL_MODE")
            DUAL_MODE = False
        MHMup_bot = None
    else:
        MHMup_bot = MHMuserClient(
            session_file(LOGS),
            udB=udB,
            app_version=MHMup_version,
            device_model="MHMuser",
            proxy=udB.get_key("TG_PROXY"),
        )

    if not BOT_MODE:
        MHMup_bot.run_in_loop(autobot())
    else:
        if not udB.get_key("BOT_TOKEN"):
            LOGS.critical(
                '"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"'
            )

            sys.exit()

    asst = MHMuserClient(None, bot_token=udB.get_key("BOT_TOKEN"), udB=udB)

    if BOT_MODE:
        MHMup_bot = asst
        if udB.get_key("OWNER_ID"):
            try:
                MHMup_bot.me = MHMup_bot.run_in_loop(
                    MHMup_bot.get_entity(udB.get_key("OWNER_ID"))
                )
            except Exception as er:
                LOGS.exception(er)
    elif not asst.me.bot_inline_placeholder:
        MHMup_bot.run_in_loop(enable_inline(MHMup_bot, asst.me.username))

    vcClient = vc_connection(udB, MHMup_bot)

    _version_changes(udB)

    HNDLR = udB.get_key("HNDLR") or "."
    DUAL_HNDLR = udB.get_key("DUAL_HNDLR") or "/"
    SUDO_HNDLR = udB.get_key("SUDO_HNDLR") or HNDLR
else:
    print("pyMHMuser 2022 © MHMuser")

    from logging import getLogger

    LOGS = getLogger("pyMHMuser")

    MHMup_bot = asst = udB = vcClient = None
