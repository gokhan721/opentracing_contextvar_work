import wrapt
from tracer.wrappers.flask.middleware import FlaskMiddleware


def _wrapper(wrapped, instance, args, kwargs):
    response = wrapped(*args, **kwargs)
    try:
        middleware = FlaskMiddleware()
        middleware.set_app(instance)
    except:
        pass
    return response


def patch():
    wrapt.wrap_function_wrapper(
        'flask',
        'Flask.__init__',
        _wrapper
    )
