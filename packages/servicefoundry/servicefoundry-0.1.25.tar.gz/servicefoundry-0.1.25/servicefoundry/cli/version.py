from importlib_metadata import version

try:
    __version__ = version(__name__)
except Exception:
    __version__ = "NA"
