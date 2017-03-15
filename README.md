jupyter-widget-audio
===============================

Audio player widget modeled on audio Display object.

Installation
------------

To install use pip:

    $ pip install ipywidgetaudio
    $ jupyter nbextension enable --py --sys-prefix ipywidgetaudio


For a development installation (requires npm),

    $ git clone https://github.com/robchambers/jupyter-widget-audio.git
    $ cd jupyter-widget-audio
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipywidgetaudio
    $ jupyter nbextension enable --py --sys-prefix ipywidgetaudio
