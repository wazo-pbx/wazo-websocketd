# Copyright 2016-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import argparse
import ssl

from xivo.chain_map import ChainMap
from xivo.config_helper import read_config_file_hierarchy
from xivo.xivo_logging import get_log_level_by_name

logger = logging.getLogger(__name__)

_DEFAULT_CONFIG = {
    'config_file': '/etc/wazo-websocketd/config.yml',
    'extra_config_files': '/etc/wazo-websocketd/conf.d/',
    'debug': False,
    'log_level': 'info',
    'log_file': '/var/log/wazo-websocketd.log',
    'user': 'wazo-websocketd',
    'auth': {'host': 'localhost', 'port': 9497, 'prefix': None, 'https': False},
    'auth_check_strategy': 'static',
    'auth_check_static_interval': 60,
    'bus': {
        'host': 'localhost',
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
        'exchange_name': 'wazo-websocketd',
        'exchange_type': 'headers',
        'upstream_exchange_name': 'xivo',
        'upstream_exchange_type': 'topic',
    },
    'websocket': {
        'listen': '127.0.0.1',
        'port': 9502,
        'certificate': None,
        'private_key': None,
        'ping_interval': 60,
    },
}


def load_config():
    cli_config = _parse_cli_args()
    file_config = read_config_file_hierarchy(ChainMap(cli_config, _DEFAULT_CONFIG))
    reinterpreted_config = _get_reinterpreted_raw_values(
        ChainMap(cli_config, file_config, _DEFAULT_CONFIG)
    )
    return ChainMap(reinterpreted_config, cli_config, file_config, _DEFAULT_CONFIG)


def _parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--config-file', action='store', help="The path where is the config file"
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help="Log debug messages. Overrides log_level.",
    )
    parser.add_argument(
        '-u', '--user', action='store', help="The owner of the process."
    )
    parsed_args = parser.parse_args()

    result = {}
    if parsed_args.config_file:
        result['config_file'] = parsed_args.config_file
    if parsed_args.debug:
        result['debug'] = parsed_args.debug
    if parsed_args.user:
        result['user'] = parsed_args.user

    return result


def _get_reinterpreted_raw_values(config):
    result = {'websocket': {}}

    ssl_context = None
    if config['websocket']['certificate'] and config['websocket']['private_key']:
        logger.warning(
            'Using service SSL configuration is deprecated. Please use NGINX instead.'
        )
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ssl_context.load_cert_chain(
            config['websocket']['certificate'], config['websocket']['private_key']
        )
    result['websocket']['ssl'] = ssl_context

    result['log_level'] = get_log_level_by_name(config['log_level'])

    return result
