**If you don't know qutebrowser, the best keyboard driven webbrowser on this
planet, [check it out](https://www.qutebrowser.org/)!**

# Userscripts for Qutebrowser

A very enthusiastic description for currently two userscripts:

1. [Per Domain Stylesheets](#stylesheets)
2. [(Per Domain) Darkreader](#darkreader)

For an introduction to userscripts in qutebrowser open
[qute://help/userscripts.html](qute://help/userscripts.html) from within
qutebrowser.

## Per Domain Stylesheets for Qutebrowser {#stylesheets}

Currently qutebrowser does not natively support per-domain stylesheets. So to
trick it to have some kind of per-domain stylesheets, one can use greasmonkey
scripts, which just load styles for the specified domains. This repo contains
the `rebuild-qutebrowser-grease-styles.py` userscript to facilitate this task.

### Installation and Usage

This repo mirrors part of the config directory of qutebrowser, which is located
depending on your environment e.g. at `~/.config/qutebrowser`. Following files
shall be copied to it (while retaining relative pathes):
```
stylemap.py
styles/qute.help.css
userscripts/rebuild-qutebrowser-grease-styles.py
```
Stylesheets can now be copied to the `styles` directory, as an example it
already contains dark theme styles for the qutebrowser help pages. *Please
excuse this bad example. Unfortunatly I'm not really good at styling.*

After that styles can be configured per domain by appending to the styles
dictionary in the `stylemap.py` file. Each key of the dictionary represents a
file from the `styles` directory, while the value is an array of url patterns
for which the style shall be applied.

Now the only thing left to do is to execute the userscript. This can be done
from within qutebrowser of course
```
spawn --userscript rebuild-qutebrowser-grease-styles.py
```
as well as by executing the script directly from a terminal (provided all
environment variables are set correctly):
```
python3 rebuild-qutebrowser-grease-styles.py
```
The script will just build a userscript for each stylesheet and place it under
the greasemonkey directory under the config directory of qutebrowser.
Of course it may be convenient to add a mapping to your config.py, e.g.:
```
config.bind(',s', 'spawn --userscript rebuild-qutebrowser-grease-styles.py', mode='normal')
```
Note that this perfectly eases the developement flow when developing user
stylesheets. All you need is to edit and save the stylesheet and then execute
the userscript in qutebrowser again, which will not only regenerate the
greasemonkey scripts, but also reload them in qutebrowser afterwards and reload
the current page.

### Notes

The 'pseudo' per-domain user stylesheets work pretty well. They are quite fast,
seem to work in all cases I tested them and really stick to the domains they are
configuered for. However some pages will only load the new css after they are
completely loaded (the qutebrowser help stylesheet is such an example), while
others work immediatly (I have one for wikipedia, which styles it directly). I
don't know why. If anyone is able to help me figuring that out, please contact
me via mail or open a ticket.

### Stylsheet sources

There are some sources for user styles. Remark, that those stylesheets must
first be adapted to work with this setup. Especially the must not contain any
information about the urls they apply to directly. Instead this information
must be transfered to `stylemap.py`.

  - https://uso.kkx.one/
  - https://userstyles.world/explore
  - https://freestyler.ws/
  - https://github.com/topics/usercss

## Per Domain Darkreader for Qutebrowser {#darkreader}

All credits go to the developers of
[Darkreader](https://github.com/darkreader/darkreader).

### Installation and Usage

To install this userscript, just copy `userscripts/darkreader.py` to the
`userscripts` directory under the qutebrowser config directory.

Then you can enable darkreader for the current domain using:

```
:spawn --userscript darkreader.py enable domain
```

(Yes, domain must be typed literally.)

`brightness`, `contrast` and `sepia` for darkreader default to `90`, `90` and
`50`, but you can specify different values by appending them to the userscript
invocation. e.g.:

```
:spawn --userscript darkreader.py enable domain 100 100 0
```

Darkreader can be disabled by

```
:spawn --userscript darkreader.py disable domain
```

You can also use an url pattern instead of the string `domain`. However to
disable darkreader for the specified pattern, you must be sure to type it
exactly like you did again for the `disable` command.

To faciliate the invokation of darkreader it may be useful to define aliases (or
keybindings if you like) in your `config.py`, e.g.:

```
c.aliases['dr'] = 'spawn --userscript darkreader.py enable domain'
c.aliases['drd'] = 'spawn --userscript darkreader.py disable domain'
c.aliases['darkreader'] = 'spawn --userscript darkreader.py'
config.bind(',d', "set-cmd-text -s :darkreader enable '{url}*'")
config.bind(',r', "set-cmd-text -s :darkreader disable '{url}*'")
```

### How it works

The userscript creates a greasemonkey script for the domain/url pattern
provided when invoking it. It's named `darkreader-{md5 of the url pattern}` and
stored in the greasemonkey folder in the qutebrowser configuration directory.
It just contains an [invokation to DarkReader](https://github.com/darkreader/darkreader#using-dark-reader-for-a-website).
