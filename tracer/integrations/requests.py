from opentracing import Format
from tracer.integrations.base_integration import BaseIntegration


class RequestsIntegration(BaseIntegration):

    def __init__(self):
        pass

    def get_operation_name(self, wrapped, instance, args, kwargs):
        prepared_request = args[0]
        return prepared_request.url

    def before_call(self, scope, wrapped, instance, args, kwargs, response, exception):
        pass

    def after_call(self, scope, wrapped, instance, args, kwargs, response, exception):
        pass