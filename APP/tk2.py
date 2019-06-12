# coding: utf-8
# @author  : lin
# @time    : 2019/6/6
from tkinter import *

root = Tk()


def scrollCall(moveto, pos):
    # 如何得到两个参数：使用如下打印中的信息，可以看到解释器传给scrollCall函数的两个参数，一个为
    # moveto,参考手册可以得知，它是当拖动slider时调用的函数；另一个参数为slider的当前位置，我们
    # 可以通过set函数来设置slider的位置，因此使用这个pos就可以完成控制slider的位置。
    scrollbar.set(pos, 0)
    list.insert(END, pos)


# root.geometry("1280x720")#大小
scrollbar = Scrollbar(root, command=scrollCall)
scrollbar.grid(column=0, row=0, sticky=NS)
# sticky 意思是组件紧靠所在单元格的某一边角。
# 取值有：N,S,E,W,NS,EW,NE,SW
# (默认为CENTER)
list = Listbox(root)
list.grid(row=0, column=1)
root.mainloop()
