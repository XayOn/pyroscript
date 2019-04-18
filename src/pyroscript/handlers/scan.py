from contextlib import suppress
from dataclasses import asdict
import asyncio
from glob import glob

from aiojobs.aiohttp import spawn
import pyrcrack


async def do_scan(session, args, kwargs):
    """Execute scan and update results dict each 1.1 seconds.

    Airodump-ng will update the file each second.
    """
    async with pyrcrack.AirodumpNg() as pdump:
        kwargs.update({'write_interval': 1})
        await pdump.run(*args, **kwargs)
        while True:
            await asyncio.sleep(1.1)
            with suppress(KeyError):
                session.scan.result_files = glob(pdump.tempdir.name + '/*')
                session.scan.results.update(
                    {a.bssid: asdict(a)
                     for a in pdump.sorted_aps()})


async def scan(request):
    """Scan for targets.

        ---
    summary: Scan for targets
    description: Scan for targets on a given session
    tags:
    - "scan"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Scan for targets"
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
            description: "Airodump-ng args"
            example: ["wlan0"]
          kwargs:
            type: object
            description: "Airodump-ng kwargs"
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
