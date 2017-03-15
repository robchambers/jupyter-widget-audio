import ipywidgets as widgets
import os
from traitlets import Unicode, Bool, Integer

from IPython.utils.py3compat import (string_types, #cast_bytes_py2, cast_unicode,
                                     unicode_type)

@widgets.register('audio.Audio')
class Audio(widgets.DOMWidget):
    """"""
    _view_name = Unicode('AudioView').tag(sync=True)
    _model_name = Unicode('AudioModel').tag(sync=True)
    _view_module = Unicode('jupyter-widget-audio').tag(sync=True)
    _model_module = Unicode('jupyter-widget-audio').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    value = Unicode('Audio World!').tag(sync=True)
    data = Unicode()
    url = Unicode().tag(sync=True)
    embed = Bool()
    rate = Integer()
    autoplay = Bool()

    def __init__(self, data=None, filename=None, url=None, embed=None, rate=None, autoplay=False, **kwargs):
        # if filename is None and url is None and data is None:
        #     raise ValueError("No image data found. Expecting filename, url, or data.")
        # if embed is False and url is None:
        #     raise ValueError("No url found. Expecting url when embed=False")
        #
        # if url is not None and embed is not True:
        #     self.embed = False
        # else:
        #     self.embed = True
        self.autoplay = autoplay
        self.initdata(data=data, url=url, filename=filename)
        super(Audio, self).__init__(**kwargs)

        if self.data is not None and not isinstance(self.data, bytes):
            self.data = self._make_wav(data, rate)

    def initdata(self, data=None, url=None, filename=None):
        """
        Parameters
        ----------
        data : unicode, str or bytes
            The raw data or a URL or file to load the data from
        url : unicode
            A URL to download the data from.
        filename : unicode
            Path to a local file to load the data from.
        """
        if data is not None and isinstance(data, string_types):
            if data.startswith('http') and url is None:
                url = data
                filename = None
                data = None
            elif _safe_exists(data) and filename is None:
                url = None
                filename = data
                data = None

        self.data = data
        self.url = url
        self.filename = None if filename is None else unicode_type(filename)

        self.reload()
        self._check_data()

    # def __repr__(self):
    #     if not self._show_mem_addr:
    #         cls = self.__class__
    #         r = "<%s.%s object>" % (cls.__module__, cls.__name__)
    #     else:
    #         r = super(DisplayObject, self).__repr__()
    #     return r


    def reload(self):
        """Reload the raw data from file or URL."""
        if self.filename is not None:
            with open(self.filename, self._read_flags) as f:
                self.data = f.read()
        elif self.url is not None:
            try:
                try:
                    from urllib.request import urlopen  # Py3
                except ImportError:
                    from urllib2 import urlopen
                response = urlopen(self.url)
                self.data = response.read()
                # extract encoding from header, if there is one:
                encoding = None
                for sub in response.headers['content-type'].split(';'):
                    sub = sub.strip()
                    if sub.startswith('charset'):
                        encoding = sub.split('=')[-1].strip()
                        break
                # decode data, if an encoding was specified
                if encoding:
                    self.data = self.data.decode(encoding, 'replace')
            except:
                self.data = None

    def _make_wav(self, data, rate):
        """ Transform a numpy array to a PCM bytestring """
        import struct
        from io import BytesIO
        import wave

        try:
            import numpy as np

            data = np.array(data, dtype=float)
            if len(data.shape) == 1:
                nchan = 1
            elif len(data.shape) == 2:
                # In wave files,channels are interleaved. E.g.,
                # "L1R1L2R2..." for stereo. See
                # http://msdn.microsoft.com/en-us/library/windows/hardware/dn653308(v=vs.85).aspx
                # for channel ordering
                nchan = data.shape[0]
                data = data.T.ravel()
            else:
                raise ValueError('Array audio input must be a 1D or 2D array')
            scaled = np.int16(data / np.max(np.abs(data)) * 32767).tolist()
        except ImportError:
            # check that it is a "1D" list
            idata = iter(data)  # fails if not an iterable
            try:
                iter(idata.next())
                raise TypeError('Only lists of mono audio are '
                                'supported if numpy is not installed')
            except TypeError:
                # this means it's not a nested list, which is what we want
                pass
            maxabsvalue = float(max([abs(x) for x in data]))
            scaled = [int(x / maxabsvalue * 32767) for x in data]
            nchan = 1

        fp = BytesIO()
        waveobj = wave.open(fp, mode='wb')
        waveobj.setnchannels(nchan)
        waveobj.setframerate(rate)
        waveobj.setsampwidth(2)
        waveobj.setcomptype('NONE', 'NONE')
        waveobj.writeframes(b''.join([struct.pack('<h', x) for x in scaled]))
        val = fp.getvalue()
        waveobj.close()

        return val

    # def _data_and_metadata(self):
    #     """shortcut for returning metadata with url information, if defined"""
    #     md = {}
    #     if self.url:
    #         md['url'] = self.url
    #     if md:
    #         return self.data, md
    #     else:
    #         return self.data
    #
    # def _repr_html_(self):
    #     src = """
    #             <audio controls="controls" {autoplay}>
    #                 <source src="{src}" type="{type}" />
    #                 Your browser does not support the audio element.
    #             </audio>
    #           """
    #     return src.format(src=self.src_attr(), type=self.mimetype, autoplay=self.autoplay_attr())
    #
    # def src_attr(self):
    #     import base64
    #     if self.embed and (self.data is not None):
    #         data = base64 = base64.b64encode(self.data).decode('ascii')
    #         return """data:{type};base64,{base64}""".format(type=self.mimetype,
    #                                                         base64=data)
    #     elif self.url is not None:
    #         return self.url
    #     else:
    #         return ""
    #
    # def autoplay_attr(self):
    #     if (self.autoplay):
    #         return 'autoplay="autoplay"'
    #     else:
    #         return ''

def _safe_exists(path):
    """Check path, but don't let exceptions raise"""
    try:
        return os.path.exists(path)
    except Exception:
        return False