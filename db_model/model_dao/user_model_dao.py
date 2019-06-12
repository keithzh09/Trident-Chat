# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

from ..model import UserModel
from peewee import DoesNotExist
from lib.MD5_encrypt import md5_encrypt


class UserModelDao:

    @staticmethod
    def check_user_and_user_pwd(user_name, user_pwd):
        """
        检查user_code和user_key
        :param user_name: 用户名
        :param user_pwd: 用户密码
        :return: 验证通过：user_id， 不存在用户：-1，密码错误：-2
        """
        try:
            user_obj = UserModel.get(UserModel.name == user_name)
        except DoesNotExist:
            return 'User doesn\'t exist'
        else:
            # 将user_key先MD5加密
            user_pwd = md5_encrypt(user_pwd)
            return 'Correct' if user_obj.password == user_pwd else 'User\'s password is incorrect'

    @staticmethod
    def get_name_by_user_id(user_id):
        """
        通过用户ID查询数据
        :param user_id:用户id
        :return:
        """
        try:
            user_obj = UserModel.get(UserModel.id == user_id)
            return user_obj.name
        except DoesNotExist:
            return None

    @staticmethod
    def get_id_by_user_name(user_name):
        """
        通过用户ID查询数据
        :param user_name:用户名
        :return:
        """
        try:
            user_obj = UserModel.get(UserModel.name == user_name)
            return user_obj.id
        except DoesNotExist:
            return None

    @staticmethod
    def add_user(user_name, user_pwd):
        """
        创建新用户，user_state在数据库设置默认值为1
        :param user_name: 用户名
        :param user_pwd: 用户密码
        :return:
        """
        try:
            UserModel.get(UserModel.name == user_name)
            return 'User was existed'
        except DoesNotExist:
            pass
        try:
            user_pwd = md5_encrypt(user_pwd)
            id = UserModel.insert(name=user_name, password=user_pwd).execute()
            return 'Succeed'
        except Exception as error:
            print(error)
            return 'Fail'

