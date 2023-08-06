from jupyter_server.utils import url_path_join

from .transform_view import TransformJupyterRouteHandler
from .autocomplete_view import AutoCompleteRouteHandler
from .check_status_view import CheckStatusRouterHandler
from .accept_view import AcceptRouterHandler
from .decline_view import DeclineRouterHandler

TRANSFORM_NB_ROUTE = "TRANSFORM_NB"
AUTOCOMPLETE_ROUTE = "AUTOCOMPLETE"
CHECK_STATUS = "CHECK_STATUS"
ACCEPT_FILE = "ACCEPT_FILE"
DECLINE_FILE = "DECLINE_FILE"


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    url_path = "jupyterlab-mutableai"

    autocomplete_route_pattern = url_path_join(
        base_url, url_path, AUTOCOMPLETE_ROUTE)

    transform_jupyter_route_pattern = url_path_join(
        base_url, url_path, TRANSFORM_NB_ROUTE
    )

    check_status_jupyter_route_pattern = url_path_join(
        base_url, url_path, CHECK_STATUS
    )

    accept_jupyter_route_pattern = url_path_join(
        base_url, url_path, ACCEPT_FILE
    )

    decline_jupyter_route_pattern = url_path_join(
        base_url, url_path, DECLINE_FILE
    )

    handlers = [
        (autocomplete_route_pattern, AutoCompleteRouteHandler),
        (transform_jupyter_route_pattern, TransformJupyterRouteHandler),
        (check_status_jupyter_route_pattern, CheckStatusRouterHandler),
        (accept_jupyter_route_pattern, AcceptRouterHandler),
        (decline_jupyter_route_pattern, DeclineRouterHandler),
    ]

    web_app.add_handlers(host_pattern, handlers)
