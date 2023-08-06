# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_r6s']

package_data = \
{'': ['*'],
 'nonebot_plugin_r6s': ['fonts/*',
                        'imgs/avatar/*',
                        'imgs/operators/*',
                        'imgs/ranks/*']}

install_requires = \
['Pillow>=8.4.0,<9.0.0',
 'httpx>=0.21.1,<1.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-r6s',
    'version': '0.4.2',
    'description': 'A R6s plugin for Nonebot2',
    'long_description': '<div align="center">\n\n# NoneBot Plugin R6s\n\nRainbow Six Siege Players Searcher For Nonebot2\n\n</div>\n\n</div>\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/abrahum/nonebot-plugin-r6s/master/LICENSE">\n    <img src="https://img.shields.io/github/license/abrahum/nonebot_plugin_r6s.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-r6s">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-r6s.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.7.3+-blue.svg" alt="python">\n</p>\n\n## 使用方法\n\n``` zsh\nnb plugin install nonebot-plugin-r6s // or\npip install --upgrade nonebot-plugin-r6s\n```\n在 Nonebot2 入口文件（例如 bot.py ）增加：\n``` python\nnonebot.load_plugin("nonebot_plugin_r6s")\n```\n\n## 指令详解\n\n|  指令  |          别名          | 可接受参数 | 功能                                                         |\n| :----: | :--------------------: | ---------- | ------------------------------------------------------------ |\n|  r6s   | 彩六，彩虹六号，r6，R6 | 昵称       | 查询玩家基本信息                                             |\n| r6spro |      r6pro，R6pro      | 昵称       | 查询玩家进阶信息                                             |\n| r6sops |      r6ops，R6ops      | 昵称       | 查询玩家干员信息                                             |\n|  r6sp  |        r6p，R6p        | 昵称       | 查询玩家 ~~近期对战~~ 历史段位信息                           |\n| r6sset |      r6set，R6set      | 昵称       | 设置玩家昵称，设置后其余指令可以不带昵称即查询已设置昵称信息 |\n\n## 更新日志\n\n### 0.4.2\n\n- 增加玩家基本信息以及进阶信息数据:\n  > 玩家基本信息: 更新玩家当前赛季非排以及当前赛季排位MMR分数  \n  玩家进阶信息:   \n  1.将非排和排位数据中MMR更新为当前赛季MMR  \n  2.新增最高段位赛季数据 最高MMR和结束赛季时最终MMR 胜场以及负场\n- 修复已知BUG:\n  > 修复因玩家头像获取不到导致的出错  \n  修复因干员头像获取不到导致的出错\n\n> Thanks for [#6](https://github.com/abrahum/nonebot_plugin_r6s/pull/6)\n\n### 0.4.1\n\n- fix dependencies [#4](https://github.com/abrahum/nonebot_plugin_r6s/pull/4)\n\n### 0.4.0\n\n- 适配 Nonebot2-beta.1\n- python3.7.3+ 与 nonebot2 保持一致\n\n### 0.3.0\n\n- 变更为使用图片回复，旧文字消息暂时停用（未来看情况作为可选）\n- 添加 oop 中间件，为未来可能的其他数据来源提供便利\n- 要求版本上升为 Python3.8 （还有人在用 3.7 以下? 不会吧? 不会吧? )\n\n### 0.2.2\n\n- ground 数据源失效，暂时完全切换回 r6scn ，部分无法查询问题会重现。*2021.05.24*\n\n### 0.2.1\n\n- 更换优先使用 ground 数据源，cn 数据源存在排位休闲数据错位，改名后数据长期未更新问题。\n- ground 数据源乱码严重，目前无法识别干员数据和近期对战数据\n- 已知 ground 数据源第一次使用会返回未更新数据，待研究解决（咕咕咕）\n- 针对有 Ubi 账号未游玩 R6s 账号返回 Not Found\n\n## 已知问题\n\n- r6scn 不再更新数据\n\n## 特别鸣谢\n\n[nonebot/nonebot2](https://github.com/nonebot/nonebot2/)：简单好用，扩展性极强的 Bot 框架\n\n[Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：更新迭代快如疯狗的 [OneBot](https://github.com/howmanybots/onebot/blob/master/README.md) Golang 原生实现\n\n',
    'author': 'abrahumlink',
    'author_email': '307887491@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/abrahum/nonebot_plugin_r6s',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
