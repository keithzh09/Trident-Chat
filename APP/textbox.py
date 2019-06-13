# coding: utf-8
# @author  : lin
# @time    : 2019/6/6


from tkinter import *
from client import Client
from threading import Thread, Event


class MainFrame(Frame):
    def __init__(self, client, master):
        Frame.__init__(self, master)
        self.client = client
        self.room_name = StringVar()    # 可变，用于标签显示，与self.client.room_name同步更新
        self.field_1_label = None
        self.field_1_label2 = None
        self.field_1_listbox = None
        self.field_2_t_scrollbar = None
        self.field_2_text = None
        self.field_3_button = None
        self.grid(row=0, column=0, sticky="nsew")
        self.create_frame()

    def create_frame(self):
        label_frame_top = LabelFrame(self)
        field_1 = LabelFrame(label_frame_top)
        field_1.pack(fill="x")
        self.field_1_label = Label(field_1, textvariable=self.room_name,
                                   width=10, height=20, font='Helvetica -15 bold')
        self.field_1_label.pack(fill="y", expand=0, side=LEFT)
        self.field_1_listbox = Listbox(field_1,  width=20, font='Helvetica -15 bold')
        self.field_1_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        scrollbar_y = Scrollbar(field_1)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        self.field_1_listbox['yscrollcommand'] = scrollbar_y.set

        scrollbar_y['command'] = self.field_1_listbox.yview
        self.field_1_label2 = Label(field_1, textvariable=self.room_name,
                                    width=10, height=20, font='Helvetica -15 bold')
        self.field_1_label2.pack(fill="y", expand=0, side=LEFT)
        label_frame_top.pack(fill="x")

        label_frame_center = LabelFrame(self)
        field_2 = LabelFrame(label_frame_center)
        field_2.pack(fill="x")

        self.field_2_t_scrollbar = Scrollbar(field_2, orient=VERTICAL)  # 文本框-竖向滚动条

        self.field_2_text = Text(field_2, height=5, yscrollcommand=self.field_2_t_scrollbar.set,
                                 wrap='word')  # 设置滚动条-换行
        # 滚动事件
        self.field_2_t_scrollbar.config(command=self.field_2_text.yview)

        # 布局
        self.field_2_t_scrollbar.pack(fill="y", side=RIGHT, anchor=W)
        # 设置文本框自适应大小
        self.field_2_text.pack(fill="x", expand=1, side=BOTTOM)

        # 绑定事件
        self.field_2_text.bind("<Control-Key-a>", self.select_text)
        self.field_2_text.bind("<Control-Key-A>", self.select_text)

        label_frame_center.pack(fill="x")

        label_frame_bottom = LabelFrame(self)
        field_3 = LabelFrame(label_frame_bottom)
        field_3.pack(fill="x")
        self.field_3_button = Button(field_3, text="更新", width=10, height=1, command=self.send_and_clear_text)
        self.field_3_button.pack(fill="none", expand=0, side=LEFT, anchor=SE)
        self.field_3_button = Button(field_3, text="发送", width=10, height=1, command=self.send_one_msg)
        self.field_3_button.pack(fill="none", expand=0, side=RIGHT, anchor=SE)
        label_frame_bottom.pack()

        t = Thread(target=self.monitor_latest_note)
        t.start()

    def monitor_latest_note(self):
        # 监控所有最新消息
        # 监控当前用户是否已经失效
        while True:
            if not self.client.latest_notes_queue.empty():
                note = self.client.latest_notes_queue.get()
                msg1 = ('%-20s%s' % (note[0], note[2]))
                self.field_1_listbox.insert(END, msg1, note[1])
                self.field_1_listbox.insert(END, ' ')
                # 滚动到最下面
                self.field_1_listbox.yview_moveto(1)
            if self.client.is_user_logout:
                break

    def monitor_all_notes(self):
        while True:
            if self.client.is_get_all_notes_succeeded:
                self.field_1_listbox.delete(0, END)
                for note in self.client.all_notes:
                    # note格式: eg.['lin', 'Hello World!', '2019-06-05 00:34:53']
                    msg1 = ('%-20s%s' % (note[0], note[2]))
                    self.field_1_listbox.insert(END, msg1, note[1])
                    self.field_1_listbox.insert(END, ' ')
                    self.field_1_listbox.yview_moveto(1)

                break

    def update_notes(self):
        # start_evt = Event()
        # 暂且使用线程,防止用户一下子多次请求更新
        t1 = Thread(target=self.client.operate, args=('all_notes',))
        t1.start()
        # start_evt.wait()
        # self.client.stop_loop()
        t1 = Thread(target=self.monitor_all_notes)
        t1.start()

    # 文本全选
    def select_text(self, event):
        self.field_2_text.tag_add(SEL, "1.0", END)
        # self.lfc_field_1_t.mark_set(INSERT, "1.0")
        # self.lfc_field_1_t.see(INSERT)
        return 'break'  # 为什么要return 'break'

    # 文本清空
    def send_and_clear_text(self):
        self.field_2_text.delete(0.0, END)
        self.update_notes()

    def send_one_msg(self):
        msg = self.field_2_text.get(0.0, END)[:-1]
        if len(msg) > 0:
            # 输入不为空时才可以
            # t1 = Thread(target=self.client.start_loop, args=('chat', None, msg, ))
            # t1.start()
            self.client.operate(order='chat', msg=msg)
            self.field_2_text.delete(0.0, END)


class MainApp:

    def __init__(self, client):
        self.client = client
        self.is_user_logout = False
        self.received_client = Client(self.client.user_name)
        self.root = Tk()
        self.root.title('Trident Chat')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        # 设置了主窗口的初始大小和放的位置
        self.root.geometry('800x610+600+200')
        self.menu = Menu(self.root)  # 参数是父级控件
        self.main_frame = MainFrame(self.client, self.root)
        self.create_app()

    def create_app(self):

        # 二级菜单
        cascade0 = Menu(self.menu, tearoff=False)  # tearoff=False 表示这个菜单不可以被拖出来

        cascade0.add_separator()  # 分割线
        # cascade0.add_checkbutton(label="在不调试的情况下启动")  # 单选框
        for i in range(len(self.client.all_rooms)):
            if i == 0:
                cascade0.add_radiobutton(label=self.client.all_rooms[i],
                                         command=lambda: self.choose_room(self.client.all_rooms[0]))  # 多选框
            elif i == 1:
                cascade0.add_radiobutton(label=self.client.all_rooms[i],
                                         command=lambda: self.choose_room(self.client.all_rooms[1]))  # 多选框
            elif i == 2:
                cascade0.add_radiobutton(label=self.client.all_rooms[i],
                                         command=lambda: self.choose_room(self.client.all_rooms[2]))  # 多选框

        cascade0.add_separator()  # 分割线
        self.menu.add_cascade(label='聊天室', menu=cascade0)  # 在menu0中添加一个label为项目的级联菜单

        cascade1 = Menu(self.menu, tearoff=False)

        cascade1.add_command(label='注销', command=self.logout)
        cascade1.add_command(label='退出', command=self.exit_it)

        self.menu.add_cascade(label='用户', menu=cascade1)

        self.root['menu'] = self.menu  # 窗口root的menu是menu0

        self.main_frame.mainloop()

    def choose_room(self, room_name):
        # 获取上一个房间名，是为了取消订阅
        last_room_name = self.client.room_name
        self.client.room_name = room_name
        self.client.receive_latest_note(last_room_name)
        self.main_frame.room_name.set(room_name)
        self.main_frame.send_and_clear_text()

    def exit_it(self):
        self.client.is_user_logout = True
        self.root.destroy()

    def logout(self):
        self.client.is_user_logout = True
        self.root.destroy()
        self.is_user_logout = True

