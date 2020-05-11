#! /usr/local/bin/python
"""
Description: This is a sample FastAPI web service.

Title: main.py

Author: theStygianArchitect
"""
import os
import sys
from socket import gethostname
from socket import gethostbyname

try:
    import uvicorn
    from fastapi import FastAPI
    from fastapi.openapi.utils import get_openapi
    from starlette.middleware.cors import CORSMiddleware
    from starlette.responses import RedirectResponse
except ModuleNotFoundError as module_not_found_error:
    print(module_not_found_error)
    print('Please install required packages')
    sys.exit(1)

try:
    from logger import set_up_stream_logging
except ModuleNotFoundError:
    from app.logger import set_up_stream_logging  # type: ignore

app = FastAPI()  # pylint: disable=C0103,E1101
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['*'],
                   allow_headers=['*'])

log = set_up_stream_logging(__file__)  # pylint: disable=C0103


def custom_openapi():
    """Define customized openAPI."""
    description = """This is a custom description"""
    openapi_schema = get_openapi(
        title='New Title',
        version='0.1.0',
        description=description,
        routes=app.routes
        # openapi_prefix='Endpoints'
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema


@app.get('/health_check')
async def health_check():
    """Perform health check."""
    result = {'status': 'Ok'}
    log.info(result)
    return result


@app.get('/')
async def index():
    """Redirect to docs page."""
    response = RedirectResponse(url='/docs')
    return response


def main():
    """Run server."""
    custom_openapi()
    local_ip_address = gethostbyname(gethostname())
    local_port = 8080
    os.environ['HOST'] = f"{local_ip_address}"
    os.environ['PORT'] = f"{local_port}"
    os.environ['BIND'] = f"{local_ip_address}:{local_port}"
    uvicorn.run(app, host=local_ip_address, port=local_port, timeout_notify=120)


if __name__ == '__main__':
    main()
