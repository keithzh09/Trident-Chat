# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import BaseModel
from peewee import CharField, BigIntegerField, TextField


class ChatRoomsModel(BaseModel):
    name = CharField(max_length=64)

    class Meta:
        db_table = 'chat_rooms'
