# coding: utf-8
# @author  : lin
# @time    : 2019/4/25

import paho.mqtt.client as mqtt
from .dao import ServerDao
from config.topic_config import TOPIC_PARAMS, PROJECT_CODE, HOST, PORT
from lib.dao import LibDao
from db_model.model_dao import UserModelDao, ChatRoomsModelDao, ChatNotesModelDao
from threading import Thread, Lock


class Server:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)
        self.lock = Lock()
        self.loop_num = 0
        # handle_func的keys()为要订阅的主题列表
        self.handle_func = {'login': self.login, 'register': self.register,
                            'chat': self.chat, 'all_notes': self.all_notes}

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

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully ")
        for topic in self.handle_func.keys():
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        # 规定传入数据均为dict的形式
        data = eval(msg.payload.decode('utf-8'))
        if ServerDao.check_publish_topic(msg.topic, data):
            if msg.topic in self.handle_func.keys():
                func = self.handle_func[msg.topic]
                func(data)

    def login(self, data):
        msg = UserModelDao.check_user_and_user_pwd(data['user_name'], data['user_pwd'])
        print(msg)
        token = LibDao.set_user_name_token(data['user_name']) if msg == 'Correct' else None
        # topic使用用户名，即对某个用户定点发送
        # t = Thread(target=ServerDao.publish_login_msg, args=(data['user_name'], msg, token, ))
        # t.start()
        return_topic = data['return_topic']
        ServerDao.publish_login_msg(self.client, return_topic, data['user_name'], msg, token)

    def register(self, data):
        if data['project_code'] == PROJECT_CODE:
            msg = UserModelDao.add_user(data['user_name'], data['user_pwd'])
        else:
            msg = 'project_code is wrong'
        print(msg)
        ServerDao.publish_register_msg(self.client, data['user_name'], msg)

    def chat(self, data):
        token = data['token']
        return_topic = data['return_topic']
        if not LibDao.if_token_valid(token):
            token_user = LibDao.get_user_name_from_token(token)
            if token_user:  # 能获取到名字就发送
                ServerDao.publish_invalid_msg(self.client, return_topic)
            return
        room_name = data['room_name']
        user_name = LibDao.get_user_name_from_token(token)
        room_id = ChatRoomsModelDao.get_id_by_name(room_name)
        user_id = UserModelDao.get_id_by_user_name(user_name)
        message = data['msg']
        time = data['time']
        note_id = ChatNotesModelDao.add_note(room_id, user_id, message, time)
        if note_id:
            ServerDao.publish_latest_note(room_name, note_id)

    def all_notes(self, data):
        token = data['token']
        return_topic = data['return_topic']
        if not LibDao.if_token_valid(token):
            token_user = LibDao.get_user_name_from_token(token)
            if token_user:  # 能获取到名字就发送
                ServerDao.publish_invalid_msg(self.client, return_topic)
            return
        room_name = data['room_name']
        user_name = LibDao.get_user_name_from_token(token)
        ServerDao.publish_room_all_notes(return_topic, room_name)


