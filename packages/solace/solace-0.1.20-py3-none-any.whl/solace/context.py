from starlette.types import *
from starlette.responses import *

from solace.validator import SolaceValidator
from solace.exceptions import InvalidTypeError
from .templating import Jinja2Templates, _TemplateResponse
from .exceptions import HTTPException
from box import Box

class Context:
    
    def __init__(self):
        self.headers: dict = {}
        self.code: int = 200
        self.stores = Box({})
        self.models = Box({})
        self.state = Box({}) # state is mutable data throughout the lifecycle of a request

    # TODO: add more "shortcut" properties
    # from the request property to context

    @property
    def url(self) -> str:
        return self.request.url
    
    @property
    def method(self) -> str:
        return self.request.method
    
    @property
    def params(self) -> dict:
        return self.request.path_params
    
    @property
    def args(self) -> dict:
        return dict(self.request.query_params)
    
    async def is_json_valid(self, validator: SolaceValidator) -> bool:
        if type(validator) != SolaceValidator:
            raise InvalidTypeError("validator arg must be of type SolaceValidator")

        json_data = await self.request.json()
        return validator(json_data)

    async def is_form_valid(self, validator: SolaceValidator) -> bool:
        if type(validator) != SolaceValidator:
            raise InvalidTypeError("validator arg must be of type SolaceValidator")

        form_data = await self.request.form()
        return validator(form_data)

    # def trace(self, label: str = None):
    #     """ trace the context """
    #     if self.config.get('context_tracers_enabled') == True:
    #         caller = getframeinfo(stack()[1][0])
    #         frame = caller._asdict()
    #         if label:
    #             frame["label"] = label
    #         self.frames.append(frame)

    def text(self,
        content: typing.Any = None,
    ) -> PlainTextResponse:
        """ a plain text response """
        return PlainTextResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def json(self,
        content: typing.Any = None,
    ) -> JSONResponse:
        """ a json response """
        return JSONResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def html(self,
        content: typing.Any = None,
    ) -> HTMLResponse:
        """ an html response """
        return HTMLResponse(
            content = content,
            status_code = self.code,
            headers = self.headers
        )

    def view(self,
        template: str,
        data: dict = {}
    ) -> _TemplateResponse:
        """ a template based response """
        templates = Jinja2Templates('templates') # TODO: work on config for this...??
        return templates.TemplateResponse(
            name = template,
            context = data,
            status_code = self.code,
            headers = self.headers,
        )

    def file(self,
        path: str,
        file_name: str = None,
    ) -> FileResponse:
        """ a file response """
        return FileResponse(
            path = path,
            status_code = self.code,
            headers = self.headers,
            filename = file_name
        )

    def stream(self,
        content: typing.Any = None,    
    ) -> StreamingResponse:
        """ a streaming based response """
        return StreamingResponse(
            content = content,
            status_code = self.code,
            headers = self.headers            
        )
    
    def redirect(self,
        url,    
    ) -> StreamingResponse:
        """ a redirect response """
        self.code = 302
        return RedirectResponse(
            url = url,
            status_code = self.code,
            headers = self.headers
        )
