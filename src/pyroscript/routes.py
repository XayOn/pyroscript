"""Routes."""
from .handlers import start_session
from .handlers import scan
from .handlers import monitor


def setup_routes(app):
    """Setup routes."""
    app.router.add_post('/start_session', start_session.start_session)
    app.router.add_post('/scan', scan.scan)
    app.router.add_post('/scan/results', scan.get_scan_results)
    app.router.add_get('/interface/list', monitor.get_wifis)
    app.router.add_post('/interface/monitor', monitor.monitor_mode)
