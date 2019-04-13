import pyrcrack


async def get_wifis(request):
    """Get a list of wireless interfaces

    ---
    summary: Get a list of capable wireless interface
    description: Get a list of capable wireless interfaces
    tags:
    - interfaces
    """
    async with pyrcrack.AirmonNg() as airmon:
        return await airmon.list_wifis()


async def monitor_mode(request):
    """Set interface in monitor mode.

    ---
    summary: Set monitor mode
    description: Set monitor mode
    tags:
    - "interfaces"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Set monitor mode"
      required: true
      schema:
        type: object
        required:
          - interface
        properties:
          interface:
            description: "Wifi interface"
            type: string
            example: "wlan0"
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
    wifi = (await request.json())['interface']
    async with pyrcrack.AirmonNg() as airmon:
        assert wifi in (a['interface'] for a in (await airmon.list_wifis()))
        return {'set_monitor': True, 'results': await airmon.set_monitor(wifi)}


async def channel(request):
    """Channel

    ---
    summary: Set channel
    description: Set channel
    tags:
    - "interfaces"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Set channel"
      required: true
      schema:
        type: object
        required:
          - interface
          - channel
        properties:
          channel:
            description: "Channel"
            type: string
            example: "1"
          interface:
            description: "Wifi interface"
            type: string
            example: "wlan0"
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
    results = await request.json()
    wifi = results['interface']
    channel = results['channel']
    async with pyrcrack.AirmonNg() as airmon:
        assert wifi in (a['interface'] for a in (await airmon.list_wifis()))
        return {
            'set_monitor': True,
            'results': await airmon.set_monitor(wifi, channel)
        }
