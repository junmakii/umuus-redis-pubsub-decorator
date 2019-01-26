
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        import sys
        import shlex
        import pytest
        errno = pytest.main(['--doctest-modules'])
        if errno != 0:
            raise Exception('An error occured during installution.')
        install.run(self)


setup(
    packages=setuptools.find_packages('.'),
    version='0.1',
    url='https://github.com/junmakii/umuus-redis-pubsub-decorator',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['redis>=3.0.1', 'toolz>=0.9.0', 'fire>=0.1.3', 'attrs>=18.2.0'],
    dependency_links=[],
    classifiers=[],
    entry_points={},
    project_urls={},
    setup_requires=[],
    test_suite='',
    tests_require=[],
    extras_require={},
    package_data={},
    python_requires='',
    include_package_data=True,
    zip_safe=True,
    name='umuus-redis-pubsub-decorator',
    description='Utilities, tools, and scripts for Python.',
    long_description=('Utilities, tools, and scripts for Python.\n'
 '\n'
 'umuus-redis-pubsub-decorator\n'
 '============================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install '
 'git+https://github.com/junmakii/umuus-redis-pubsub-decorator.git\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ export UMUUS_REDIS_PUBSUB_DECORATOR=/PATH/FILE.json\n'
 '\n'
 '    $ umuus_redis_pubsub_decorator\n'
 '\n'
 '    >>> import umuus_redis_pubsub_decorator\n'
 '\n'
 '\n'
 '----\n'
 '\n'
 '    $ cat CONFIG.json\n'
 '\n'
 '    {\n'
 '        "redis_pubsub_util": {\n'
 '            "config": {\n'
 '                "host": "redis",\n'
 '                "port": 6379,\n'
 '                "password": "ehu493jfqn8d"\n'
 '            }\n'
 '        },\n'
 '        "paths": ["example:foo", "example:bar"]\n'
 '    }\n'
 '\n'
 '    $ python umuus_redis_pubsub_decorator.py run --options "$(cat '
 'CONFIG.json)"\n'
 '\n'
 '----\n'
 '\n'
 '    redis_pubsub_decorator = '
 'umuus_redis_pubsub_decorator.RedisPubSubUtil(config={"host": "redis", '
 '"port": 6379})\n'
 '\n'
 '    @redis_pubsub_decorator.publish()\n'
 '    def f(x, y):\n'
 '        return x * y\n'
 '\n'
 '    @redis_pubsub_decorator.subscribe()\n'
 '    def g(x, y):\n'
 "        print('SUBSCRIBED:g')\n"
 '        return x * y\n'
 '\n'
 '    @redis_pubsub_decorator.subscribe()\n'
 '    def h(x, y):\n'
 "        print('SUBSCRIBED:h')\n"
 '        return x * y\n'
 '\n'
 '    redis_pubsub_decorator.run()\n'
 '\n'
 '----\n'
 '\n'
 "    $ redis-cli PSUBSCRIBE '*' &\n"
 '\n'
 '    $ redis-cli PUBLISH \'__main__.h\' \'{"x": 1, "y": 2}\'\n'
 '\n'
 '    $ redis-cli PUBLISH \'__main__.g\' \'{"x": 1, "y": 2}\'\n'
 '\n'
 '----\n'
 '\n'
 '    @umuus_redis_pubsub_decorator.default_instance.subscribe()\n'
 '    def f(x, y):\n'
 "        print('f')\n"
 '        return x * y\n'
 '\n'
 '    umuus_redis_pubsub_decorator.default_instance.run()\n'
 '\n'
 '----\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>'),
    cmdclass={"pytest": PyTest},
)
