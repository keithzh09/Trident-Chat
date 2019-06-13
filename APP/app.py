# coding: utf-8
# @author  : lin
# @time    : 2019/6/5

import easygui as gui
from client import Client
from threading import Thread, Event
from APP.textbox import MainApp


class LoginDemo:
    def __init__(self):
        self.client = Client('', '')
        t = Thread(target=self.client.start_loop)
        t.start()
        msg = "输入账户密码呢亲"
        title = "Login"
        field_names = ["用户名", "密码"]
        field_values = []  # we start with blanks for the values

        field_values = gui.multpasswordbox(msg, title, field_names, field_values,
                                           callback=self.check_for_blank_fields)
        print("Reply was: {}".format(field_values))

    def check_for_blank_fields(self, box):
        # 保证输入框用户名和密码均不能为空
        cancelled = box.values is None
        errors = []
        if cancelled:
            pass
        else:
            for name, value in zip(box.fields, box.values):
                if value.strip() == "":
                    errors.append('"{}" 不可为空.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            self.client.user_name = box.values[0]
            self.client.user_pwd = box.values[1]
            # 另开一个线程监听服务端返回信息，不阻塞当前线程
            t = Thread(target=self.receive_login_msg, args=(box, ))
            t.start()
        box.msg = "\n".join(errors)

    def receive_login_msg(self, box):
        start_evt = Event()
        t = Thread(target=self.client.operate, args=('login', start_evt))
        t.start()
        # 阻塞，直到有结果
        start_evt.wait()
        errors = [self.client.login_msg]
        box.msg = "\n".join(errors)
        if self.client.is_login_succeeded:  # 登录成功
            box.stop()


class RegisterDemo:

    def __init__(self):
        self.client = Client('', '')
        t = Thread(target=self.client.start_loop)
        t.start()
        msg = "输入账户密码呢亲"
        title = "Register"
        field_names = ["用户名", "密码", "项目标识"]
        field_values = []  # we start with blanks for the values
        field_values = gui.multpasswordbox(msg, title, field_names, field_values,
                                           callback=self.check_for_blank_fields)
        print("Reply was: {}".format(field_values))

    def check_for_blank_fields(self, box):
        cancelled = box.values is None
        errors = []
        if cancelled:
            pass
        else:
            for name, value in zip(box.fields, box.values):
                if value.strip() == "":
                    errors.append('"{}" 不可为空.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            self.client.user_name = box.values[0]
            self.client.user_pwd = box.values[1]
            self.client.project_code = box.values[2]
            # 重开一个线程等待服务端返回信息，不阻塞当前线程
            t = Thread(target=self.receive_register_msg, args=(box, ))
            t.start()

        box.msg = "\n".join(errors)

    def receive_register_msg(self, box):
        start_evt = Event()
        t = Thread(target=self.client.operate, args=('register', start_evt))
        t.start()
        # 阻塞，直到有结果
        start_evt.wait()
        errors = [self.client.register_msg]
        box.msg = "\n".join(errors)
        if self.client.is_register_succeeded:  # 登录成功
            self.client.stop_loop()
            box.stop()


def login():
    login_demo = LoginDemo()
    if login_demo.client.is_login_succeeded:
        app = MainApp(login_demo.client)
        if app.is_user_logout:
            login_demo.client.stop_loop()
            login()
    login_demo.client.stop_loop()


def register():
    register_demo = RegisterDemo()
    register_demo.client.stop_loop()
    if register_demo.client.is_register_succeeded:
        login()


