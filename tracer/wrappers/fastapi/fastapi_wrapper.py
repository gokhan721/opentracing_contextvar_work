import time
from tracer.opentracing.tracer import FastapiTracer

class FastapiWrapper:    
    __instance = None
    
    @staticmethod
    def get_instance():
        return FastapiWrapper() if FastapiWrapper.__instance is None else FastapiWrapper.__instance

    def __init__(self):
        FastapiWrapper.__instance = self


    def before_request(self, request):
        tracer = FastapiTracer.get_instance()
        scope = tracer.start_active_span(operation_name=request.get('path'),
                                    start_time=time.time(),
                                    finish_on_close=False)
        print(scope.span.span_id)


    def after_request(self):
        tracer = FastapiTracer.get_instance()
        scope = tracer.scope_manager.active
        root_span = scope.span
        try:
            root_span.finish(f_time=time.time())
        except Exception as e:
            print("Error occured after request of fastapi: {}".format(e))
            pass
        finally:
            try:
                scope.close()
            except Exception as e:
                print("Error occured while closing scope: {}".format(e))
                pass