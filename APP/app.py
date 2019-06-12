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
        # make sure that none of the fields was left blank
        cancelled = box.values is None
        errors = []
        if cancelled:
            pass
        else:  # check for errors
            for name, value in zip(box.fields, box.values):
                if value.strip() == "":
                    errors.append('"{}" 不可为空.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            self.client.user_name = box.values[0]
            self.client.user_pwd = box.values[1]
            start_evt = Event()
            t = Thread(target=self.client.operate, args=('login', start_evt))
            t.start()
            # self.client.operate(order='login', start_evt=start_evt)
            # 阻塞，直到有结果
            start_evt.wait()
            errors = [self.client.login_msg]
            if self.client.is_login_succeeded:  # 登录成功
                box.stop()  # no problems found

        box.msg = "\n".join(errors)


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
        # make sure that none of the fields was left blank
        cancelled = box.values is None
        errors = []
        if cancelled:
            pass
        else:  # check for errors
            for name, value in zip(box.fields, box.values):
                if value.strip() == "":
                    errors.append('"{}" 不可为空.'.format(name))

        all_ok = not errors

        if cancelled or all_ok:
            self.client.user_name = box.values[0]
            self.client.user_pwd = box.values[1]
            self.client.project_code = box.values[2]
            start_evt = Event()
            t = Thread(target=self.client.operate, args=('register', start_evt))
            t.start()
            # 阻塞，直到有结果
            start_evt.wait()
            errors = [self.client.register_msg]
            # self.client.stop_loop()
            if self.client.is_register_succeeded:  # 登录成功
                self.client.stop_loop()
                box.stop()  # no problems found

        box.msg = "\n".join(errors)


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


if __name__ == '__main__':
    ret = gui.buttonbox(image='timg.gif',
                        title='HELLO WORLD', choices=(['登录', '注册']))
    if ret == '登录':
        login()
    elif ret == '注册':
        register()
