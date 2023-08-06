# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyxxl', 'pyxxl.tests', 'pyxxl.tests.api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0']

setup_kwargs = {
    'name': 'pyxxl',
    'version': '0.1.5',
    'description': 'A Python executor for XXL-jobs',
    'long_description': 'xxl-jobs 的python客户端实现\n=============================\n\n.. image:: https://img.shields.io/pypi/v/pyxxl?color=%2334D058&label=pypi%20package\n    :target: https://pypi.org/project/pyxxl\n\n.. image:: https://img.shields.io/pypi/pyversions/pyxxl.svg?color=%2334D058\n    :target: https://pypi.org/project/pyxxl\n\n.. image:: https://img.shields.io/codecov/c/github/fcfangcc/pyxxl?color=%2334D058\n    :target: https://codecov.io/gh/fcfangcc/pyxxl\n\n\n使用pyxxl可以方便的把Python写的方法注册到xxl-job中,使用xxl-job-admin管理Python定时任务和周期任务\n\n如何使用\n=======================\n.. code:: shell\n\n    pip install pyxxl\n\n具体可以查看example文件夹下面的2个例子\n\n.. code:: python\n\n    import logging\n    import asyncio\n\n    from pyxxl import PyxxlRunner, JobHandler\n\n    logger = logging.getLogger("pyxxl")\n    logger.setLevel(logging.INFO)\n    xxl_handler = JobHandler()\n\n    @xxl_handler.register\n    async def test_task():\n        await asyncio.sleep(30)\n        return "成功30"\n\n\n    @xxl_handler.register(name="xxxxx")\n    @xxxxx # 自己定义的装饰器必须放在下面\n    async def abc():\n        await asyncio.sleep(3)\n        return "成功3"\n\n\n    runner = PyxxlRunner(\n        "http://localhost:8080/xxl-job-admin/api/",\n        executor_name="xxl-job-executor-sample",\n        port=9999,\n        host="172.17.0.1",\n        handler=xxl_handler,\n    )\n    runner.run_executor()\n\n\n\n\n开发人员\n=======================\n下面是开发人员如何快捷的搭建开发调试环境\n\n=====================\n启动xxl的调度中心\n=====================\n\n.. code:: shell\n\n    ./init_dev_env.sh\n\n=====================\n启动执行器\n=====================\n.. code:: shell\n\n    poetry install\n    # 修改app.py中相关的配置信息,然后启动\n    poetry run python example/app.py\n\n\n======================\nTODOs\n======================\n\n- [x] 自定义查看日志函数\n- [x] docs\n',
    'author': 'fcfangcc',
    'author_email': 'swjfc22@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fcfangcc/pyxxl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
