# coding: utf-8
# @author  : lin
# @time    : 2019/4/25

import paho.mqtt.client as mqtt
import time

HOST = "127.0.0.1"
PORT = 1883


def test():
    client = mqtt.Client()
    client.connect(HOST, PORT, 60)
    client.user_data_set('I am a gentlemen')
    print(client._userdata)
    for i in range(1):
        # data = ['xxxxxxxxxxxxxxxxxx', 'this 我 is a login message!']
        data = {'token': 'sadsaasdas', 'msg': '我是爸爸'}
        # print(str(data))
        client.publish("login", str(data), 1)
        time.sleep(1)
        client.loop()


# if __name__ == '__main__':
#     test()

handle_func = {'login': test, 'register': test, 'chat': test}

handle_func.update({'cc': 1})
print(handle_func)
