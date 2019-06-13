# coding: utf-8
# @author  : lin
# @time    : 2019/6/13

import easygui as gui
from APP.app import login, register

if __name__ == '__main__':
    ret = gui.buttonbox(image='gif/hy1.gif',
                        title='Trident Chat', choices=(['登录', '注册']))
    if ret == '登录':
        login()
    elif ret == '注册':
        register()
