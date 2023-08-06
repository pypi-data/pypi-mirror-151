# MHMuser
# Copyright (C) 2021-2022 MHMuser
#
# This file is a part of < https://github.com/Dev-MHM/MHMuser/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/Dev-MHM/pyMHMuser/blob/main/LICENSE>.

"""
Exceptions which can be raised by pyMHMuser Itself.
"""


class pyMHMuserError(Exception):
    ...


class TelethonMissingError(ImportError):
    ...


class DependencyMissingError(ImportError):
    ...


class RunningAsFunctionLibError(pyMHMuserError):
    ...
