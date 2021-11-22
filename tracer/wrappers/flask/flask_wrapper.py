import time
from tracer.opentracing.tracer import FastapiTracer

try:
    from flask import request, g
except ImportError:
    request = None
    g = None


class FlaskWrapper:

    def __init__(self):
        pass

    def before_request(self, _request):
        tracer = FastapiTracer.get_instance()
        scope = tracer.start_active_span(operation_name=_request.path,
                                    start_time=time.time(),
                                    finish_on_close=False)
        print(scope.span.span_id)
    
    def after_request(self, response):
        return response

    def teardown_request(self, exception=None):
        tracer = FastapiTracer.get_instance()
        scope = tracer.scope_manager.active
        root_span = scope.span
        try:
            root_span.finish(f_time=time.time())
        except Exception:
            # TODO: handle root span finish errors
            pass
        finally:
            try:
                scope.close()
            except Exception as e:
                print("Error occured while closing scope: {}".format(e))
                pass