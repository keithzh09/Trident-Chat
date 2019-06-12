# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import BaseModel
from peewee import CharField, BigIntegerField, TextField


class UserModel(BaseModel):
    name = CharField(max_length=64)
    password = CharField(max_length=32)

    class Meta:
        db_table = 'user'
