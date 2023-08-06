# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_tortoise_orm']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'tortoise-orm[asyncpg]>=0.19.1,<0.20.0']

setup_kwargs = {
    'name': 'nonebot-plugin-tortoise-orm',
    'version': '0.0.1a0',
    'description': '一个通用数据库连接插件',
    'long_description': '# 通用 ORM 数据库连接插件\n\n> 施工中。。。\n\n- 参考 [example_bot](example_bot) 来创建一个 聊天记录 插件吧~！\n\n## 数据库类型\n\n- [x] postgres\n- [ ] sqlite\n\n其他待补充\n',
    'author': 'kexue',
    'author_email': 'x@kexue.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kexue-z/nonebot-plugin-tortoise-orm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
