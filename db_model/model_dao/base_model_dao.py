# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import UserModel, ChatRoomsModel, ChatNotesModel


class BaseModelDao:
    @staticmethod
    def create_table(table):
        """
        如果table不存在，新建table
        """
        if not table.table_exists():
            table.create_table()

    @staticmethod
    def drop_table(table):
        """
        table 存在，就删除
        """
        if table.table_exists():
            table.drop_table()

    @staticmethod
    def create_all_tables():
        BaseModelDao.create_table(UserModel)
        BaseModelDao.create_table(ChatRoomsModel)
        BaseModelDao.create_table(ChatNotesModel)

    @staticmethod
    def drop_all_tables():
        BaseModelDao.drop_table(UserModel)
        BaseModelDao.drop_table(ChatRoomsModel)
        BaseModelDao.drop_table(ChatNotesModel)



