#!/usr/bin/env python

import os
import sys
import hashlib
from urllib.parse import urlparse

class Darkreader(object):
    def __init__(self):
        self.config_dir = self.get_config_dir()

    def get_config_dir(self):
        config_dir = os.getenv('QUTE_CONFIG_DIR')
        if config_dir: return config_dir

        dir = os.getenv('XDG_CONFIG_HOME')
        if dir: return dir + '/qutebrowser'

        dir = os.getenv('HOME', '~')
        return dir + '/.config/qutebrowser'

    def get_scriptpath(self, url_pattern):
        url_pattern_md5 = hashlib.md5(url_pattern.encode('utf-8'))
        grease_filename = f'darkreader-{url_pattern_md5.hexdigest()}.js'
        return f'{self.config_dir}/greasemonkey/{grease_filename}'

    def enable(self, url, url_pattern, brightness, contrast, sepia):
        script = self.create_grease(url, url_pattern, brightness, contrast, sepia)
        with open(self.get_scriptpath(url_pattern), 'w') as grease_file:
            grease_file.write(script)

    def disable(self, url_pattern):
        os.remove(self.get_scriptpath(url_pattern))

    def create_grease(self, url, url_pattern, brightness, contrast, sepia):
        return (
              '// ==UserScript==\n'
            + f'// @name          Dark Reader ({url_pattern})\n'
            + '// @run-at        document-end\n'
            + '// @grant         none\n'
            + f'// @include       {url_pattern}\n'
            + '// @require       https://cdn.jsdelivr.net/npm/darkreader/darkreader.min.js\n'
            + '// ==/UserScript==\n'
            + f'// original url: {url}\n'
            + 'DarkReader.setFetchMethod(window.fetch);'
            + 'DarkReader.enable({\n'
            + f'	brightness: {brightness},\n'
            + f'	contrast: {contrast},\n'
            + f'	sepia: {sepia}\n'
            + '});'
        )

def reload():
   fifo = os.getenv('QUTE_FIFO')
   
   if not fifo: return

   with open(fifo, 'w') as feefifofam:
       feefifofam.write('greasemonkey-reload -q\n')
       feefifofam.write('reload\n')

def get_domain_pattern():
    url = os.getenv('QUTE_URL')
    domain = urlparse(url).netloc
    return f'*{domain}*'

if __name__ == "__main__":
    darkreader = Darkreader()

    sys.argv.pop(0)
    type = sys.argv.pop(0)
    url = os.getenv('QUTE_URL')
    url_pattern = sys.argv.pop(0)
    if url_pattern == 'domain': url_pattern = get_domain_pattern()

    defaults = {
        'brightness': 90,
        'contrast':   90,
        'sepia':      50
    }

    brightness = sys.argv.pop(0) if sys.argv else defaults['brightness']
    contrast   = sys.argv.pop(0) if sys.argv else defaults['contrast']
    sepia      = sys.argv.pop(0) if sys.argv else defaults['sepia']

    if type == 'disable':
        darkreader.disable(url_pattern)
    else:
        darkreader.enable(url, url_pattern, brightness, contrast, sepia)

    reload()
