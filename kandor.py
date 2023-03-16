#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools
import logging
import configparser
import io
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_SERVER_HOST = 'localhost'

DEFAULT_SERVER_PORT = 4800

DEFAULT_LOG_NAME = 'kandor'

DEFAULT_LOG_LEVEL = 'INFO'


@functools.cache
def load_config():
    """Lee la configuración desde el fichero Kandor.ini.

    Si no existe, asume algunos valores predefinidos:

    - Servidor por defecto : localhost
    - Puerto por defecto: 5800
    - Nivel de log: INFO
    """
    config = configparser.ConfigParser()
    config.read('kandor.ini')
    if 'core' not in config:
        config.add_section('core')
    core = config['core']
    log_name = core.get('log_name', DEFAULT_LOG_NAME)
    log_level = core.get('log_level', DEFAULT_LOG_LEVEL)
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    server_host = core.get('server_host', DEFAULT_SERVER_HOST)
    server_port = core.getint('server_port', DEFAULT_SERVER_PORT)
    return {
        'address': (server_host, server_port),
        'logger': logger,
    }


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):  # NoQA
        logger = load_config().get('logger')
        message = (
            f'{self.command} from {self.client_address}'
            f' requesting path {self.path}'
            )
        logger.debug(message)
        body = message.encode('utf-8')
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    do_POST = do_GET


def main():
    """Main server function.
    """
    config = load_config()
    print(config)
    logger = config['logger']
    address = config['address']
    logger.info('Kandor API simulator starts')
    logger.info('waiting connections at %s:%s', *address)
    httpd = HTTPServer(address, RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
