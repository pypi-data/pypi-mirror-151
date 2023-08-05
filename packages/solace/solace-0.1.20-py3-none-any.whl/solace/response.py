from .context import Context
from .flow import ResponseHandler
from .exceptions import HTTPException

def error_handler(ctx: Context):
    """ Handle Errors """
    if hasattr(ctx.error, 'message'):
        code = 500
        if hasattr(ctx.error, 'code'):
            code = ctx.error.code
        raise HTTPException(
            detail = ctx.error.message,
            status_code = code
        )

def response_handler(ctx: Context, **kwargs):
    """ Handle responses... duh """
    return ResponseHandler(ctx, **kwargs)()
