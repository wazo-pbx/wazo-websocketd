# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class NoTokenError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class AuthenticationExpiredError(AuthenticationError):
    pass


class SessionProtocolError(Exception):
    pass


class BusConnectionError(Exception):
    pass


class BusConnectionLostError(BusConnectionError):
    pass


class UnsupportedVersionError(Exception):
    pass
