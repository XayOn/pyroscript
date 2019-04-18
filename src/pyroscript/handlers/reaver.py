from contextlib import suppress
from dataclasses import asdict
import asyncio

from aiojobs.aiohttp import spawn
import pyreaver


async def do_crack(session, args, kwargs):
    """Execute crack and update results dict each second.

    Reaver will update the file each second.
    """
    async with pyreaver.Reaver() as reavo:
        await reavo.run(*args, **kwargs)
        # TODO: we need to have some way to stop the process.
        while True:
            with suppress(KeyError):
                session.crack.results = reavo.meta['result']['lines']
            await asyncio.sleep(1)


async def reaver(request):
    """Crack with reaver

    ---
    summary: Crack with reaver
    description: Crack with reaver
    tags:
    - "crack"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Crack reaver targets"
      required: true
      schema:
        type: object
        required:
          - args
          - kwargs
          - session_id
        properties:
          session_id:
            description: "Session ID previously requested."
            type: string
            example: "session_id"
          args:
            type: array
            description: "reaver args"
            example: []
          kwargs:
            type: object
            description: "reaver kwargs"
            example: {"interface": "wlp1s0", "bssid": "XXX"}
    produces:
      - application/json
    responses:
      200:
        description: All OK.
      500:
        description: Unknown exception
      400:
        description: Bad request
    """
    arguments = await request.json()
    session_id = arguments.pop('session_id')
    session = request.app['sessions'][session_id]
    session.crack.results = {}
    await spawn(
        request,
        do_crack(session, arguments.pop('args', []), arguments.get(
            'kwargs', {})))
    return session.crack.results
