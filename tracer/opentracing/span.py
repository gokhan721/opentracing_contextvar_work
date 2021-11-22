import time
from threading import Lock

import opentracing


class FastapiSpan(opentracing.Span):

    def __init__(self,
                 tracer,
                 operation_name=None,
                 context=None,
                 tags=None,
                 start_time=None):
        super(FastapiSpan, self).__init__(tracer, context)
        self._context = context
        self._lock = Lock()
        self.operation_name = operation_name if operation_name is not None else ""
        self.start_time = start_time or int(time.time() * 1000)
        self.finish_time = 0
        self.tags = tags if tags is not None else {}

    @property
    def context(self):
        return self._context

    @property
    def span_id(self):
        return self._context.span_id

    def set_operation_name(self, operation_name):
        with self._lock:
            self.operation_name = operation_name
        return super(FastapiSpan, self).set_operation_name(operation_name)

    def set_tag(self, key, value):
        with self._lock:
            if self.tags is None:
                self.tags = {}
            self.tags[key] = value
        return super(FastapiSpan, self).set_tag(key, value)

    def get_tag(self, key):
        if self.tags is not None:
            return self.tags.get(key)
        return None

    def finish(self, f_time=None):
        with self._lock:
            self.finish_time = int(time.time() * 1000) if f_time is None else f_time

    def set_error_to_tag(self, err):
        error_type = type(err)
        self.set_tag('error', True)
        self.set_tag('error.kind', error_type.__name__)
        self.set_tag('error.message', str(err))

    def get_duration(self):
        if self.finish_time == 0:
            return int(time.time() * 1000) - self.start_time
        else:
            return self.finish_time - self.start_time

    def erroneous(self):
        return self.tags is not None and 'error' in self.tags
