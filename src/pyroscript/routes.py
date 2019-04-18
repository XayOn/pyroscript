"""Routes."""
from .handlers import reaver_scan
from .handlers import aireplay
from .handlers import results
from .handlers import start_session
from .handlers import scan
from .handlers import monitor
from .handlers import reaver


def setup_routes(app):
    """Setup routes."""
    app.router.add_get('/start_session', start_session.start_session)
    app.router.add_post('/scan/airodump', scan.scan)
    app.router.add_post('/scan/reaver', reaver_scan.reaver_scan)
    app.router.add_post('/results', results.get_results)
    app.router.add_get('/interface/list', monitor.get_wifis)
    app.router.add_post('/interface/monitor', monitor.monitor_mode)
    app.router.add_post('/interface/channel', monitor.channel)
    app.router.add_post('/aireplay', aireplay.aireplay)
    app.router.add_post('/crack/reaver', reaver.reaver)
