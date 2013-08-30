CRDPPF
============

# Getting started

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

Create your own buildout file
    $ buildout_<user>.cfg

Overwrite all the vars which equal to $ overwrite

Run buildout

    $ ./buildout/bin/buildout -c buildout_<user>.cfg
