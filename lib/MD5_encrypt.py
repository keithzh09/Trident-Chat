# coding: utf-8
# @author: lin
# @date: 19-02-28

import hashlib


def md5_encrypt(data):
    """
    MD5加密
    :param data:
    :return:
    """
    m = hashlib.md5()
    m.update(data.encode('UTF-8'))
    return m.hexdigest()
