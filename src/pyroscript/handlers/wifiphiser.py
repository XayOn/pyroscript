import asyncio
from pathlib import Path
from aiojobs.aiohttp import spawn
from pyrcrack.executor import ExecutorHelper


class WifiPhiser(ExecutorHelper):
    """ usage: wifiphisher [-h] [-i INTERFACE] [-eI EXTENSIONSINTERFACE]
                   [-aI APINTERFACE] [-iI INTERNETINTERFACE]
                   [-iAM MAC_AP_INTERFACE] [-iEM MAC_EXTENSIONS_INTERFACE]
                   [-iNM] [-kN] [-nE] [-nD]
                   [-dC DEAUTH_CHANNELS [DEAUTH_CHANNELS ...]] [-e ESSID]
                   [-dE DEAUTH_ESSID] [-p PHISHINGSCENARIO] [-pK PRESHAREDKEY]
                   [-hC HANDSHAKE_CAPTURE] [-qS] [-lC] [-lE LURE10_EXPLOIT]
                   [--logging] [-dK] [-lP LOGPATH] [-cP CREDENTIAL_LOG_PATH]
                   [--payload-path PAYLOAD_PATH] [-cM] [-wP]
                   [-wAI WPSPBC_ASSOC_INTERFACE] [-kB] [-fH]
                   [-pPD PHISHING_PAGES_DIRECTORY]
                   [--dnsmasq-conf DNSMASQ_CONF] [-pE PHISHING_ESSID]

    Options:
      -h, --help            show this help message and exit
      --interface INTERFACE
                        Manually choose an interface that supports both AP and
                        monitor modes for spawning the rogue AP as well as
                        mounting additional Wi-Fi attacks from Extensions
                        (i.e. deauth). Example: -i wlan1
      --extensionsinterface EXTENSIONSINTERFACE
                        Manually choose an interface that supports monitor
                        mode for deauthenticating the victims. Example: -eI
                        wlan1
      --apinterface APINTERFACE
                        Manually choose an interface that supports AP mode for
                        spawning the rogue AP. Example: -aI wlan0
      --internetinterface INTERNETINTERFACE
                        Choose an interface that is connected on the
                        InternetExample: -iI ppp0
      --mac-ap-interface MAC_AP_INTERFACE
                        Specify the MAC address of the AP interface
      --mac-extensions-interface MAC_EXTENSIONS_INTERFACE
                        Specify the MAC address of the extensions interface
      --no-mac-randomization
                       Do not change any MAC address
      --keepnetworkmanager
                       Do not kill NetworkManager
      --noextensions   Do not load any extensions.
      --nodeauth       Skip the deauthentication phase.
      --deauth-channels DEAUTH_CHANNELS [DEAUTH_CHANNELS ...]
      --essid ESSID
                        Enter the ESSID of the rogue Access Point. This option
                        will skip Access Point selection phase. Example:
                        --essid 'Free WiFi'
      --deauth-essid DEAUTH_ESSID
                        Deauth all the BSSIDs in the WLAN with that ESSID.
      --phishingscenario PHISHINGSCENARIO
                        Choose the phishing scenario to run.This option will
                        skip the scenario selection phase. Example: -p
                        firmware_upgrade
      --presharedkey PRESHAREDKEY
                        Add WPA/WPA2 protection on the rogue Access Point.
                        Example: -pK s3cr3tp4ssw0rd
      --handshake-capture HANDSHAKE_CAPTURE
                        Capture of the WPA/WPA2 handshakes for verifying
                        passphraseExample : -hC capture.pcap
      --quitonsuccess  Stop the script after successfully retrieving one pair
                        of credentials
      --lure10-capture
                        Capture the BSSIDs of the APs that are discovered
                        during AP selection phase. This option is part of
                        Lure10 attack.
      --lure10-exploit LURE10_EXPLOIT
                        Fool the Windows Location Service of nearby Windows
                        users to believe it is within an area that was
                        previously captured with --lure10-capture. Part of the
                        Lure10 attack.
      --logging             Log activity to file
      --disable-karma  Disables KARMA attack
      --logpath LOGPATH
                        Determine the full path of the logfile.
      --credential-log-path CREDENTIAL_LOG_PATH
                        Determine the full path of the file that will store
                        any captured credentials
      --payload-path PAYLOAD_PATH
                        Payload path for scenarios serving a payload
      --channel-monitor
                       Monitor if target access point changes the channel.
      --wps-pbc        Monitor if the button on a WPS-PBC Registrar is
                       pressed.
      --wpspbc-assoc-interface WPSPBC_ASSOC_INTERFACE
                            The WLAN interface used for associating to the WPS
                            AccessPoint.
      --known-beacons  Broadcast a number of beacon frames advertising
                            popular WLANs
      --force-hostapd  Force the usage of hostapd installed in the system
      --phishing-pages-directory PHISHING_PAGES_DIRECTORY
                            Search for phishing pages in this location
      --dnsmasq-conf DNSMASQ_CONF
                        Determine the full path of a custom dnmasq.conf file
      --phishing-essid PHISHING_ESSID
                        Determine the ESSID you want to use for the phishing
                        page
    """  # noqa
    requires_tempfile = False
    requires_tempdir = True
    command = "wifiphisher"

    async def run(self, *args, **kwargs):
        """Run async, with prefix stablished as tempdir."""
        asyncio.create_task(self.result_updater())
        return await super().run(*args, **kwargs)

    async def result_updater(self):
        """Set result on local object."""
        while not self.proc:
            await asyncio.sleep(1)

        while self.proc.returncode is None:
            # log_path = self.tempdir_path / 'wifiphisher.log'
            log_path = Path('wifiphisher.log')
            self.meta['result'] = log_path.read_text().splitlines()
            await asyncio.sleep(2)


async def do_wifiphiser(session, args, kwargs):
    """Crack."""
    async with WifiPhiser() as wifiphiser:
        await wifiphiser.run(*args, **kwargs)
        while True:
            await asyncio.sleep(1)
            session.wifiphiser.results = wifiphiser.meta


async def wifiphiser(request):
    """Run wifiphiser

    ---
    summary: Run wifiphiser
    description: Run wifiphiser
    tags:
    - "phising"
    consumes:
    - "application/json"
    produces:
    - "application/json"
    parameters:
    - in: "body"
      name: "body"
      description: "Run wifiphiser"
      required: true
      schema:
        type: object
        required:
          - args
          - kwargs
          - session_id
        properties:
          args:
            type: array
            description: "args"
          kwargs:
            type: object
            description: "kwargs"
          session_id:
            type: string
            description: session id
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
        do_wifiphiser(session, arguments.pop('args', []),
                      arguments.get('kwargs', {})))
    return session.wifiphiser.results
