# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import ChatRoomsModel
from peewee import DoesNotExist


class ChatRoomsModelDao:
    @staticmethod
    def get_id_by_name(name):
        try:
            obj = ChatRoomsModel.get(ChatRoomsModel.name == name)
            return obj.id
        except DoesNotExist:
            return None

    @staticmethod
    def get_all_rooms():
        try:
            model_list = ChatRoomsModel.select().where((ChatRoomsModel.id >= 0)).execute()
            name_list = [model.name for model in model_list]
            return name_list
        except Exception as error:
            print(error)
            return None

