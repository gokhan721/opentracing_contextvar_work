import wrapt
from tracer.integrations.requests import RequestsIntegration

request_integration = RequestsIntegration()


def _wrapper(wrapped, instance, args, kwargs):
    return request_integration.run_and_trace(
        wrapped,
        instance,
        args,
        kwargs,
    )


def patch():
    wrapt.wrap_function_wrapper(
        'requests',
        'Session.send',
        _wrapper
    )
