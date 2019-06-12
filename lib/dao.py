# coding: utf-8
# @author  : lin
# @time    : 2019/6/3

# from . import config
from config.db_config import redis_client
from lib.MD5_encrypt import md5_encrypt
from time import time
from datetime import datetime

server_token_key = "server_user _"  # token 与 user_id记录的redis key前缀
user_token_timeout = 3600 * 24  # token有效期
timer_token = "timer_"  # 利用redis计数器实现自增id，防止高并发下token重复

client_token_key = 'client_user_'


class LibDao:

    @staticmethod
    def get_user_name_from_token(token):
        """
        根据token获取用户名
        :param token: token
        :return:
        """
        if not token:
            return 0
        cache_key1 = server_token_key + token
        user_name = redis_client.get(cache_key1)
        if user_name:  # 不存在时为None
            # 设置过期时间
            user_name = user_name.decode('utf-8')  # 二进制转化成字符串
            cache_key2 = server_token_key + user_name
            redis_client.expire(cache_key1, user_token_timeout)
            redis_client.expire(cache_key2, user_token_timeout)
            return user_name
        else:
            return None

    @staticmethod
    def if_token_valid(token):
        """
        token必须在与对应的用户名成功时生效,即说明一个用户重新登陆后,无法再用原来的token
        :param token: token
        :return:
        """
        if not token:
            return False
        cache_key1 = server_token_key + token
        user_name = redis_client.get(cache_key1)
        if user_name:
            user_name = user_name.decode('utf-8')
            cache_key2 = server_token_key + user_name
            real_token = redis_client.get(cache_key2)
            if real_token:
                real_token = real_token.decode('utf-8')
                if real_token == token:
                    return True
        return False

    @staticmethod
    def set_user_name_token(user_name):
        """
        记录token数据
        :param user_name: 用户名
        :return:
        """
        token = LibDao.get_one_token()
        cache_key1 = server_token_key + token
        cache_key2 = server_token_key + user_name
        redis_client.set(cache_key1, user_name)
        redis_client.set(cache_key2, token)
        # 设置超时时间
        redis_client.expire(cache_key1, user_token_timeout)
        redis_client.expire(cache_key2, user_token_timeout)
        return token

    @staticmethod
    def get_one_token():
        """
        随机生成一个32位的字符串
        :return:
        """
        timer_key = timer_token + datetime.now().strftime("%Y-%m-%d")
        # 自增，防止高并发下重复
        timer_id = redis_client.incr(timer_key)
        # redis_client.expire(timer_key, user_token_timeout)
        d = str(time()) + "_" + str(timer_id)
        return md5_encrypt(d)

    @staticmethod
    def delete_one_token(token):
        cache_key1 = server_token_key + token
        user_name = redis_client.get(cache_key1)
        user_name = user_name.decode('utf-8')  # 二进制转化成字符串
        cache_key2 = server_token_key + user_name
        redis_client.delete(cache_key1)
        redis_client.delete(cache_key2)

    @staticmethod
    def set_client_user_token(user_name, token):
        """
        客户端使用，记录token数据，key为前缀+用户名，value为token
        :param user_name: 用户名
        :param token:
        :return:
        """
        print('set', user_name, 'token')
        cache_key = client_token_key + user_name
        redis_client.set(cache_key, token)
        # 设置超时时间
        redis_client.expire(cache_key, user_token_timeout)
        return 'Success'

    @staticmethod
    def get_client_token_by_user_name(user_name):
        """
        客户端使用，根据用户名得到其token
        :param user_name:
        :return:
        """

        cache_key = client_token_key + user_name
        data = redis_client.get(cache_key)
        data = data.decode('utf-8')   # 二进制转化成字符串
        print('get_',user_name,'token')
        if data:
            # 重新设置过期时间
            redis_client.expire(cache_key, user_token_timeout)
            return data
        else:
            return None
