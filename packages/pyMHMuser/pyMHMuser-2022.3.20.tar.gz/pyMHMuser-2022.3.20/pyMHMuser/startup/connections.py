# MHMuser
# Copyright (C) 2021-2022 MHMuser
#
# This file is a part of < https://github.com/Dev-MHM/MHMuser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Dev-MHM/pyMHMuser/blob/main/LICENSE>.

import sys

from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.sessions import StringSession

from ..configs import Var
from . import *
from .BaseClient import MHMuserClient


def session_file(logger):
    if Var.SESSION:
        if len(Var.SESSION.strip()) != 353:
            logger.exception("Wrong string session. Copy paste correctly!")
            sys.exit()
        return StringSession(Var.SESSION)
    logger.exception("No String Session found. Quitting...")
    sys.exit()


def vc_connection(udB, MHMup_bot):
    VC_SESSION = Var.VC_SESSION or udB.get_key("VC_SESSION")
    if VC_SESSION and VC_SESSION != Var.SESSION:
        try:
            return MHMuserClient(
                StringSession(VC_SESSION), log_attempt=False, handle_auth_error=False
            )
        except (AuthKeyDuplicatedError, EOFError):
            LOGS.info(
                "Your VC_SESSION Expired. Deleting VC_SESSION from redis..."
                + "\nRenew/Change it to Use Voice/Video Chat from VC Account..."
            )
            udB.del_key("VC_SESSION")
        except Exception as er:
            LOGS.info("While creating Client for VC.")
            LOGS.exception(er)
    return MHMup_bot
