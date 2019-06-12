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
    print(pos)


# root.geometry("1280x720")#大小
scrollbar = Scrollbar(root, orient=HORIZONTAL, command=scrollCall)
scrollbar.pack(side=BOTTOM, fill=X)  # 必须填充

root.mainloop()