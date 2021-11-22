from tracer.integrations.modules.fastapi import patch as fastapi_patch
from tracer.integrations.modules.flask import patch as flask_patch
from tracer.integrations.modules.requests import patch as requests_patch

requests_patch()
fastapi_patch()
flask_patch()
