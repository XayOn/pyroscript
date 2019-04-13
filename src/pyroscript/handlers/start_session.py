from uuid import uuid4
from dotmap import DotMap


async def start_session(request):
    """Start a new session

    ---
    summary: Get a session id
    description: Get a session_id
    tags:
    - "sessions"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    responses:
      200:
        description: All OK.
      500:
        description: Unknown exception
      400:
        description: Bad request
    """
    uuid = uuid4()
    request.app['sessions'][str(uuid)] = DotMap()
    return {'session_id': uuid}
