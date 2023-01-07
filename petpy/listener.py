from petpy.connect import Connection


class Listener:
    def __init__(self, name: str):
        self.name = name

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def get_connection(self) -> Connection:
        pass
