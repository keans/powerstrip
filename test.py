#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from powerstrip.pluginmanager import PluginManager
from powerstrip.models.metadata import Metadata
from powerstrip.models.pluginpackage import PluginPackage


logging.basicConfig(level=logging.DEBUG)


def main():
    pm = PluginManager("~/python/tmp")

    #pp = PluginPackage("~/python/tmp")

    #pp.pack("~/python/tmp/b")

    #pp.install("pluginA-0.0.1.zip")

    info = pm.info("pluginB-0.0.2.psp")
    print(info)
    #pp.install("pluginB-0.0.2.psp")

    #pp.uninstall("pluginB")


def main2():
    m = Metadata(".")



def main3():
    pm=PluginManager('~/python/tmp')

    cls = pm.discover()
    print(cls)
    for c in cls:
        print(c)
        print(c())

    #pm.install("test.pkg")



if __name__ == "__main__":
    main()
