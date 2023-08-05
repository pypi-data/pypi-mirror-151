from .context import Context
import copy
from typing import Any, Callable
from starlette.types import Scope, Send, Receive, ASGIApp
from boltons.tbutils import ExceptionInfo
from starlette.routing import iscoroutinefunction_or_partial
from starlette.requests import *
from starlette.responses import *
from starlette.exceptions import HTTPException
from .templating import _TemplateResponse

VALID_RESPONSE_TYPES = (
    Response, 
    JSONResponse, 
    StreamingResponse, 
    PlainTextResponse,
    _TemplateResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse
)

class Handler:
    def __init__(self, handler: Callable, **kwargs: Any):
        self.handler = handler
        self.kwargs = kwargs

class ResponseHandler:
    """ A Generic Response Handler """
    def __init__(self,
        ctx: Context,
        code: int = 200,
        type: str = 'text', # can be 'json', 'view', 'text' or 'redirect'
        **kwargs) -> None:
        self.ctx = ctx
        self.type = type
        self.kwargs = kwargs
        self.ctx.code = code

    def __call__(self):
        content = self.kwargs.get('content', None)
        args = self.kwargs.get('args', {})
        if self.type == 'json':
            return self.ctx.json(content = content)

        elif self.type == 'view':
            template = args.get("template")
            return self.ctx.view(
                template = template,
                data = self.ctx.state
            )
        elif self.type == 'redirect':
            url = args.get('url')
            return self.ctx.redirect(url=url)
        else:
            return self.ctx.text(content=content)

class SolaceFlow:
    """ Creates a SolaceFlow application instance. """

    def __init__(self, ctx: Context, name: str = None):
        self.name = name
        self.stack = [] # list of handlers
        self.ctx = ctx

    def add_handler(self, handler: Callable, **kwargs: Any):
        h = Handler(handler = handler, **kwargs)
        self.stack.append(h)

    async def _run(self, ctx: Context) -> ASGIApp:
        """ run attempts to execute every handler in the flow """
        try:
            for h in self.stack:
                handler = h.handler
                kwargs = h.kwargs
                if iscoroutinefunction_or_partial(handler):
                    handler_return = await handler(ctx, **kwargs)
                else:
                    handler_return = handler(ctx, **kwargs)
                
                # # we have a return value...
                if handler_return is not None:
                    # NOTE: if we have a context object,
                    # then we need to update it before
                    # going into the next flow handler.
                    if isinstance(handler_return, Context):
                        ctx = handler_return
                    
                    # if the return value is a valid Response type,
                    # then we will immediately return, stopping any
                    # futher handlers in the flow from executing.
                    elif issubclass(type(handler_return), VALID_RESPONSE_TYPES):
                        return handler_return

        except HTTPException as e:
            args = {}
            error = e.detail
            details = ExceptionInfo.from_exc_info(*sys.exc_info())
            if self.ctx.env.type in ['dev', 'test']:
                error += "\n\n"
                error += details.get_formatted()

            if self.ctx.error.type in ['json', 'view']:
                details = details.to_dict()
                error = {"error": e.detail}
                if self.ctx.env.type in ['dev', 'test']:
                    error["details"] = details

            if self.ctx.error.type == 'view':
                self.ctx.state.errors = error
                args = self.ctx.error.args

            return ResponseHandler(
                self.ctx,
                code = e.status_code,
                type = self.ctx.error.type,
                content = error,
                args = args
            )()

        except Exception as e:
            args = {}
            error = f"ERROR: {str(e)}"
            details = ExceptionInfo.from_exc_info(*sys.exc_info())
            if self.ctx.env.type in ['dev', 'test']:
                error += "\n\n"
                error += details.get_formatted()

            if self.ctx.error.type in ['json', 'view']:
                details = details.to_dict()
                error = {"error": error}
                if self.ctx.env.type in ['dev', 'test']:
                    error["details"] = details

            if self.ctx.error.type == 'view':
                self.ctx.state.error = error
                args = self.ctx.error.args
            
            return ResponseHandler(
                self.ctx,
                code = 500,
                type = self.ctx.error.type,
                content = error,
                args = args
            )()

        return ctx

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # NOTE: this creates a "deep copy" of the context object per flow
        # This is to prevent "context collisions" that can occur by
        # sharing a single context object across the application.
        # This is more efficient than instaniating a new object for each flow.
        ctx = copy.deepcopy(self.ctx)
        ctx.request = Request(
            scope = scope,
            receive = receive,
            send = send
        )
        app = await self._run(ctx) # this should return an ASGIApp object
        await app(scope, receive, send)
