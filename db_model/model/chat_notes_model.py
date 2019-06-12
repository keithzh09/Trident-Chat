# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import BaseModel
from peewee import CharField, BigIntegerField, TextField


class ChatNotesModel(BaseModel):
    room_id = BigIntegerField()
    user_id = BigIntegerField()
    message = TextField()
    # picture_url = CharField(max_length=128)
    time = CharField(max_length=20)  # 2018-01-01 23:00:01

    class Meta:
        db_table = 'chat_notes'
