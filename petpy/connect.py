class Connection:
    def __init__(self):
        self._listeners = []
        
        
    def send_message(self, message):
        pass
    
    def add_listener(self, listener):
        self._listeners.append(listener)
        
    def update_progress(self, progress):
        for listener in self._listeners:
            listener.on_progress(progress)
            
    def acquire_newline(self):
        pass