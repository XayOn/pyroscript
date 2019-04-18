import asyncio

from aiojobs.aiohttp import spawn
import pyrcrack


async def do_aircrack(session, args, kwargs):
    """Crack."""
    async with pyrcrack.AircrackNg() as aircrack:
        await aircrack.run(*args, **kwargs)
        session.aircrack.results = await aircrack.get_result().decode()


async def aircrack(request):
    """Crack a file

    ---
    summary: Crack with aircrack-ng
    description: Crack with aircrack-ng
    tags:
    - "crack"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Crack with aircrack-ng"
      required: true
      schema:
        type: object
        required:
          - args
          - kwargs
        properties:
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
        do_aircrack(session, arguments.pop('args', []),
                    arguments.get('kwargs', {})))
    return session.aircrack.results
