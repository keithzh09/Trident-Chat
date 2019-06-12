# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

import paho.mqtt.client as mqtt
from db_model.model_dao import UserModelDao, ChatRoomsModelDao, ChatNotesModelDao
from config.topic_config import TOPIC_PARAMS, HOST, PORT


class ServerDao:
    @staticmethod
    def check_publish_topic(topic, data):
        keys = data.keys()
        for key in TOPIC_PARAMS[topic]:
            if key not in keys:
                print('publish is not enough')
                return False
        return True

    @staticmethod
    def publish_login_msg(client, return_topic, user_name, msg, token=None):
        """
        回复给客户端的token
        :param user_name:用户名
        :param msg: 验证情况
        :param token:
        :return:
        """
        # client = mqtt.Client()
        # client.connect(HOST, PORT, 60)
        # user_name可以去掉
        data = {'user_name': user_name, 'login_msg': msg}
        if token:
            all_rooms = ChatRoomsModelDao.get_all_rooms()
            data.update({'token': token, 'all_rooms': all_rooms})
        client.publish(return_topic, str(data).encode(), 1)
        print('publish login_msg to ', return_topic, ' succeed')
        # client.loop()

    @staticmethod
    def publish_register_msg(client, user_name, msg):
        """
        回复给客户端的token
        :param user_name:用户名
        :param msg: 插入情况
        :return:
        """
        # 分情况
        data = {'user_name': user_name, 'register_msg': msg}
        print(data)
        client.publish(user_name, str(data).encode(), 1)
        print('publish register_msg to ', user_name, ' succeed')

    @staticmethod
    def publish_room_all_notes(return_topic, room_name):
        """
        给客户端该房间的所有历史记录
        :param return_topic: 标识一个客户端
        :param room_name:
        :return:
        """
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        room_id = ChatRoomsModelDao.get_id_by_name(room_name)
        model_list = ChatNotesModelDao.query_notes(room_id)
        data = []
        for model in model_list:
            user_name = UserModelDao.get_name_by_user_id(model.user_id)
            one_data = [user_name, model.message, model.time]
            data.append(one_data)
        publish_data = {'all_notes': data}
        client.publish(return_topic, str(publish_data).encode(), 1)
        print('publish all notes to ', return_topic, ' successfully')
        client.loop()

    @staticmethod
    def publish_latest_note(return_topic, note_id):
        """
        将最新发布的信息发送给所有订阅的客户端
        :param return_topic: 标识房间
        :param note_id:
        :return:
        """
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        model = ChatNotesModelDao.query_one_note(note_id)
        user_name = UserModelDao.get_name_by_user_id(model.user_id)
        data = [user_name, model.message, model.time]
        publish_data = {'latest_note': data}
        client.publish(return_topic, str(publish_data).encode(), 1)
        print('publish one note to ', return_topic, ' successfully')
        client.loop()

    @staticmethod
    def publish_invalid_msg(client, return_topic):
        """
        回复给客户端的token
        :param client:
        :param return_topic:
        :return:
        """
        # user_name可以去掉
        msg = 'Token invalid '
        data = {'error_msg': msg}
        client.publish(return_topic, str(data).encode(), 1)
        print('publish error_msg to ', return_topic, ' succeed')

