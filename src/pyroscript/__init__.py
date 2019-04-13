"""Main app."""

import configparser
import logging
import uuid

from .routes import setup_routes

from aiohttp import ClientSession
from aiohttp import web
from aiohttp_apiset import SwaggerRouter
from aiohttp_apiset.middlewares import jsonify
from aiohttp_sentry import SentryMiddleware
from aiojobs.aiohttp import setup

from cleo import Command
from cleo import Application

import pygogo


@web.middleware
async def log_middleware(request, handler):
    """Logging middleware"""
    request['logger'] = request.app['logger'].get_logger(uid=uuid.uuid4())
    return await handler(request)


def get_app(options):
    """Get app."""
    router = SwaggerRouter(swagger_ui='/swagger/')

    app = web.Application(
        router=router,
        middlewares=[
            jsonify,
            SentryMiddleware(),
            log_middleware,
        ],
    )

    app['logger'] = pygogo.Gogo(
        __name__,
        low_formatter=pygogo.formatters.structured_formatter,
        verbose=options.option('debug'))

    if options.option('debug'):
        logging.basicConfig(level=logging.DEBUG)

    app['sessions'] = {}
    app['logger'].get_logger().debug("starting")
    app['config'] = configparser.ConfigParser()
    app['config'].read(options.option('config') or '')
    setup(app)

    setup_routes(app)
    return app


class PyroscriptServerCommand(Command):
    """Starts api service.

    start_server
        {--host=0.0.0.0 : Host to listen on}
        {--port=8081 : Port to listen on}
        {--config=config.ini : Config file}
        {--debug : Debug and verbose mode}
    """

    def handle(self):
        """Handle command."""
        app = get_app(self)
        web.run_app(
            app, host=self.option('host'), port=int(self.option('port')))


def main():
    """Main."""
    application = Application()
    application.add(PyroscriptServerCommand())
    application.run()
