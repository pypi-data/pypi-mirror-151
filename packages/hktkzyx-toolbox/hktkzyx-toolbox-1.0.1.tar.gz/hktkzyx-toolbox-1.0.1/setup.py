# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hktkzyx_toolbox', 'hktkzyx_toolbox.finance', 'hktkzyx_toolbox.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'numpy>=1.22.3,<2.0.0', 'scipy>=1.7.1,<2.0.0']

extras_require = \
{'docs': ['mike>=1.1.2,<2.0.0',
          'mkdocs>=1.3.0,<2.0.0',
          'mkdocs-material>=8.2.8,<9.0.0',
          'mkdocstrings-python-legacy>=0.2.2,<0.3.0',
          'pytkdocs[numpy-style]>=0.16.1,<0.17.0'],
 'test': ['pytest>=7.1.1,<8.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['hktkzyx-electronics = '
                     'hktkzyx_toolbox.scripts.electronics:hktkzyx_electronics',
                     'hktkzyx-finance = '
                     'hktkzyx_toolbox.scripts.finance:hktkzyx_finance']}

setup_kwargs = {
    'name': 'hktkzyx-toolbox',
    'version': '1.0.1',
    'description': 'Toolbox of hktkzyx.',
    'long_description': '# hktkzyx toolbox 文档\n\n[Official Website](https://hktkzyx.github.io/hktkzyx-toolbox/) | @hktkzyx/hktkzyx-toolbox\n\nhktkzyx toolbox 是 hktkzyx 的一个工具箱应用。\n目前该工具箱主要采用命令行接口，具有一下功能：\n\n- 养老保险计算\n\n    计算城镇居民养老保险的预期待遇\n\n- LED 分压电阻、电流计算\n\n    计算 LED 的分压电阻大小\n\n- 标准电阻查询\n\n    根据电阻值查询标准电阻\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hktkzyx/hktkzyx-toolbox/build-and-test)](https://github.com/hktkzyx/hktkzyx-toolbox/actions)\n[![Codecov](https://img.shields.io/codecov/c/github/hktkzyx/hktkzyx-toolbox)](https://app.codecov.io/gh/hktkzyx/hktkzyx-toolbox)\n[![PyPI - License](https://img.shields.io/pypi/l/hktkzyx-toolbox)](https://github.com/hktkzyx/hktkzyx-toolbox/blob/main/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/hktkzyx-toolbox)](https://pypi.org/project/hktkzyx-toolbox/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hktkzyx-toolbox)](https://pypi.org/project/hktkzyx-toolbox/)\n[![GitHub last commit](https://img.shields.io/github/last-commit/hktkzyx/hktkzyx-toolbox)](https://github.com/hktkzyx/hktkzyx-toolbox)\n\n## 安装\n\n```bash\npip install hktkzyx-toolbox\n```\n\n## 使用\n\n查询金融工具箱的命令和用法\n\n```bash\nhktkzyx-finance --help\n```\n\n查询电子工具箱的命令和用法\n\n```bash\nhktkzyx-electronics --help\n```\n\n## 如何贡献\n\n十分欢迎 Fork 本项目！\n欢迎修复 bug 或开发新功能。\n开发时请遵循以下步骤:\n\n1. 使用 [poetry](https://python-poetry.org/) 作为依赖管理\n\n    克隆项目后，在项目文件夹运行\n\n    ```bash\n    poetry install\n    ```\n\n2. 使用 [pre-commit](https://pre-commit.com/) 并遵守 [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) 规范\n\n    安装 pre-commit 并运行\n\n    ```bash\n    pre-commit install -t pre-commit -t commit-msg\n    ```\n\n    建议使用 [commitizen](https://github.com/commitizen-tools/commitizen) 提交您的 commits。\n\n3. 建议遵循 [gitflow](https://nvie.com/posts/a-successful-git-branching-model/) 分支管理策略\n\n    安装 [git-flow](https://github.com/petervanderdoes/gitflow-avh) 管理您的分支并运行\n\n    ```bash\n    git config gitflow.branch.master main\n    git config gitflow.prefix.versiontag v\n    git flow init -d\n    ```\n\n4. PR 代码到 develop 分支\n\n*[PR]: Pull request\n\n## 许可证\n\nCopyright (c) 2022 Brooks YUAN.\n\nEnvironment Sensor Bluetooth firmware is licensed under Mulan PSL v2.\n\nYou can use this software according to the terms and conditions of the Mulan PSL v2.\nYou may obtain a copy of Mulan PSL v2 at: <http://license.coscl.org.cn/MulanPSL2>.\n\nTHIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,\nEITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,\nMERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.\n\nSee the Mulan PSL v2 for more details.\n',
    'author': 'Brooks YUAN',
    'author_email': 'hktkzyx@yeah.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hktkzyx.github.io/hktkzyx-toolbox/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
