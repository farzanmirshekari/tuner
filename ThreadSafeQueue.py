from threading import Lock

class ThreadSafeQueue(object):
    
    def __init__(self):
        self.queue = []
        self.max_size = 10
        self.lock = Lock()

    def push(self, item):
        with self.lock:
            self.queue.append(item)
            if len(self.queue) > self.max_size:
                self.queue.pop(0)
            
    def pop(self):
        with self.lock:
            if len(self.queue) > 0:
                return self.queue.pop(0)
            else:
                return None
            
    def size(self):
        with self.lock:
            return len(self.queue)
        
    def clear(self):
        with self.lock:
            self.queue.clear()