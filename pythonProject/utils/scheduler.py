class Scheduler(object):
    def __init__(self):
        self.thread_list = []
        self.window = None
        self.terminate = False
    def start(self,base_dir,window,fn_start,fn_stop,fn_counter,fn_error_counter):
        self.window = window
        self.terminate = False

        for row_index in range(window.table_widget.rowCount()):
            asin = window.table_widget.item(row_index,0).text().strip()
            status_text = window.table_widget.item(row_index,6).text().strip()

            import os
            log_folder = os.path.join(base_dir,"log")
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)
            log_file_path = os.path.join(base_dir,"log","{}.log".format(asin))

            if status_text != "待执行":
                continue

            from  utils.threads import TackThread
            t = TackThread(self,log_file_path,row_index,asin,window)
            t.start_signal.connect(fn_start)
            t.stop_signal.connect(fn_stop)
            t.counter_signal.connect(fn_counter)
            t.error_counter_signal.connect(fn_error_counter)

            t.start()

            self.thread_list.append(t)
            # print(asin)
            pass
        pass

    def stop(self):
        self.terminate = True
        #创建线程检测thread_list的数量，更新数量信息



        from utils.threads import StopThread
        t = StopThread(self,self.window)
        t.update_signal.connect(self.window.update_status_message)
        t.start()
        pass


    def destroy_thread(self,thread):
        self.thread_list.remove(thread)




#单例模式
SCHEDULER = Scheduler()