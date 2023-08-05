# URIRouter
Creates an object-oriented structure and decorators similar to Flask, but for handling internal URIs. 

## Format
URIRouter uses a minimum of two parts to add a route, a scheme and parameter(s). Optionally, there can also be a net location. Any parameters will be treated as ```kwargs``` and passed to the function that the route decorates.

```{{scheme}}:///{{path/more-path}}?{{param1=something}}&{{param2=somethingelse}}``` uses ```.route("/path/more/path")``` and will add to ```kwargs``` the parameters ```{'param1':'something', 'param2':'somethingelse'}```

```{{scheme}}://{netloc}/{{path/more-path}}?{{param1=something}}&{{param2=somethingelse}}```

## Example Application Class
URIRouter can be used to handle any in-bound URIs, but it is intended to be used with a structure that can accept events with callbacks, such as:
```
from urirouter import URIRouter
from PySide6.QtCore import QEvent, QUrl
from PySide6.QtWidgets import QApplication


router = URIRouter("myappscheme")


class CustomURIApplication(QApplication):

    def __init__(self, router: URIRouter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.router = router

    def event(self, e):
        """Handle macOS FileOpen events or pass to super."""
        if e.type() == QEvent.FileOpen:
            url: QUrl = e.url()
            if url.isValid():
                self.router.handle(url.url())
            else:
                print(f"application received invalid uri: {url.errorString()}")
        else:
            return super().event(e)
        return True

if __name__ == "__main__":
    app = CustomURIApplication(router)
    # see quickstart to install routes
```

## Quickstart
Note: the quickstart requires a way to handle in-bound URIs, either with a ```NSApplication``` (such as with ```pyobjc```) or a ```QApplication``` (such as ```PySide6```). See the **Example Application Class** section above for an example with ```QApplication```.
```
from urirouter import URIRouter


router = URIRouter("myappscheme")


@router.route("/")
def home(*args, **kwargs):
    print("in home")
    print(kwargs) # any parameters contained in the URI are passed to the function in kwargs


if __name__ == "__main__":
    inbound_uri = ... # get/handle in-bound URIs (see Example Application Class above)
    router.handle(inbound_uri)
```