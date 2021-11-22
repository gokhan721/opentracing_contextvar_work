RESPONSE_REDIRECT_STATUS_CODE = 307

class FastapiMiddleware(object):
    def __init__(self, app, wrapper):
        self.app = app
        self._wrapper = wrapper

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        try:
            self._wrapper.before_request(scope)
        except Exception as e:
            print("Error during the before part of fastapi: {}".format(e))

        def handle_response(message):
            try:
                if "status" in message and message.get("status") == RESPONSE_REDIRECT_STATUS_CODE:
                    scope["res_redirected"] = True
                if message and message.get("type") == "http.response.start" and message.get("status") != 307:
                    scope["res_redirected"] = False
                elif message and message.get("type") == "http.response.body" and not scope["res_redirected"]:
                    try:
                        if not message.get("more_body") or message.get("more_body") == False:
                            self._wrapper.after_request()
                    except Exception as e:
                        print("Error during the after part of fastapi: {}".format(e))
            except Exception as e:
                print("Error during getting res body in fast api: {}".format(e))
    

        async def wrapped_send(message):
            handle_response(message)
            await send(message)


        async def wrapped_receive():
            try:
                req = await receive()
            except Exception as e:
                print("Error during receive request fast api asgi function: {}".format(e))
                raise e
            return req

        try:
            await self.app(scope, wrapped_receive, wrapped_send)
        except Exception as e:
            print("Error in the app fastapi: {}".format(e))
            raise e