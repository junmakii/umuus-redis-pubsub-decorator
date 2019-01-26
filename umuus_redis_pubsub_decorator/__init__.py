#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Jun Makii <junmakii@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Utilities, tools, and scripts for Python.

umuus-redis-pubsub-decorator
============================

Installation
------------

    $ pip install git+https://github.com/junmakii/umuus-redis-pubsub-decorator.git

Example
-------

    $ export UMUUS_REDIS_PUBSUB_DECORATOR_REDIS_CONF_FILE=/PATH/FILE.json

    $ umuus_redis_pubsub_decorator

    >>> import umuus_redis_pubsub_decorator


----

    $ cat CONFIG.json

    {
        "redis_pubsub_util": {
            "config": {
                "host": "redis",
                "port": 6379,
                "password": "ehu493jfqn8d"
            }
        },
        "paths": ["example:foo", "example:bar"]
    }

    $ python umuus_redis_pubsub_decorator.py run --options "$(cat CONFIG.json)"

----

    redis_pubsub_decorator = umuus_redis_pubsub_decorator.RedisPubSubUtil(config={"host": "redis", "port": 6379})

    @redis_pubsub_decorator.publish()
    def f(x, y):
        return x * y

    @redis_pubsub_decorator.subscribe()
    def g(x, y):
        print('SUBSCRIBED:g')
        return x * y

    @redis_pubsub_decorator.subscribe()
    def h(x, y):
        print('SUBSCRIBED:h')
        return x * y

    redis_pubsub_decorator.run()

----

    $ redis-cli PSUBSCRIBE '*' &

    $ redis-cli PUBLISH '__main__.h' '{"x": 1, "y": 2}'

    $ redis-cli PUBLISH '__main__.g' '{"x": 1, "y": 2}'

----

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

"""
import os
import sys
import json
import functools
import logging
logger = logging.getLogger(__name__)
import fire
import redis
import attr
import addict
import asyncio
import toolz
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-redis-pubsub-decorator'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__author_username__ = 'junmakii'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'redis>=3.0.1',
    'toolz>=0.9.0',
    'fire>=0.1.3',
    'attrs>=18.2.0',
]
__dependency_links__ = []
__classifiers__ = []
__entry_points__ = {}
__project_urls__ = {}
__setup_requires__ = []
__test_suite__ = ''
__tests_require__ = []
__extras_require__ = {}
__package_data__ = {}
__python_requires__ = ''
__include_package_data__ = True
__zip_safe__ = True
__static_files__ = {}
__extra_options__ = {}
__download_url__ = ''
__all__ = []


@attr.s()
class RedisPubSubListener(object):
    parent = attr.ib(None)
    fn = attr.ib(None)
    interval = attr.ib(0.1)
    encoding = attr.ib(sys.getdefaultencoding())
    name = attr.ib(__name__)

    def __attrs_post_init__(self):
        self.name = self.fn.__module__ + '.' + self.fn.__qualname__

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

    async def run(self):
        self.parent.pubsub.subscribe(self.name)
        while True:
            try:
                message = self.parent.pubsub.get_message()
                if message and message.get('type') == 'message':
                    result = self.fn(**self.parent.serializer(
                        message.get('data').decode(self.encoding)))
                    self.parent.instance.publish(
                        self.name + ':on_completed',
                        self.parent.serializer(result))
            except Exception as err:
                self.parent.instance.publish(self.name + ':on_error',
                                             json.dumps(dict(error=str(err))))
            await asyncio.sleep(self.interval)


@attr.s()
class RedisPubSubUtil(object):
    file = attr.ib(None)
    name = attr.ib(__name__)
    config = attr.ib(None)
    instance = attr.ib(None)
    env = attr.ib(None)
    serializer = attr.ib(lambda _: toolz.excepts(Exception, lambda _: addict.Dict(json.loads(_)), lambda err: _)(_))
    subscriptions = attr.ib([])

    def __attrs_post_init__(self):
        if not self.env:
            self.env = os.environ.get(
                self.name.replace('.', '__').upper() + '_REDIS_CONF_FILE')
        if not self.instance:
            self.instance = redis.Redis(
                **(self.config or json.load(open(self.file or self.env))))
            self.pubsub = self.instance.pubsub()

    @toolz.curry
    def publish(self, fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            self.instance.publish(fn.__qualname__, self.serializer(result))
            return result

        return wrapper

    @toolz.curry
    def subscribe(self, fn):
        listener = RedisPubSubListener(fn=fn, parent=self)
        self.subscriptions.append(listener)
        return self

    def run_coroutines(self):
        return list(map(lambda _: _.run(), self.subscriptions))

    def run(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(asyncio.gather(*self.run_coroutines()))


def run(options={}):
    options = addict.Dict(options)
    redis_pubsub_util = RedisPubSubUtil(**options.redis_pubsub_util)
    [
        redis_pubsub_util.subscribe()(getattr(
            __import__(module_name), function_name)) for path in options.paths
        for module_name, function_name in [path.split(':')]
    ]
    redis_pubsub_util.run()


def main(argv=[]):  # type: int
    fire.Fire()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
