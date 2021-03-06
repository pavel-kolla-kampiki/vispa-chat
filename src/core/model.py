# -*- coding: utf-8 -*-

__author__ = 'degibenz'

import asyncio

from aiohttp.log import *
from bson.objectid import ObjectId

from configs.db import DB

__all__ = [
    'Model',
    'ObjectId'
]

# TODO было бы хорошо, сделать тут полноценное удержание соединения
database = DB()


def init_model(loop=None):
    connection = database.hold_connect()
    return connection


class Model(object):
    pk = None
    db = None
    collection = None
    loop = None

    result = {}

    def __init__(self, **kwargs):
        if 'io_loop' in kwargs.keys():
            self.loop = kwargs.get('io_loop')

    async def get(self):
        assert self.pk is not None

        try:
            self.result = await self.objects.find_one(
                {
                    "_id": ObjectId(self.pk)
                }
            )
        except(Exception,) as error:
            self.result = {
                'status': False,
                'error': '%s' % error
            }

            access_logger.error("%s" % self.result)

        finally:
            return self.result

    async def save(self, **kwargs):
        try:
            self.result = await self.objects.insert(
                kwargs
            )

            self.pk = self.result

        except(Exception,) as error:
            self.result = {
                'status': False,
                'error': '%s' % error
            }

        finally:
            return self.result

    async def delete(self):

        try:
            self.objects.remove(
                {
                    "_id": ObjectId(self.pk)
                }
            )

            self.result = {
                'status': True
            }
        except(Exception,) as error:
            self.result = {
                'status': False,
                'error': '%s' % error
            }

        finally:
            return self.result

    @property
    def objects(self):
        return self.db["%s" % self.collection]
