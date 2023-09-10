class Scheduler(object):
    def __init__(self):
        self.thread_list = []
        self.window = None
        self.terminate = False
    def start(self,window,fin_start):
        self.window =  window
        self.terminate = False

        for ip in window.finallye:
            print(ip)
            pass
        #创建线程
        pass

    def stop(self):
        pass

SCHEDULER = Scheduler()