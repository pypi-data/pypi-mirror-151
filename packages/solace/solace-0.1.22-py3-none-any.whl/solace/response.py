from .context import Context
from .flow import ResponseHandler

def response_handler(ctx: Context, **kwargs):
    """ Handle responses... duh """
    return ResponseHandler(ctx, **kwargs)()
