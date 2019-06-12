# coding: utf-8
# @author  : lin
# @time    : 2019/6/5

import paho.mqtt.client as mqtt
from config.topic_config import TOPIC_PARAMS, HOST, PORT
from lib.dao import LibDao

publish_topic = {'login_topic': 'login', 'register_topic': 'register',
                 'chat_topic': 'chat', 'all_notes_topic': 'all_notes'}


class ClientDao:

    @staticmethod
    def publish_login(client, user_name, user_pwd, return_topic):
        """
        发布登录信息
        :param client:
        :param user_name:
        :param user_pwd:
        :return:
        """
        # client = mqtt.Client()
        # client.connect(HOST, PORT, 60)
        data = {'user_name': user_name, 'user_pwd': user_pwd, 'return_topic': return_topic}
        # qos1
        client.publish(publish_topic['login_topic'], str(data).encode(), 1)
        # client.loop()
        print('publish msg to ', publish_topic['login_topic'], ' succeed')

    @staticmethod
    def publish_register(client, user_name, user_pwd, project_code):
        """
        发布注册信息
        :param client:
        :param user_name:
        :param user_pwd:
        :param project_code:
        :return:
        """
        # client = mqtt.Client()
        # client.connect(HOST, PORT, 60)
        data = {'user_name': user_name, 'user_pwd': user_pwd, 'project_code': project_code}
        client.publish(publish_topic['register_topic'], str(data).encode(), 1)
        print('publish msg to ', publish_topic['register_topic'], ' succeed')
        # client.loop()

    @staticmethod
    def publish_chat(user_token_key, msg, time, room_name, return_topic):
        """
        聊天信息
        :param user_token_key:
        :param msg:
        :param time:
        :param room_name:
        :return:
        """
        token = LibDao.get_client_token_by_user_name(user_token_key)
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        data = {'token': token, 'msg': msg, 'time': time, 'room_name': room_name,
                'return_topic': return_topic}
        client.publish(publish_topic['chat_topic'], str(data).encode(), 1)
        print('publish chat to ', publish_topic['chat_topic'], ' succeed')
        client.loop()

    @staticmethod
    def publish_all_notes_request(user_token_key, room_name, return_topic):
        """
        聊天信息
        :param user_token_key:
        :param room_name:
        :return:
        """
        token = LibDao.get_client_token_by_user_name(user_token_key)
        client = mqtt.Client()
        client.connect(HOST, PORT, 60)
        data = {'token': token, 'room_name': room_name, 'return_topic': return_topic}
        client.publish(publish_topic['all_notes_topic'], str(data).encode(), 1)
        print('publish update_request to ', publish_topic['all_notes_topic'], ' succeed')
        client.loop()

