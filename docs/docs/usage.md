# Usage

The `PluginManager` is the main class that is used to handle plugins.

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
