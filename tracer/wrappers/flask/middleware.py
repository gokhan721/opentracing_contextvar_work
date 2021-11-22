from tracer.wrappers.flask.flask_wrapper import FlaskWrapper

class FlaskMiddleware:
    def __init__(self):
        self._wrapper = FlaskWrapper()

    def set_app(self, app):
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_request(self.teardown_request)

    def before_request(self):
        try:
            from flask import request
            self._wrapper.before_request(request)
        except Exception as e:
            print("Error during the before part: {}".format(e))

    def after_request(self, response):
        try:
            self._wrapper.after_request(response)
        except Exception as e:
            print("Error setting response to context: {}".format(e))
        return response

    def teardown_request(self, exception):
        try:
            self._wrapper.teardown_request(exception)
        except Exception as e:
            print("Error during the request teardown: {}".format(e))
