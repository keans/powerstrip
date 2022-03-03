# Usage

The use of the `powerstrip` module is two fold: on the one hand, plugins can
be developed apart from the main application by extending the abstract `Plugin`
class, while on the other hand, the main application can make use of the
`PluginManager` class to discover and make use of the plugins.


## Plugin

Create a separate directory for your plugin, such as `examples/pluginA`, and
create `metadata.yml` file in it with following content:

```
name: pluginA
author: foo <foo@example.com>
description: This is plugin A.
hash: a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
license: MIT
version: 0.0.1
category: blue
url: https://www.example.com
tags: one, two
```

Next to it, create a Python file, such as `plugina.py`, for the actual
plugin functionality. Each plugin must be derived from the `Plugin` class.

For example:

```
from powerstrip import Plugin


class PluginA(Plugin):
    """
    plugin A
    """
    def init(self):
        self.log.debug(f"initializing plugin {self.__class__.__name__}")

    def run(self):
        self.log.debug(f"running plugin {self.__class__.__name__}")

    def shutdown(self):
        self.log.debug(f"shutting down plugin {self.__class__.__name__}")
```

At minimum the three methods must be implemented for the abstract `Plugin`
class.


## The PluginManager class

The `PluginManager` is the main class that is used to handle plugins from
the application that should make use of the plugins:

```
from powerstrip import PluginManager

# create a plugin manager instance with given target plugin path
pm = PluginManager("~/.config/plugins")

# create two plugin packages from directory and store it in current directory
# two plugin package files: plugina-0.0.1.psp, pluginb-0.0.2.psp
pm.pack("examples/pluginA")
pm.pack("examples/pluginB")

# get metadata of both plugins
pm.info("plugina-0.0.1.psp")
pm.info("pluginb-0.0.2.psp")

# install both plugin packages to target path
pm.install("plugina-0.0.1.psp")
pm.install("pluginb-0.0.2.psp")

# discover all plugins
pm.discover()

# get all plugin classes
pm.get_plugin_classes()

# get plugin classes from specific category
pm.get_plugin_classes(category="blue")

# get plugin classes by tag
pm.get_plugin_classes(tag="one")

# uninstall plugin A
pm.uninstall("pluginA")
```
