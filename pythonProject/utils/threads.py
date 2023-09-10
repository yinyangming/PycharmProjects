import requests
import lxml
import  time
from bs4 import BeautifulSoup
from  PyQt5.QtCore import  QThread,pyqtSignal

HOST = "https://www.amazon.com/"
HOST_ASIN_TPL = "{}{}".format(HOST,"gp/product/")
HOST_TASK_LIST_TPL  = "{}{}".format(HOST,"gp/offer-listing")

class NewTaskThread(QThread):
    #触发信号
    success = pyqtSignal(int,str,str,str)
    error = pyqtSignal(int,str,str,str)



    def __init__(self,row_index,asin,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.row_index = row_index
        self.asin = asin
    def run(self):
        '''线程具体要做的事'''
        # self.error.emit(1,"xx","xx","xx")
        # self.success.emit(2,"xx","xx","xx")

        try:
            url = "{}{}".format(HOST_ASIN_TPL,self.asin)
            res = requests.get(
                url=url,
                headers={
                    "User - Agent":"Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML,likeGecko) Chrome / 116.0.0.0Safari/537.36",
                    "pragma":"no_cache",
                    "Accept - Language":"zh - CN, zh;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                    "upgrade-insecure-requests":"1",
                    "cache-control":"no-cache",
                    "accept-encoding":"gzip,deflate,br",
                    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
                }
            )
            if res.status_code  !=200:
                raise  Exception("初始化失败")
            soup = BeautifulSoup(res.text,"lxml")
            title = soup.find(id ="productTitle").text.strip()
            url = "{}{}/ref=dp_olp_all_mbc?ie=UTF8&condition=new".format(HOST_TASK_LIST_TPL,self.asin)
            self.success.emit(self.row_index,self.asin,title,url)

        except Exception as e:
            title = "监控项{}添加失败".format(self.asin)
            self.error.emit(self.row_index,self.asin,title,str(e))
            print(2)

class TackThread(QThread):
    start_signal = pyqtSignal(int)
    counter_signal = pyqtSignal(int)
    stop_signal = pyqtSignal(int)

    error_counter_signal = pyqtSignal(int)

    def __init__(self,scheduler,log_file_path,row_index,asin,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.scheduler = scheduler
        self.row_index = row_index
        self.asin = asin
        self.log_file_path = log_file_path

    def run(self) :
        #
        self.start_signal.emit(self.row_index)
        import time
        import random
        while True:
            if self.scheduler.terminate:
                self.stop_signal.emit(self.row_index)
                self.scheduler.destroy_thread(self)
                return
            try:
                time.sleep(random.randint(1,3))
                self.counter_signal.emit(self.row_index)

                with open(self.log_file_path,mode="a",encoding="utf-8") as f:
                    f.write("日志\n")
                    #监控的动作
                    #1.根据型号访问通过bs4获取数据
                    #2.获取到数据，价格是否小于预期
                    #3.发送邮件报警
                    #需要死循环执行的部分
                time.sleep(5)
            except Exception as e:
                self.error_counter_signal.emit(self.row_index)


class StopThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self,scheduler,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.scheduler = scheduler
    def run(self):
        total_count = len(self.scheduler.thread_list)
        while True:
            running_count = len(self.scheduler.thread_list)

            self.update_signal.emit("正在中止，剩余{}".format(running_count))

            if running_count == 0 :

                break
            time.sleep(2)
        self.update_signal.emit("中止完成")



