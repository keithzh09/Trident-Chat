# coding: utf-8
# @author  : lin
# @time    : 2019/6/3


HOST = "39.106.53.169"
PORT = 1883

# 定义topic
# TOPIC = {'登录': 'login', '注册': 'register', '聊天': 'chat'}

# 登录时的token由客户端生成
login_params = ['user_name', 'user_pwd']  # user_room不确定要不要下
register_params = ['user_name', 'user_pwd', 'project_code']
chat_params = ['token', 'msg', 'time', 'room_name']
all_notes_params = ['token', 'room_name']

TOPIC_PARAMS = {'login': login_params, 'register': register_params,
                'chat': chat_params, 'all_notes': all_notes_params}
PROJECT_CODE = 'HELLO WORLD'

# 服务端发送给客户端的反馈格式为： topic: user_name, 成功时数据为{'token': 'xxxxx', 'all_rooms': []}
# 服务端发送给客户端一个房间所有数据： topic为房间名，数据为{'all_notes': data},
# data是[user_name, model.message, model.time]
# 服务端发送给客户端最新消息
