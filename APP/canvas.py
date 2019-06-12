# coding: utf-8
# @author  : lin
# @time    : 2019/6/6


# -*- coding: cp936 -*-
# 创建一个矩形，指定画布的颜色为白色
from tkinter import *  # 相当于命名空间

root = Tk()
# 创建一个Canvas，设置其背景色为白色
cv = Canvas(root, bg='white')
# 创建一个矩形，坐标为(10,10,110,110)
cv.create_rectangle(10, 10, 110, 110)
cv.pack()
root.mainloop()
# 为明显起见，将背景色设置为白色，用以区别 root
root.mainloop()