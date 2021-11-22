import wrapt

def _wrapper(wrapped, instance, args, kwargs):
    from fastapi.middleware import Middleware
    from tracer.wrappers.fastapi.middleware import FastapiMiddleware
    from tracer.wrappers.fastapi.fastapi_wrapper import FastapiWrapper
    middlewares = kwargs.pop("middleware", [])
    middlewares.insert(0, Middleware(FastapiMiddleware, wrapper=FastapiWrapper.get_instance()))
    kwargs.update({"middleware": middlewares})
    wrapped(*args, **kwargs)


def patch():
    wrapt.wrap_function_wrapper(
        "fastapi.applications",
        "FastAPI.__init__",
        _wrapper
    )