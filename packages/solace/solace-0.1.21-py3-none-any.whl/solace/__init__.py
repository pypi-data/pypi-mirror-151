from starlette.types import ASGIApp
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from .flow import SolaceFlow
from .context import Context
from .importer import import_from_string
from .response import response_handler, error_handler
from .store import store_handler
from .model import model_handler, data_handler

class Solace:
    """ Creates an ASGI Application Instance """

    def __init__(self, config):
        self.config = config()
        self.app = Starlette()
        self._process_operations()
    
    def _process_operations(self):
        """ register operations on the app instance """
        for operation in self.config.operations:
            ctx = Context()

            # NOTE: this is the start of error management
            if hasattr(self.config, 'error'):
                ctx.error = self.config.error
            
            if hasattr(self.config, 'env'):
                ctx.env = self.config.env

            flow = SolaceFlow(ctx, operation.name)
            
            if hasattr(self.config, 'stores'):
                for store in self.config.stores:
                    kwargs = self.config.stores.get(store)
                    kwargs['store'] = store
                    flow.add_handler(store_handler, **kwargs)
            
            methods = ['GET']
            
            # NOTE: if we're performing a save operation,
            # we will always ensure that a "payload" property
            # is set on context.
            if operation.type == 'save':
                methods = ['POST', 'PUT']
                flow.add_handler(data_handler)
                if hasattr(self.config, 'models'):
                    for model in self.config.models:
                        kwargs = self.config.models.get(model)
                        kwargs['model'] = model
                        flow.add_handler(model_handler, **kwargs)
            
            if operation.type == 'void':
                methods = ['GET', 'POST', 'DELETE']

            if hasattr(operation, 'flow'):
                for h in operation.flow:
                    handler = import_from_string(h)
                    flow.add_handler(handler)

            flow.add_handler(error_handler)
            flow.add_handler(response_handler, **operation.res)

            r = Route(
                path = operation.path,
                endpoint = flow,
                methods = methods
            )
            self.app.routes.append(r)

    def __call__(self) -> ASGIApp:
        if hasattr(self.config, 'static_assets'):
            url = 'static'
            dir = 'static'
            if hasattr(self.config.static_assets, 'url'):
                url = self.config.static_assets.url
            if hasattr(self.config.static_assets, 'dir'):
                dir = self.config.static_assets.dir
            
            if not url.startswith("/"):
                url = f"/{url}"
            
            self.app.routes.append(Mount(url, 
                app = StaticFiles(
                    directory = dir
                ), name = "static" 
            ))
        return self.app