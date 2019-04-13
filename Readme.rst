Pyroscript
==========

Aircrack-ng HTTP API.

Exposes a session-based api that handles aircrack-ng suite background processes.
See swagger for API info and examples at /swagger/


::

        USAGE
          poetry run pyroscript start_server [--host <...>] [--port <...>] [--config <...>] [--debug]

        OPTIONS
          --host                 Host to listen on (default: "0.0.0.0")
          --port                 Port to listen on (default: "8081")
          --config               Config file (default: "config.ini")
          --debug                Debug and verbose mode

        GLOBAL OPTIONS
          -h (--help)            Display this help message
          -q (--quiet)           Do not output any message
          -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
          -V (--version)         Display this application version
          --ansi                 Force ANSI output
          --no-ansi              Disable ANSI output
          -n (--no-interaction)  Do not ask any interactive question


Example usage with httpie
==========================

This examples requires httpie and jq ( https://httpie.org/ and https://stedolan.github.io/jq/ )

Create a session::

        $> SESSION_ID=$(http post http://localhost:8082/start_session|jq -r .session_id)

Get a list of wireless interfaces::

        $> http get http://localhost:8082/interface/list

        HTTP/1.1 200 OK
        Content-Length: 178
        Content-Type: application/json; charset=utf-8
        Date: Sat, 13 Apr 2019 10:55:09 GMT
        Server: Python/3.7 aiohttp/3.5.4

        [
            {
                "chipset": "Intel Corporation Dual Band Wireless-AC 3165 Plus Bluetooth (rev 99)",
                "driver": "iwlwifi",
                "interface": "wlp1s0",
                "phy": "phy0"
            }
        ]

Put interface in monitor mode::

        $> http post http://localhost:8082/interface/monitor interface=wlp1s0mon

        HTTP/1.1 200 OK
        Content-Length: 591
        Content-Type: application/json; charset=utf-8
        Date: Sat, 13 Apr 2019 10:57:13 GMT
        Server: Python/3.7 aiohttp/3.5.4

        {
            "results": [
                {
                    "chipset": "Intel Corporation Dual Band Wireless-AC 3165 Plus Bluetooth (rev 99)",
                    "driver": "iwlwifi",
                    "interface": "wlp1s0",
                    "phy": "phy0"
                },
                {
                    "chipset": null,
                    "driver": null,
                    "interface": "(mac80211 monitor mode vif enabled for [phy0]wlp1s0 on [phy0]wlp1s0mon)",
                    "phy": ""
                },
                {
                    "chipset": null,
                    "driver": null,
                    "interface": "(mac80211 station mode vif disabled for [phy0]wlp1s0)",
                    "phy": ""
                }
            ],
            "set_monitor": true
        }


Start scan::

       $> http post http://localhost:8082/scan session_id=$SESSION_ID args:='["wlp1s0mon"]' kwargs:={}

       HTTP/1.1 200 OK
       Content-Length: 2
       Content-Type: application/json; charset=utf-8
       Date: Sat, 13 Apr 2019 10:58:48 GMT
       Server: Python/3.7 aiohttp/3.5.4

       {}


Get scan results::

        $> http post http://localhost:8082/scan/results session_id=$SESSION_ID

        HTTP/1.1 200 OK
        Content-Length: 21954
        Content-Type: application/json; charset=utf-8
        Date: Sat, 13 Apr 2019 10:59:19 GMT
        Server: Python/3.7 aiohttp/3.5.4

        {
            "00:00:00:XX:XX:XX": {
                "authentication": "PSK",
                "beacons": "4",
                "bssid": "00:00:00:XX:XX:XX",
                "channel": "1",
                "cipher": "CCMP",
                "clients": [
                    {
                        "bssid": "3C:98:72:XX:XX:XX",
                        "first_time_seen": "2019-04-13 12:58:55",
                        "last_time_seen": "2019-04-13 12:58:55",
                        "packets": "7",
                        "power": "-69",
                        "probed_essids": "",
                        "station_mac": "00:00:00:XX:XX:XX"
                    }
                ],
                "essid": "TEST-111",
                "first_time_seen": "2019-04-13 12:58:48",
                "id_length": "20",
                "iv": "0",
                "key": "",
                "lan_ip": "0.  0.  0.  0",
                "last_time_seen": "2019-04-13 12:58:55",
                "power": "-87",
                "privacy": "WPA2",
                "speed": "54"
            }
        }

