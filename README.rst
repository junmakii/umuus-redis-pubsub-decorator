
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