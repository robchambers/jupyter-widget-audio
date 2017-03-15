from ._version import version_info, __version__

from .audio import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'jupyter-widget-audio',
        'require': 'jupyter-widget-audio/extension'
    }]
