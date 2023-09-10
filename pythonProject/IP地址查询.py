import os
import sys
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QDesktopWidget,QHBoxLayout,QVBoxLayout,QPushButton,QLineEdit,\
QTableWidget,QTableWidgetItem,QLabel,QMessageBox,QMenu

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

STATUW_MAPPING={
    0:"初始化中",
    1:"待执行",
    2:"正在执行",
    3:"完成并提醒",
    10:"异常并停止",
    11:"初始化失败",
}


RUNING = 1
STOPING = 2
STOP = 3

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.switch = STOP

        self.txt_asin = None
        self.setWindowTitle("标题")
        self.resize(1223,450)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        layout = QVBoxLayout()
        layout.addLayout(self.init_header())
        layout.addLayout(self.init_form())
        layout.addLayout(self.init_table())
        layout.addLayout(self.init_footer())
        # 弹簧
        # layout.addStretch()

        self.setLayout(layout)

        # self.show()

    def init_header(self):
        #1
        header_layout = QHBoxLayout()

        btn_start = QPushButton("开始")
        btn_start.clicked.connect(self.event_start_click)
        # btn_start.setFixedHeight(100)
        header_layout.addWidget(btn_start)

        btn_stop = QPushButton("停止")
        btn_stop.clicked.connect(self.event_stop_click)
        header_layout.addWidget(btn_stop)
        # 弹簧
        header_layout.addStretch()

        return header_layout

    def init_form(self):

        # 2 创建标题布局
        form_layout = QHBoxLayout()
        # 输入框
        txt_asin = QLineEdit()
        txt_asin.text()
        txt_asin.setText('B08166SLDF=90')
        txt_asin.setPlaceholderText("默认提示")
        self.txt_asin=txt_asin
        form_layout.addWidget(txt_asin)
        # 添加按钮
        btn_add = QPushButton("添加")
        btn_add.clicked.connect(self.event_add_click)
        form_layout.addWidget(btn_add)

        return form_layout

    def init_table(self):

        #3 中间的表格
        table_layout = QHBoxLayout()

        # 创建表格
        # QTabWidget(行，列)
        self.table_widget = table_widget = QTableWidget(0,8)

        table_header = [
            {"field": "asin", "text": "ASIN", "width": 120},
            {"field": "title", "text": "标题", "width": 150},
            {"field": "url", "text": "URL", "width": 400},
            {"field": "price", "text": "底价", "width": 100},
            {"field": "success", "text": "成功次数", "width": 100},
            {"field": "error", "text": "503次数", "width": 100},
            {"field": "status", "text": "状态", "width": 100},
            {"field": "frequency", "text": "频率", "width": 100},
        ]

        for idx ,info in enumerate(table_header):
            item = QTableWidgetItem()
            item.setText(info['text'])
            table_widget.setHorizontalHeaderItem(idx,item)
            table_widget.setColumnWidth(idx,info["width"])
        #
        # itme = QTableWidgetItem()
        # itme.setText("标题")
        # table_widget.setHorizontalHeaderItem(0,itme)
        # table_widget.setColumnWidth(0,400)
        #
        #
        # itme = QTableWidgetItem()
        # itme.setText("地址")
        # table_widget.setHorizontalHeaderItem(1,itme)

        import json
        file_path = os.path.join(BASE_DIR,"db","db.json")
        with open(file_path,mode="r",encoding="utf-8") as f:
            data = f.read()
        data_list = json.loads(data)

        curren_row_count = table_widget.rowCount()#当前表格有多少行
        for row_list in data_list:
            table_widget.insertRow(curren_row_count)

            for i , ele in enumerate(row_list):

                ele = STATUW_MAPPING[ele] if i==6 else ele

                cell = QTableWidgetItem(str(ele))
                #不可修改属性
                if i in [4,5,6]:
                    cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsSelectable)

                table_widget.setItem(curren_row_count,i,cell)

            curren_row_count += 1

        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(self.table_right_menu)




        table_layout.addWidget(table_widget)

        return table_layout

    def table_right_menu(self,pos):
        #只选中一行时，才支持右键
        selected_item_list = self.table_widget.selectedItems()
        if len(selected_item_list) == 0:
            return


        # selected_item_list[0]



        menu = QMenu()
        item_copy = menu.addAction("复制")
        item_log = menu.addAction("查看日志")
        itme_log_clear = menu.addAction("清除日志")
        action = menu.exec_(self.table_widget.mapToGlobal(pos))

        if action == item_copy:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_item_list[0].text())

        if action == item_log:
            from utils.dialog import LogDialog
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index,0).text().strip()
            dialog = LogDialog(asin)
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec_()
            pass
        if action == itme_log_clear:
            row_index = selected_item_list[0].row()
            asin = self.table_widget.item(row_index,0).text().strip()

            file_path = os.path.join("log","{}.log".format(asin))
            if os.path.exists(file_path):
                os.remove(file_path)
            pass



    def init_footer(self):
        # 4底部菜单
        footer_layout = QHBoxLayout()

        self.lable_status = lable_status = QLabel("未检测", self)
        footer_layout.addWidget(lable_status)

        footer_layout.addStretch()

        btn_reset = QPushButton("重新初始化")
        btn_reset.clicked.connect(self.event_reset_click)
        footer_layout.addWidget(btn_reset)

        btn_recheck = QPushButton("重新检测")
        footer_layout.addWidget(btn_recheck)

        btn_reset_count = QPushButton("次数清零")
        btn_reset_count.clicked.connect(self.event_btn_reset_count_click)
        footer_layout.addWidget(btn_reset_count)

        btn_delete = QPushButton("删除检测项")
        btn_delete.clicked.connect(self.event_delete_click)
        footer_layout.addWidget(btn_delete)

        btn_alert = QPushButton("SMTP报警配置")
        btn_alert.clicked.connect(self.event_alert_click)
        footer_layout.addWidget(btn_alert)

        btn_proxy = QPushButton("代理IP")
        btn_proxy.clicked.connect(self.event_proxy_click)
        footer_layout.addWidget(btn_proxy)

        return footer_layout

    #点击按钮添加功能
    def event_add_click(self):
        text = self.txt_asin.text()
        text=text.strip()
        if not text:
            QMessageBox.warning(self,"错误","输入错误")
            return

        #B08166SLDF=90
        asin,price = text.split("=")
        price = float(price)


        new_row_list = [asin,"","",price,0,0,0,5]
        curren_row_count = self.table_widget.rowCount()  # 当前表格有多少行

        self.table_widget.insertRow(curren_row_count)

        for i, ele in enumerate(new_row_list):

            ele = STATUW_MAPPING[ele] if i == 6 else ele

            cell = QTableWidgetItem(str(ele))
            # 不可修改属性
            if i in [ 4, 5, 6]:
                cell.setFlags(Qt.ItemIsSelectable | Qt.ItemIsSelectable)

            self.table_widget.setItem(curren_row_count, i, cell)

        from utils.threads import NewTaskThread

        thread = NewTaskThread(curren_row_count,asin,self)
        thread.success.connect(self.init_tack_success_callback)
        thread.error.connect(self.init_tack_error_callback)
        thread.start()


    def init_tack_success_callback(self,row_index,asin,title,url):


        #更新标题列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index,1,cell_title)

        #更新url
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index,2,cell_url)

        #更新状态
        cell_tatus =QTableWidgetItem(STATUW_MAPPING[2])
        cell_tatus.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index,6,cell_tatus)

        #清空输入框
        self.txt_asin.clear()
        print(3)
        pass


    def init_tack_error_callback(self,row_index,asin,title,url):

        # 更新标题列
        cell_title = QTableWidgetItem(title)
        self.table_widget.setItem(row_index, 1, cell_title)

        # 更新url
        cell_url = QTableWidgetItem(url)
        self.table_widget.setItem(row_index, 2, cell_url)

        # 更新状态
        cell_tatus = QTableWidgetItem(STATUW_MAPPING[11])
        cell_tatus.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_tatus)

        self.txt_asin.clear()
        print(4)
        pass

        #重新初始化

    #重新初始化
    def event_reset_click(self):
        #1.获取选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self,"错误","请选择要重新初始化的行")
            return
        #2.获取每一行重新初始化
        for row_object in row_list:
            index = row_object.row()
            asin = self.table_widget.item(index,0).text().strip()
            # 更新状态
            cell_tatus = QTableWidgetItem(STATUW_MAPPING[0])
            cell_tatus.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 6, cell_tatus)

            #创建线程完成初始化的动作
            from utils.threads import NewTaskThread
            thread = NewTaskThread(index, asin, self)
            thread.success.connect(self.init_tack_success_callback)
            thread.error.connect(self.init_tack_error_callback)
            thread.start()

        pass

        #数量清零
    #数量清零
    def event_btn_reset_count_click(self):
        # 1.获取选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要操作的行")
            return
        # 2.获取每一行重新初始化
        for row_object in row_list:
            index = row_object.row()
            # asin = self.table_widget.item(index, 0).text().strip()
            # 更新状态
            cell_tatus = QTableWidgetItem(str(0))
            cell_tatus.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 4, cell_tatus)
            # 更新状态
            cell_tatus = QTableWidgetItem(str(0))
            cell_tatus.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table_widget.setItem(index, 5, cell_tatus)
    #删除
    def event_delete_click(self):
        # 1.获取选中的行
        row_list = self.table_widget.selectionModel().selectedRows()
        if not row_list:
            QMessageBox.warning(self, "错误", "请选择要操作的行")
            return
        # 2.获取每一行重新初始化
        row_list.reverse()
        for row_object in row_list:
            index = row_object.row()
            self.table_widget.removeRow(index )
    #邮件配置
    def event_alert_click(self):
        #创建弹窗
        from utils.dialog import AlertDialog
        dialog = AlertDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()
        pass
    #代理IP
    def event_proxy_click(self):
        from utils.dialog import ProxyDialog
        dialog = ProxyDialog()
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    # 点击开始
    def event_start_click(self):
        if self.switch != STOP:
            QMessageBox.warning(self,"错误","请勿重复操作")
            return
        self.switch = RUNING

        #每行创建一个线程
        from utils.scheduler import SCHEDULER

        SCHEDULER.start(
            BASE_DIR,
            self,
            self.tack_start_callback,
            self.tack_stop_callback,
            self.tack_counter_callback,
            self.tack_error_counter_callback

        )

        #更新状态
        self.lable_status.setText("执行中")
        self.lable_status.repaint()
        pass

    def tack_stop_callback(self,row_index):


        cell_status = QTableWidgetItem(STATUW_MAPPING[1])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)

    def tack_start_callback(self, row_index):
        # 对表格中的数据状态更新
        cell_status = QTableWidgetItem(STATUW_MAPPING[2])
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 6, cell_status)


    def tack_counter_callback(self,row_index):
        #原有个数+1
        old_count = self.table_widget.item(row_index,4).text().strip()
        new_count = int(old_count) + 1

        #重新表格赋值
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 4, cell_status)

    def tack_error_counter_callback(self,row_index):
        #原有个数+1
        old_count = self.table_widget.item(row_index,5).text().strip()
        new_count = int(old_count) + 1

        #重新表格赋值
        cell_status = QTableWidgetItem(str(new_count))
        cell_status.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.table_widget.setItem(row_index, 5, cell_status)


    def event_stop_click(self):
        if self.switch != RUNING:
            QMessageBox.warning(self,"错误","请勿重复操作")

            return
        self.switch = STOPING
        #执行中的线程逐一停止
        from utils.scheduler import SCHEDULER

        SCHEDULER.stop()
        #更新状态


        #更新状态
        self.lable_status.setText("正在中止")
        self.lable_status.repaint()

    def update_status_message(self,message):
        if message =="中止完成":
            self.switch = STOP
        self.lable_status.setText(message)
        self.lable_status.repaint()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())