# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import ChatNotesModel
from peewee import DoesNotExist


class ChatNotesModelDao:
    @staticmethod
    def query_notes(room_id):
        """
        查找某个room_id下的记录
        :param room_id:
        :return:
        """
        try:
            return ChatNotesModel.select().where((ChatNotesModel.room_id == room_id)).execute()
        except Exception as error:
            print(error)
            return None

    @staticmethod
    def query_one_note(note_id):
        """
        :param note_id:
        :return:
        """
        try:
            return ChatNotesModel.get(ChatNotesModel.id == note_id)
        except Exception as error:
            print(error)
            return None

    @staticmethod
    def add_note(room_id, user_id, message, time):
        try:
            # 插入成功后返回note_id
            note_id = ChatNotesModel.insert(room_id=room_id, user_id=user_id, message=message,
                                            time=time).execute()
            return note_id
        except Exception as error:
            print(error)
            return False



