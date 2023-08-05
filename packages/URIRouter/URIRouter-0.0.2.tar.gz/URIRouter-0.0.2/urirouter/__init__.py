import functools
from urllib.parse import urlparse


# TODO: eliminate all print statements with better logging


class _Route:

    __instances__: list = []

    def __new__(cls, route, func, *args, **kwargs):
        for instance in cls.__instances__:
            if instance.comparator == cls.get_comparator(route):
                raise RuntimeError("route already exists!")
                # print("returning existing instance")
                # return instance
        print("creating new instance")
        print(args, kwargs)
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
        # TODO: remove print statement w/ better logging
        print(f"new route created! {route=}, {func=}, {args=}, {kwargs=}")

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
                print("returning existing instance")
                return instance
        print("creating new instance")
        instance = super(URIRouter, cls).__new__(cls, *args, **kwargs)
        URIRouter.__instances__.append(instance)
        return instance

    def __init__(self, scheme, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheme = scheme
        self.__routes__: "list[_Route]" = []

    def route(self, route, *args, **kwargs):
        print("handling route")
        parsed = urlparse(route)
        built_uri = f"{self.scheme}://{parsed.netloc}{parsed.path}"
        def decorator(func):
            print("in func")
            # TODO: only create route (1) if scheme matches and (2) if not already exists
            self.__routes__.append(_Route(built_uri, func, *args, **kwargs))
            @functools.wraps(func)
            def inner_function_handling_gateway(*args, **kwargs):
                # self.__routes__.append(_Route(uri, func))
                pass
            return inner_function_handling_gateway
        return decorator

    def handle(self, uri):
        print("attempting to handle")
        parsed = urlparse(uri)
        for route in self.__routes__:
            print(route.comparator, "=?=", _Route.get_comparator(uri))
            if route.comparator == _Route.get_comparator(uri):
                print("found!")
                for item in parsed.query.split("&"):
                    print(item)
                    key, value = item.split("=")
                    if key in route.kwargs.keys():
                        # TODO: better logging and handling
                        print("Key Exists! Overriding")
                    route.kwargs[key] = value
                route.func(*route.args, **route.kwargs)
                return True
        return False
