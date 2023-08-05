import dataclasses
import inspect
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    List,
)

from fastapi import APIRouter, params, Response, Depends
from fastapi.types import DecoratedCallable
from fastapi.datastructures import DefaultPlaceholder, Default
from fastapi.responses import JSONResponse
from starlette.routing import Route
from fastapi.routing import APIRoute
from nextx.dependency_injection import Factory, __mappings__
from inject import autoparams, instance
from dataclasses import dataclass


ROUTER_KEY = "__api_router__"
ENDPOINT_KEY = "__endpoint_api_key__"


class ApiController(APIRouter):
    """
    Registers endpoints for both a non-trailing-slash and a trailing slash.
    In regards to the exported API schema only the non-trailing slash will be included.

    Examples:

        @router.get("", include_in_schema=False) - not included in the OpenAPI schema,
        responds to both the naked url (no slash) and /

        @router.get("/some/path") - included in the OpenAPI schema as /some/path,
        responds to both /some/path and /some/path/

        @router.get("/some/path/") - included in the OpenAPI schema as /some/path,
        responds to both /some/path and /some/path/

    Co-opted from https://github.com/tiangolo/fastapi/issues/2060#issuecomment-974527690
    """

    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        given_path = path
        path_no_slash = given_path[:-1] if given_path.endswith("/") else given_path

        add_nontrailing_slash_path = super().api_route(
            path_no_slash, include_in_schema=include_in_schema, **kwargs
        )

        add_trailing_slash_path = super().api_route(
            path_no_slash + "/", include_in_schema=False, **kwargs
        )

        def add_path_and_trailing_slash(func: DecoratedCallable) -> DecoratedCallable:
            add_trailing_slash_path(func)
            return add_nontrailing_slash_path(func)

        return (
            add_trailing_slash_path
            if given_path == "/"
            else add_path_and_trailing_slash
        )


__controllers__: List[ApiController] = []

T = TypeVar("T")


SetIntStr = Set[Union[int, str]]
DictIntStrAny = Dict[Union[int, str], Any]


@dataclass
class RouteArgs:
    """The arguments APIRouter.add_api_route takes.

    Just a convenience for type safety and so we can pass all the args needed by the underlying FastAPI route args via
    `**dataclasses.asdict(some_args)`.
    """

    path: str
    response_model: Optional[Type[Any]] = None
    status_code: Optional[int] = None
    tags: Optional[List[str]] = None
    dependencies: Optional[Sequence[params.Depends]] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    response_description: str = "Successful Response"
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None
    deprecated: Optional[bool] = None
    methods: Optional[Union[Set[str], List[str]]] = None
    operation_id: Optional[str] = None
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    include_in_schema: bool = True
    response_class: Union[Type[Response], DefaultPlaceholder] = Default(JSONResponse)
    name: Optional[str] = None
    route_class_override: Optional[Type[APIRoute]] = None
    callbacks: Optional[List[Route]] = None
    openapi_extra: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True


def post(path: str, **kwargs):
    def decorator(fn: Callable[..., Any]):
        endpoint = RouteArgs(path=path, methods=["POST"], **kwargs)
        setattr(fn, ENDPOINT_KEY, endpoint)
        return fn

    return decorator


def get(path: str, **kwargs):
    def decorator(fn: Callable[..., Any]):
        endpoint = RouteArgs(path=path, methods=["GET"], **kwargs)
        setattr(fn, ENDPOINT_KEY, endpoint)
        return fn

    return decorator


def delete(path: str, **kwargs):
    def decorator(fn: Callable[..., Any]):
        endpoint = RouteArgs(path=path, methods=["DELETE"], **kwargs)
        setattr(fn, ENDPOINT_KEY, endpoint)
        return fn

    return decorator


def put(path: str, **kwargs):
    def decorator(fn: Callable[..., Any]):
        endpoint = RouteArgs(path=path, methods=["PUT"], **kwargs)
        setattr(fn, ENDPOINT_KEY, endpoint)
        return fn

    return decorator


def patch(path: str, **kwargs):
    def decorator(fn: Callable[..., Any]):
        endpoint = RouteArgs(path=path, methods=["PATCH"], **kwargs)
        setattr(fn, ENDPOINT_KEY, endpoint)
        return fn

    return decorator


def controller(*args, **kwargs) -> Type[Callable[[Type[T]], Type[T]]]:
    """
    Returns a decorator that makes a Class-Based-View (or a controller)
    out of a regular python class.

    `args` and `kwargs` are used to create the underlying FastAPI Router
    (actually an instance of an ApiController), that will be registered
    on server creation.

    Decorated class should not define constructor arguments, other than
    dependencies. All arguments would be treated as injection parameters, and
    type-hints would be used as interface-resolvers for this dependencies.

    This decorator effectively decorates the class constructor with
    `inject.autoparams()` so any non-resolved dependency would
    issue an exception at runtime.

    Controllers should be imported before `Server` creation, so the controller
    is registered and properly initialized.

    When defining endpoints, dependency injection at endpoint-level should
    behave as expected in FastAPI

    Example
    =======

    >>> @controller(prefix='/controller-test', tags=['My Controller'])
    >>> class UsersController:
    >>>     def __init__(self, user_service: IUserService):
    >>>         self.user_service = user_service
    >>>
    >>>     @get('/{user_id}')
    >>>     async def get_users(self, user_id: str = Path(...)):
    >>>         return await self.user_service.get_by_id(user_id)
    """
    router = ApiController(*args, **kwargs)

    def decorator(cls: Type[T]):
        # inject the underlying router in the class
        return _controller(router, cls)

    return decorator


def _controller(router: ApiController, cls: Type[T]) -> Type[T]:
    """
    Replaces any methods of the provided class `cls` that are endpoints
    with updated function calls that will properly inject an instance of
    `cls`
    """
    # Make this class constructor based injectable
    wrapper = autoparams()
    cls = wrapper(cls)

    # get all functions from cls
    function_members = inspect.getmembers(cls, inspect.isfunction)
    functions_set = set(func for _, func in function_members)

    # filter to get only endpoints
    endpoints = [f for f in functions_set if getattr(f, ENDPOINT_KEY, None) is not None]

    for endpoint in endpoints:
        _fix_endpoint_signature(cls, endpoint)
        # Add the corrected function to the router
        args: RouteArgs = getattr(endpoint, ENDPOINT_KEY)
        router.add_api_route(endpoint=endpoint, **dataclasses.asdict(args))

    # register the router
    __controllers__.append(router)
    return cls


def _fix_endpoint_signature(cls: Type[Any], endpoint: Callable[..., Any]):
    old_signature = inspect.signature(endpoint)
    old_parameters: List[inspect.Parameter] = list(old_signature.parameters.values())
    old_first_parameter = old_parameters[0]

    # Here we replace the function signature from:
    # >>> Class Test:
    # >>>   @post('/')
    # >>>   async def do_something(self, item: Item):
    # >>>       ...
    # To:

    # >>> Class Test:
    # >>>   @post('/')
    # >>>   async def do_something(self = Depends(Factory(Test)), item: Item):
    # >>>       ...

    # With this new signature, FastAPI will instantiate the self argument
    # with each HTTP method call, and because of the `Factory(cls)` returns
    # a parameterless constructor, FastAPI will know that this does not require
    # any dependency and will not document it.
    # For this to work, `cls` must effectively be wrapped on inject.autoparams(),
    # so it tries to inject all the constructor arguments at runtime
    new_self_parameter = old_first_parameter.replace(default=Depends(Factory(cls)))
    new_parameters = [new_self_parameter] + [
        parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY)
        for parameter in old_parameters[1:]
    ]

    new_signature = old_signature.replace(parameters=new_parameters)
    setattr(endpoint, "__signature__", new_signature)
