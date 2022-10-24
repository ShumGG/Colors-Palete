import threading;

class RenderThread(threading.Thread):

    def __init__(self, func):
        threading.Thread.__init__(self);
        self.func = func;
        self._stopper = threading.Event();
    
    def setFunc(self, func):
        self.func = func;
        
    def stop(self): 
        self._stopper.set();

    def run(self):
        while True:
            if (self._stopper.is_set()):
                break;
            else:
                self.func();
        