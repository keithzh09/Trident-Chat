# coding: utf-8
# @author  : lin
# @time    : 2019/4/25

import paho.mqtt.client as mqtt
import threading
from multiprocessing import Process
import time


HOST = "127.0.0.1"
PORT = 1883

class client:

    def __init__(self,  client):
        self.client = client

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully ")

    def login(self, msg):
        # print(msg.topic + ": " + str(msg.payload))
        print(msg.topic, msg.payload)
        data = eval(msg.payload.decode('utf-8'))
        # print(data)

    def on_message(self, client, userdata, msg):
        self.login(msg)
        # self.client._thread_terminate = True
        # # self.client.unsubscribe('lii')
        # # self.client.subscribe('lii')
        # self.client._thread_terminate = False
        data = {'token': 'sadsaasdas'}
        for i in range(5):
            self.client.publish('lii', str(data).encode(), 1)
            print('publish sorry')
            self.client.publish('mqtt', str(data).encode(), 1)

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(HOST, PORT, 60)
        self.client.subscribe('mqtt')
        # self.client.subscribe('login')
        self.client.subscribe('lii')
        self.client.loop_forever()

    def start2(self):
        # client2 = mqtt.Client()
        # client2.connect(HOST, PORT, 60)
        # self.client.loop()
        data = {'token': 'sadsaasdas'}
        for i in range(1):
            self.client.publish('lii', str(data).encode(), 1)
            print('publish sorry')
            self.client.publish('mqtt', str(data).encode(), 1)
            print('publish sorry')

            # time.sleep(1)
            # self.client.loop()


if __name__ == '__main__':
    client1 = mqtt.Client()
    myClient = client(client1)
    p = threading.Thread(target=myClient.start)
    p.start()
    myClient.client.subscribe('lii')
    print('Child process will start.')
    time.sleep(1)
    myClient.start2()
    # t2 = Process(target=start2)
    # t2.start()






