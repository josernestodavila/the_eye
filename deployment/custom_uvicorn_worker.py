from uvicorn.workers import UvicornWorker


class CustomWorker(UvicornWorker):
    """
    Custom configuration for UvicornWorker
    taken from https://github.com/encode/uvicorn/issues/266
    """

    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
        "lifespan": "off",
    }
