# -*- coding: utf-8 -*-

from core.interface import print_line


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


class RequestBase(object):
    pass


@singleton
class RequestLogin(RequestBase):
    pass


@singleton
class RequestCreatePlatform(RequestBase):
    pass
