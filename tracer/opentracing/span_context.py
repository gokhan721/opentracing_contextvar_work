import opentracing


class FastapiSpanContext(opentracing.SpanContext):

    def __init__(self,
                 span_id=None):
        self._span_id = span_id

    @property
    def span_id(self):
        return self._span_id

    @span_id.setter
    def span_id(self, value):
        self._span_id = value
