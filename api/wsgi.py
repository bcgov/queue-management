from gevent import monkey
import os

# Monkey patch to allow for async actions (aka multiple workers)
monkey.patch_all()

from qsystem import application, socketio


def _env_flag(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    debug = _env_flag("WSGI_DEBUG", True)
    host = os.environ.get("WSGI_HOST", "0.0.0.0")
    port = int(os.environ.get("WSGI_PORT", "5000"))
    use_reloader = _env_flag("WSGI_USE_RELOADER", False)

    print(
        "Starting socketio app"
        + f" with debug={debug}, host={host}, port={port}, reloader={use_reloader}"
    )
    socketio.run(
        application,
        host=host,
        port=port,
        debug=debug,
        use_reloader=use_reloader,
    )
