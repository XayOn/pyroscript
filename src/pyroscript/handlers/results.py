async def get_results(request):
    """Get session results

    ---
    summary: Get session results
    description: Get session results
    tags:
    - "session"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Get session results for a session_id"
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
    return request.app['sessions'][session_id]
