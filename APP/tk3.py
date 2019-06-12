# coding: utf-8
# @author  : lin
# @time    : 2019/6/6
from tkinter import *

root = Tk()
lb = Listbox(root)
scrollbarx = Scrollbar(root, orient=HORIZONTAL)
scrollbary = Scrollbar(root)
scrollbarx.pack(side=BOTTOM, fill=X)
scrollbary.pack(side=RIGHT, fill=Y)
# root.geometry("1280x720")
# side指定Scrollbar为居右；fill指定填充满整个剩余区域，到WM在时候再详细介绍这几个属性。
# 下面的这句是关键：指定Listbox的yscrollbar的回调函数为Scrollbar的set
lb['xscrollcommand'] = scrollbarx.set
lb['yscrollcommand'] = scrollbary.set
for i in range(100):
    lb.insert(END, str(i) * 20)

# side指定Listbox为居左,
lb.pack(side=LEFT, fill=BOTH)
# 下面的这句是关键：指定Scrollbar的command的回调函数是Listbar的yview
scrollbary['command'] = lb.yview
scrollbarx['command'] = lb.xview
root.mainloop()