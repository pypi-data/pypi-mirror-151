import functools
from urllib.parse import urlparse
import logging


_logger = logging.Logger(__name__)
streamFormatter = logging.Formatter("[URIRouter] %(levelname)s: %(message)s")
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(streamFormatter)
_logger.addHandler(streamHandler)


class RoutingError(Exception):
    """Exception raised for errors in routes and routing.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=None):
        self.message = message
        if message:
            _logger.error(self.message)
            super().__init__(self.message)
        else:
            super().__init__()


class _Route:

    __instances__: list = []

    def __new__(cls, route, func, *args, **kwargs):
        for instance in cls.__instances__:
            if instance.comparator == cls.get_comparator(route):
                raise RoutingError(f"attempted to register existent route ({route})")
        instance = super(_Route, cls).__new__(cls)
        _Route.__instances__.append(instance)
        return instance

    """
    {{scheme}}://{netloc}/{{path/more-path}}?{{param1=something}}&{{param2=somethingelse}}
    {{scheme}}:///{{path/more-path}}?{{param1=something}}&{{param2=somethingelse}}
    """

    # TODO: implement singleton protocol that works with *args and **kwargs

    def __init__(self, route, func, *args, **kwargs):
        self.parsed = urlparse(route)
        self.scheme = self.parsed.scheme
        self.netloc = self.parsed.netloc
        self.route = self.parsed.path
        self.func = func
        self.args = args
        self.kwargs = kwargs
        _logger.info(f"created {self}")

    def __repr__(self):
        return f"_Route(route={self.route}, func={self.func}, args={self.args}, kwargs={self.kwargs})"

    @property
    def comparator(self) -> str:
        return f"{self.scheme}://{self.netloc}{self.route}"

    @staticmethod
    def get_comparator(uri) -> str:
        parsed = urlparse(uri)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


class URIRouter:

    __instances__: list = []

    def __new__(cls, scheme, *args, **kwargs):
        for instance in cls.__instances__:
            if instance.scheme == scheme:
                _logger.warning(f"attempting to create a new URIRouter with existing scheme; URIRouter's must have unique schemes, returning existing scheme (returning the existing URIRouter instance)")
                return instance
        _logger.info(f"creating new URIRouter")
        instance = super(URIRouter, cls).__new__(cls, *args, **kwargs)
        URIRouter.__instances__.append(instance)
        return instance

    def __init__(self, scheme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, 'scheme'):
            self.scheme = scheme
        if not hasattr(self, '__routes__'):
            self.__routes__: "list[_Route]" = []

    def __repr__(self):
        return f"URIRouter('{self.scheme}://...')"

    def route(self, route, *args, **kwargs):
        """
        Register a route from a uri to a function when that uri-event occurs in a bundled app.
        :param route: //netloc/path/path2/path... or just /path/path2/path... (DO NOT END IN '/')
        :param args: optional args to pass to the function that is being decorated
        :param kwargs: optional kwargs to pass to the function that is being decorated
        """
        _logger.debug(f"registering route {route}")
        parsed = urlparse(route)
        built_uri = f"{self.scheme}://{parsed.netloc}{parsed.path}"
        def decorator(func):
            self.__routes__.append(_Route(built_uri, func, *args, **kwargs))
            _logger.debug(f"registered route {route}")
            @functools.wraps(func)
            def inner_function_handling_gateway(*args, **kwargs):
                pass
            return inner_function_handling_gateway
        return decorator

    def handle(self, uri) -> bool:
        """
        Handle an incoming uri and its parameters.
        :param uri: the incoming uri.
        :return: True, if a registered route is found; False, if a registered route is not found
        """
        _logger.info(f"{self} received uri: {uri}")
        parsed = urlparse(uri)
        for route in self.__routes__:
            _logger.debug(f"{route.comparator} =?= {_Route.get_comparator(uri)}")
            if route.comparator == _Route.get_comparator(uri):
                _logger.info(f"{self} found a route for {uri}")
                for item in parsed.query.split("&"):
                    _logger.debug(f"got kwarg in uri: {item}")
                    key, value = item.split("=")
                    if key in route.kwargs.keys():
                        _logger.warning(f"'{key}' already exists in kwargs; overriding its value with '{value}'")
                    route.kwargs[key] = value
                route.func(*route.args, **route.kwargs)
                return True
        _logger.warning(f"{self} failed to find a route for {uri}")
        return False
