#!/usr/bin/env python

import os
import importlib.machinery as im
import importlib.util as iu

class RebuildGreaseStyles(object):
    def __init__(self):
        self.config_dir = self.get_config_dir()
        self.stylemap = self.import_stylemap(self.config_dir)

    def get_config_dir(self):
        config_dir = os.getenv('QUTE_CONFIG_DIR')
        if config_dir: return config_dir

        dir = os.getenv('XDG_CONFIG_HOME')
        if dir: return dir + '/qutebrowser'

        dir = os.getenv('HOME', '~')
        return dir + '/.config/qutebrowser'

    def import_stylemap(self, config_dir):
        loader = im.SourceFileLoader('stylemap', f"{config_dir}/stylemap.py")
        spec = iu.spec_from_loader( 'stylemap', loader )
        if spec:
            stylemap = iu.module_from_spec( spec )
            loader.exec_module( stylemap )
            return stylemap.styles

    def create_grease_scripts_from_css_files(self):
        if not self.stylemap: return

        for css_filename, patterns in self.stylemap.items():
            self.create_grease_script_from_css_file(css_filename, patterns)

    def create_grease_script_from_css_file(self, css_filename, patterns):
        with open(f'{self.config_dir}/styles/{css_filename}') as css_file:
            css = css_file.read()

        grease = self.css_to_grease(css_filename, css, patterns)

        grease_script_path = f'{self.config_dir}/greasemonkey/{css_filename}.js'
        with open(grease_script_path, 'w') as grease_file:
            grease_file.write(grease)

    def css_to_grease(self, css_filename, css, patterns):
        includes = '\n'.join([f'// @include    {p}' for p in patterns])

        return (
              '// ==UserScript==\n'
            + f'// @name    Userstyle ({css_filename})\n'
            + includes + '\n'
            + '// ==/UserScript==\n'
            + f'GM_addStyle(`{css}`)'
        )

def reload():
   fifo = os.getenv('QUTE_FIFO')
   
   if not fifo: return

   with open(fifo, 'w') as feefifofam:
       feefifofam.write('greasemonkey-reload -q\n')
       feefifofam.write('reload\n')


if __name__ == "__main__":
    RebuildGreaseStyles().create_grease_scripts_from_css_files()
    reload()
