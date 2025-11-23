import uvicorn

from gateway.application.app import create_app
from gateway.core.settings import get_settings

app = create_app()

if __name__ == "__main__":
    s = get_settings()
    uvicorn.run(app, host="0.0.0.0", port=s.http_port)
