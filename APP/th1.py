# coding: utf-8
# @author  : lin
# @time    : 2019/6/6

from tkinter import *  # 相当于命名空间

root = Tk()


def lab():
    label0 = Label(root, text="label1")
    label0.grid(column=0)


def p(event):  # 要加event
    print("hello world")


root.title("hello world")  # 窗口标题
# 第一种
btn0 = Button(root, text="button", command=lab)  # 按下调用函数lab
btn0.grid(row=0, column=0, sticky=EW)
# 第二种
btn1 = Button(root, text="button")
btn1.grid(row=0, column=1)
btn1.bind("<Button-1>", p)  # 鼠标左键，按下调用函数p
"""
1.我们在使用 bind 函数的时候事件
2.<Button-1>表示鼠标左键单击，3 右,2中
3.<KeyPress-A>表示 A 键被按下
4.<Control-V>表示按下的是 Ctrl 和 V 键
5.<F1>表示按下的是 F1 键"""

ent = Entry(root)  # 输入框
ent.grid(row=1, column=0)
ent['show'] = "*"  # 掩码
ent.bind("<KeyPress-\n>", p)  # 在输入框按下回车，调用函数p

btn0['background'] = "blue"
print(btn0["text"])

root.mainloop()
