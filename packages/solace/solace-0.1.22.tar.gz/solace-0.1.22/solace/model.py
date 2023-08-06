from .context import Context
from .validator import SolaceValidator
from box import Box

async def data_handler(ctx: Context):
    form = await ctx.request.form()
    form = dict(form)
    if bool(form):
        ctx.state.payload = form
        return ctx
    
    if not bool(form):
        json = await ctx.request.json()
        if bool(json):
            ctx.state.payload = json
            return ctx
        
        if not bool(json):
            ctx.state.payload = {}
            return ctx


def model_handler(ctx: Context, **kwargs):
    model = kwargs.get('model')
    resource = SolaceValidator(kwargs.get('schema'))
    
    ctx.models[model] = Box({})
    ctx.models[model].is_valid = resource(ctx.state.payload)
    ctx.models[model].errors = resource.errors
