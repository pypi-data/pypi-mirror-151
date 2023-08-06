import asyncio
from functools import partial
from typing import Type, Union

from aiohttp import web
from jj import default_app, default_handler
from jj.middlewares import SelfMiddleware
from jj.mock import Mock
from jj.resolvers import Registry, ReversedResolver
from jj.runners import AppRunner
from jj.servers import Server
from vedro.core import Dispatcher, Plugin, PluginConfig
from vedro.events import CleanupEvent, StartupEvent

__all__ = ("RemoteMock", "RemoteMockPlugin",)


class _Mock(Mock):
    pass


class RemoteMockPlugin(Plugin):
    def __init__(self, config: Type["RemoteMock"]) -> None:
        super().__init__(config)
        self._server: Union[Server, None] = None
        self._host = config.host
        self._port = config.port

    def subscribe(self, dispatcher: Dispatcher) -> None:
        dispatcher.listen(StartupEvent, self.on_startup) \
                  .listen(CleanupEvent, self.on_cleanup)

    def _create_server(self) -> Server:
        resolver = ReversedResolver(Registry(), default_app, default_handler)
        runner = partial(AppRunner, resolver=resolver, middlewares=[SelfMiddleware(resolver)])
        return Server(asyncio.get_event_loop(), runner, web.TCPSite)  # type: ignore

    async def on_startup(self, event: StartupEvent) -> None:
        self._server = self._create_server()
        self._server.start(_Mock(), self._host, self._port)

    async def on_cleanup(self, event: CleanupEvent) -> None:
        if self._server is None:
            return
        for runner in reversed(self._server._runners):
            await runner.cleanup()


class RemoteMock(PluginConfig):
    plugin = RemoteMockPlugin

    host: str = "0.0.0.0"
    port: int = 8080
