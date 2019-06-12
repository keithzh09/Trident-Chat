# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from db_model.model_dao import BaseModelDao, ChatRoomsModelDao, ChatNotesModelDao, UserModelDao
from db_model.model import UserModel, ChatNotesModel

# BaseModelDao.drop_table(UserModel)
# BaseModelDao.drop_table(ChatNotesModel)
# BaseModelDao.create_all_tables()
# UserModelDao.add_user('Trident', '112366')
# ChatNotesModelDao.add_note(1, 1, 'Hello World!', '2019-06-05 00:34:53')

from server import Server

server = Server()
server.start_loop()

# from queue import Queue
# from config.db_config import redis_client

# import datetime
# now_time = datetime.datetime.now().strftime('%H:%M:%S')
# print(type(now_time))
