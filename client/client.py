# coding: utf-8
# @author  : lin
# @time    : 2019/6/5


import paho.mqtt.client as mqtt
from .dao import ClientDao
from config.topic_config import HOST, PORT
from lib.dao import LibDao
from queue import Queue
import datetime
import threading


class Client:
    def __init__(self, user_name, user_pwd=None, project_code=None, room_name=None):
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.project_code = project_code  # 项目标识，只有注册时候才用到
        self.room_name = room_name  # 当前房间名
        self.login_msg = str()
        self.token_key = str()
        self.register_msg = str()
        self.all_rooms = list()
        self.all_notes = list()
        self.latest_notes_queue = Queue()
        self.is_login_succeeded = False  # 是否登录成功
        self.is_register_succeeded = False  # 是否注册成功
        self.is_get_all_notes_succeeded = False  # 是否获取所有信息成功
        self.is_publish_news_succeeded = False  # 是否发布成功
        self.is_user_logout = False  # 用户是否退出
        self.lock = threading.Lock()
        self.loop_num = 0
        self.start_evt = None  # 这是一个Event对象，用来查看是否验证成功
        # handle_func是指明接收数据后，靠数据包含字段来区分信息
        self.handle_func = {'login_msg': self.get_login_msg, 'register_msg': self.get_register_msg,
                            'all_notes': self.get_all_notes, 'latest_note': self.get_latest_note,
                            'error_msg': self.get_error_msg}
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)

    def start_loop(self):
        # 用线程锁来控制同时仅能一个loop_forever
        if self.loop_num == 0:
            self.lock.acquire()
            print('获得锁!')
            self.loop_num = 1
            self.client._thread_terminate = False
            self.client.loop_forever()

    def stop_loop(self):
        # 停止这个线程
        if self.loop_num == 1:
            self.lock.release()
            print('解锁!!')
            self.client._thread_terminate = True
            self.loop_num = 0

    def operate(self, order, start_evt=None, msg=None):
        """
        使用client._thread_terminate来控制这个线程的开启和关闭
        :param order: 指令名称
        :param start_evt: 线程控制的一个变量，当该变量执行set方法时，
                          表明子线程需要执行的任务已经完成（子线程不一定退出）
        :param msg: 只有命令为chat时才需要传入
        :return:
        """
        self.start_evt = start_evt
        if order == 'login':
            self.is_login_succeeded = False
            self.send_login_msg()
        elif order == 'register':
            self.is_register_succeeded = False
            self.send_register_msg()
        elif order == 'all_notes':
            self.is_get_all_notes_succeeded = False
            self.send_all_notes_msg()
        elif order == 'chat':
            self.send_one_msg(msg)

    def send_login_msg(self):
        # 设置标识，标示唯一一个用户，监听这个标识，直到收到回信
        self.token_key = self.user_name + datetime.datetime.now().strftime('%H:%M:%S')
        self.client.subscribe(self.token_key)
        ClientDao.publish_login(self.client, self.user_name, self.user_pwd, self.token_key)

    def send_register_msg(self):
        self.client.subscribe(self.user_name)
        ClientDao.publish_register(self.client, self.user_name, self.user_pwd, self.project_code)

    def send_all_notes_msg(self):
        self.client.subscribe(self.user_name)
        ClientDao.publish_all_notes_request(self.token_key, self.room_name, self.token_key)

    def send_one_msg(self, msg):
        # self.client.subscribe(self.user_name)
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ClientDao.publish_chat(self.token_key, msg, now_time, self.room_name, self.token_key)

    def receive_latest_note(self, last_room_name):
        # 监听这个房间的就好,此处应该是监听最新的,在选择了房间后就开始有
        try:
            self.client.unsubscribe(last_room_name)
        except Exception as error:
            print(error)
        self.client.subscribe(self.room_name)

    def get_login_msg(self, data):
        if 'token' in data.keys():
            # 登录成功
            print('验证通过')
            self.login_msg = '验证通过'
            self.is_login_succeeded = True
            self.all_rooms = data['all_rooms']
            # 保险起见
            self.user_name = data['user_name']
            LibDao.set_client_user_token(self.token_key, data['token'])
            self.client.unsubscribe(self.user_name)
            self.client.subscribe(self.token_key)
        else:
            print('验证失败 ' + data['login_msg'])
            self.login_msg = '验证失败 ' + data['login_msg']
            self.is_login_succeeded = False
            # 取消订阅
            self.client.unsubscribe(self.user_name)
        # 收到登录回信，变量调用set()函数，表示这个子线程已经执行到了该执行的位置
        self.start_evt.set()

    def get_register_msg(self, data):
        self.register_msg = data['register_msg']
        # 注册成功
        self.is_register_succeeded = True if self.register_msg == 'Succeed' else False
        self.client.unsubscribe(self.user_name)
        self.start_evt.set()

    def get_all_notes(self, data):
        self.all_notes = data['all_notes']
        # 将flag置为True，表示已经接收到最新消息
        self.is_get_all_notes_succeeded = True
        self.start_evt.set()

    def get_latest_note(self, data):
        one_note = data['latest_note']
        self.latest_notes_queue.put(one_note)

    def get_error_msg(self, data):
        # 收到这个说明当前用户已经失效
        print(data['error_msg'])
        self.is_user_logout = True

    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        data = eval(msg.payload.decode('utf-8'))
        for i in self.handle_func.keys():
            if i in data.keys():
                if i == 'error_msg':
                    print(data)
                func = self.handle_func[i]
                func(data)
