# Welcome to powerstrip

The Python package `powerstrip` allows the simple creation and management
of plugins.

Main features:

* pythonic plugins based on extending Python classes
* creation of plugin package from plugin directory for easy distribution
  of plugin package
* installation of plugins into wanted target plugin directory
* discovery of plugins from defined target plugin
* filtering of plugins by criteria such as category or tag


## Why another plugin system?

Most of the plugin systems target the management of some plugin files within
the source code of the main program. However, for the management of large
plugin projects and the exchange of plugins between different users a
more flexible system is required. To this end, the `powerstrip` module
enables the creation of plugins using a simple metadata file and the plugin
code itself as extended `Plugin` class. Besides, a `PluginManager` class is
provided to simply manage the plugins.
