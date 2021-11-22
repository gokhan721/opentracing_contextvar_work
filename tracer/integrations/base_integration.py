import abc
import traceback

from tracer.opentracing.tracer import FastapiTracer

ABC = abc.ABCMeta('ABC', (object,), {})


class BaseIntegration(ABC):
    def run_and_trace(self, wrapped, instance, args, kwargs):
        tracer = FastapiTracer.get_instance()
        if not tracer.get_active_span():
            return wrapped(*args, **kwargs)

        response = None
        exception = None

        scope = tracer.start_active_span(operation_name=self.get_operation_name(wrapped, instance, args, kwargs),
                                         finish_on_close=False)
        # Inject before span tags
        try:
            self.before_call(scope, wrapped, instance, args, kwargs, response, exception)
        except Exception as e:
            scope.span.set_tag('instrumentation_error', "Error")

        try:
            response = self.actual_call(wrapped, args, kwargs)
        except Exception as e:
            exception = e

        try:
            self.after_call(scope, wrapped, instance, args, kwargs, response, exception)
        except Exception as e:
            scope.span.set_tag('instrumentation_error', "Error")

        try:
            scope.span.finish()
        except Exception as e:
            if exception is None:
                exception = e
            else:
                print(str(e))

        scope.close()

        if exception is not None:
            scope.span.set_error_to_tag(exception)
            raise exception

        return response

    def actual_call(self, wrapped, args, kwargs):
        return wrapped(*args, **kwargs)

    @abc.abstractmethod
    def get_operation_name(self, wrapped, instance, args, kwargs):
        raise Exception("should be implemented")

    @abc.abstractmethod
    def before_call(self, scope, wrapped, instance, args, kwargs, response, exception):
        raise Exception("should be implemented")

    def after_call(self, scope, wrapped, instance, args, kwargs, response, exception):
        if exception is not None:
            self.set_exception(exception, traceback.format_exc(), scope.span)
