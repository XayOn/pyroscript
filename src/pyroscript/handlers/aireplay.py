from contextlib import suppress
from dataclasses import asdict
import asyncio

from aiojobs.aiohttp import spawn
import pyrcrack


async def do_aireplay(session, interface, args, kwargs):
    """Execute aireplay and update results dict each 1.1 seconds."""
    # Execute aireplay
    async with pyrcrack.AireplayNg() as aireplay:
        await aireplay.run(interface, *args, **kwargs)
        while True:
            await asyncio.sleep(1)
            with suppress(KeyError):
                session.aireplay.results = aireplay.meta['results']


async def aireplay(request):
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
          - interface
        properties:
          interface:
            description: "Monitor mode interface"
            type: string
          args:
            type: array
            description: "Aireplay-ng args"
            example: ["wlp1s0"]
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
        do_aireplay(session, arguments['interface'], arguments.pop('args', []),
                    arguments.get('kwargs', {})))
    return session.aireplay.results


async def get_scan_results(request):
    """Get session scan results

    ---
    summary: Get scan results
    description: Get scan results
    tags:
    - "scan"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Get scan results for a session_id"
      required: true
      schema:
        type: object
        required:
          - session_id
        properties:
          session_id:
            description: "Session ID previously requested."
            type: string
            example: "session_id"
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
    return request.app['sessions'][session_id].scan.results
