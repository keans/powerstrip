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
