from contextlib import suppress
from dataclasses import asdict
import asyncio

from aiojobs.aiohttp import spawn
import pyreaver


async def do_scan(session, args, kwargs):
    """Execute scan and update results dict each second.

    Reaver will update the file each second.
    """
    async with pyreaver.Wash() as reavo:
        await reavo.run(*args, **kwargs)
        while True:
            await asyncio.sleep(1)
            with suppress(KeyError):
                session.scan.results.update(
                    {a.bssid: asdict(a)
                     for a in reavo.sorted_aps()})


async def reaver_scan(request):
    """Scan for targets.

    ---
    summary: Scan for reaver targets
    description: Scan for reaver targets on a given session
    tags:
    - "scan"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Scan for reaver targets"
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
            description: "Airodump-ng kwargs"
            example: {"interface": "wlp1s0"}
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
    session.scan.results = {}
    await spawn(
        request,
        do_scan(session, arguments.pop('args', []), arguments.get(
            'kwargs', {})))
    return session.scan.results
