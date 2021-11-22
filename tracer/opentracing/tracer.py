import uuid
import opentracing
from tracer.opentracing.span import FastapiSpan
from tracer.opentracing.span_context import FastapiSpanContext
from opentracing.scope_managers.contextvars import ContextVarsScopeManager



class FastapiTracer(opentracing.Tracer):
    __instance = None
    

    @staticmethod
    def get_instance():
        return FastapiTracer() if FastapiTracer.__instance is None else FastapiTracer.__instance


    def __init__(self, scope_manager=None):
        scope_manager = ContextVarsScopeManager()
        super(FastapiTracer, self).__init__(scope_manager)
        FastapiTracer.__instance = self

    def start_active_span(self,
                          operation_name,
                          span_id=None,
                          tags=None,
                          start_time=None,
                          ignore_active_span=False,
                          finish_on_close=True):
        span_id = span_id or str(uuid.uuid4())
        _span = self.start_span(operation_name=operation_name,
                                span_id=span_id,
                                tags=tags,
                                start_time=start_time,
                                ignore_active_span=ignore_active_span)
        return self.scope_manager.activate(_span, finish_on_close)

    def start_span(self,
                   operation_name=None,
                   span_id=None,
                   tags=None,
                   start_time=None,
                   ignore_active_span=False):
        # Create a new span
        _span = self.create_span(operation_name=operation_name,
                                 span_id=span_id,
                                 tags=tags,
                                 start_time=start_time,
                                 ignore_active_span=ignore_active_span)
        return _span

    def create_span(self,
                    operation_name=None,
                    span_id=None,
                    tags=None,
                    start_time=None,
                    ignore_active_span=False):

        _span_id = span_id or str(uuid.uuid4())

        _context = FastapiSpanContext(span_id=_span_id,)
        _span = FastapiSpan(self,
                            operation_name=operation_name,
                            context=_context,
                            tags=tags,
                            start_time=start_time)

        return _span

    def get_active_span(self):
        scope = self.scope_manager.active
        if scope is not None:
            return scope.span

        return None