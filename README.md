CRDPPF
============

# Getting started

Create an empty folder on your disk and prepare it for the git project from your console

    $ cd [path to your directory]
    $ git init
    
Checkout the source code:

    $ git clone https://github.com/sitn/crdppf.git

or when you're using ssh key (see https://help.github.com/articles/generating-ssh-keys):

    $ git clone git@github.com:sitn/crdppf.git

Get the submodules

    $ cd crdppf

    $ git submodule update --init

Bootstrap and buildout

    $ python bootstrap.py --version 1.5.2 --distribute --download-base \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/ --setup-source \
        http://pypi.camptocamp.net/distribute-0.6.22_fix-issue-227/distribute_setup.py

Create your own buildout file by:
* Copy-paste `buildout.cfg`
* Rename the new file `buildout_<user>.cfg`
* Open this file in a text editor
* Erase all sections except the `[vars]` section
* In the `[vars]` section, delete all lines which do not contain `overwrite_me`
* At the top of the file, add the extend instruction:

```
[buildout]
extends = buildout.cfg
```

Adapt the `overwrite_me` values to your environment:
* `mapproxyurl` has to be a single or a list of WMTS URLs (like 'http://wmts1', 'http://wmts2', ...)
* If you do not set `proxy_enabled` to True, then you do not need to set the four remaining (`proxy_user`, `proxy_pass`, `proxy_server`, `proxy_port`).

Run buildout

    $ ./buildout/bin/buildout -c buildout_<user>.cfg
