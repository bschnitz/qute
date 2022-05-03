#!/usr/bin/env python

import os
import sys
import hashlib

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

    def enable(self, url_pattern, brightness, contrast, sepia):
        script = self.create_grease(url_pattern, brightness, contrast, sepia)
        with open(self.get_scriptpath(url_pattern), 'w') as grease_file:
            grease_file.write(script)

    def disable(self, url_pattern):
        os.remove(self.get_scriptpath(url_pattern))

    def create_grease(self, url_pattern, brightness, contrast, sepia):
        return (
              '// ==UserScript==\n'
            + f'// @name          Dark Reader ({url_pattern})\n'
            + '// @run-at        document-end\n'
            + '// @grant         none\n'
            + f'// @include       {url_pattern}\n'
            + '// @require       https://cdn.jsdelivr.net/npm/darkreader/darkreader.min.js\n'
            + '// ==/UserScript==\n'
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

if __name__ == "__main__":
    darkreader = Darkreader()
    url_pattern = sys.argv[2]
    brightness = 90 if len(sys.argv) < 3 else sys.argv[2]
    contrast = 90 if len(sys.argv) < 4 else sys.argv[3]
    sepia = 0 if len(sys.argv) < 5 else sys.argv[4]
    if sys.argv[1] == 'disable':
        darkreader.disable(url_pattern)
    else:
        darkreader.enable(url_pattern, brightness, contrast, sepia)
