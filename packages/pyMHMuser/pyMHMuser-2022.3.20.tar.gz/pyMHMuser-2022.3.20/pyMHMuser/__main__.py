# MHMuser
# Copyright (C) 2021-2022 MHMuser
#
# This file is a part of < https://github.com/Dev-MHM/MHMuser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Dev-MHM/pyMHMuser/blob/main/LICENSE>.

from . import *


def main():
    import os
    import sys
    import time

    from .functions.helper import time_formatter, updater
    from .startup.funcs import (
        WasItRestart,
        autopilot,
        customize,
        plug,
        ready,
        startup_stuff,
    )
    from .startup.loader import load_other_plugins

    # Option to Auto Update On Restarts..
    if (
        udB.get_key("UPDATE_ON_RESTART")
        and os.path.exists(".git")
        and MHMup_bot.run_in_loop(updater())
    ):
        os.system(
            "git pull -f -q && pip3 install --no-cache-dir -U -q -r requirements.txt"
        )

        os.execl(sys.executable, "python3", "-m", "pyMHMuser")

    startup_stuff()

    MHMup_bot.me.phone = None
    MHMup_bot.first_name = MHMup_bot.me.first_name

    if not MHMup_bot.me.bot:
        udB.set_key("OWNER_ID", MHMup_bot.uid)

    LOGS.info("Initialising...")

    MHMup_bot.run_in_loop(autopilot())

    pmbot = udB.get_key("PMBOT")
    manager = udB.get_key("MANAGER")
    addons = udB.get_key("ADDONS") or Var.ADDONS
    vcbot = udB.get_key("VCBOT") or Var.VCBOT

    if HOSTED_ON == "termux" and udB.get_key("EXCLUDE_OFFICIAL") is None:
        _plugins = "autocorrect autopic compressor forcesubscribe gdrive glitch instagram nsfwfilter nightmode pdftools writer youtube"
        udB.set_key("EXCLUDE_OFFICIAL", _plugins)

    load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

    suc_msg = """
            ----------------------------------------------------------------------
                MHMuser has been deployed! Visit @MHMuser for updates!!
            ----------------------------------------------------------------------
    """

    # for channel plugins
    plugin_channels = udB.get_key("PLUGIN_CHANNEL")

    # Customize MHMuser Assistant...
    MHMup_bot.run_in_loop(customize())

    # Load Addons from Plugin Channels.
    if plugin_channels:
        MHMup_bot.run_in_loop(plug(plugin_channels))

    # Send/Ignore Deploy Message..
    if not udB.get_key("LOG_OFF"):
        MHMup_bot.run_in_loop(ready())

    # Edit Restarting Message (if It's restarting)
    MHMup_bot.run_in_loop(WasItRestart(udB))

    try:
        cleanup_cache()
    except BaseException:
        pass

    LOGS.info(
        f"Took {time_formatter((time.time() - start_time)*1000)} to start •MHMuser•"
    )
    LOGS.info(suc_msg)


if __name__ == "__main__":
    main()

    asst.run()
