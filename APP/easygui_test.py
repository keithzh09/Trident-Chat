from tkinter import *

root = Tk()


def lab():
    label0 = Label(root, text="hello world")
    label0.grid(column=0)


root.geometry("800x480")  # 窗口大小

menu0 = Menu(root)  # 参数是父级控件

# 二级菜单
cascade0 = Menu(menu0, tearoff=False)  # tearoff=False 表示这个菜单不可以被拖出来

cascade0.add_separator()  # 分割线
# cascade0.add_checkbutton(label="在不调试的情况下启动")  # 单选框
cascade0.add_radiobutton(label="闲聊")  # 多选框
cascade0.add_radiobutton(label="测试")  # 多选框
cascade0.add_separator()  # 分割线
menu0.add_cascade(label='项目', menu=cascade0)  # 在menu0中添加一个label为项目的级联菜单

cascade1 = Menu(menu0, tearoff=False)
for x in ['注销', '退出']:
    cascade1.add_command(label=x, command=lab)

menu0.add_cascade(label='用户', menu=cascade1)

root['menu'] = menu0  # 窗口root的menu是menu0

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
