# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yastyleguide', 'yastyleguide.checkers', 'yastyleguide.visitors']

package_data = \
{'': ['*']}

install_requires = \
['black>=21.11b1,<22.0',
 'flake8-annotations-complexity>=0.0.6,<0.0.7',
 'flake8-bandit>=2.1.2,<3.0.0',
 'flake8-black>=0.2.3,<0.3.0',
 'flake8-bugbear>=21.9.2,<22.0.0',
 'flake8-builtins>=1.5.3,<2.0.0',
 'flake8-comprehensions>=3.7.0,<4.0.0',
 'flake8-docstrings>=1.6.0,<2.0.0',
 'flake8-eradicate>=1.2.0,<2.0.0',
 'flake8-expression-complexity>=0.0.9,<0.0.10',
 'flake8-isort>=4.1.1,<5.0.0',
 'flake8-requirements>=1.5.1,<2.0.0',
 'flake8-string-format>=0.3.0,<0.4.0',
 'flake8>=4.0.1,<5.0.0',
 'nitpick>=0.29.0,<0.30.0',
 'pandas-vet>=0.2.2,<0.3.0',
 'pep8-naming>=0.12.1,<0.13.0']

entry_points = \
{'flake8.extension': ['YASG = yastyleguide.plugin:YASGPlugin']}

setup_kwargs = {
    'name': 'yastyleguide',
    'version': '0.0.3',
    'description': 'Yet another styleguide.',
    'long_description': '# yastyleguide\nYet another styleguide\n\n\n## Install\n#### From gitlab pypi repository:\n<details><summary>Create gitlab access token.</summary>\n\nGo to page [gitlab settings](https://gitlab.com/-/profile/personal_access_tokens).\nCreate gitlab access token with scopes:\n- api\n- read-api\n- read_registry\n- write_registry\n\n</details>\n\nSet poetry http-basic authentication by token:\n```bash\n poetry config http-basic.yastyleguide <gitlab-access-token-name> <gitlab-access-token>\n```\nWrite to **pyproject.toml**:\n```toml\n[[tool.poetry.source]]\nname = "yastyleguide"\nurl = "https://gitlab.com/api/v4/projects/31783240/packages/pypi/simple"\nsecondary = true\n```\nInstall by poetry:\n```bash\npoetry add yastyleguide -D --source=yastyleguide\n```\n\n#### From source:\n```bash\ngit clone https://gitlab.com/ds.team/general/yastyleguide\ncd yastyleguide \npoetry build\npip install dist/yastyleguide-0.0.3.tar.gz\n```\n\n#### From [dist](https://gitlab.com/ds.team/general/yastyleguide/-/jobs/1845796021/artifacts/download) release:\n```bash\nunzip artifacts.zip\npip install dist/yastyleguide-0.0.3.tar.gz\n```\n\n#### From [git](it+https://gitlab.com/ds.team/general/yastyleguide):\n```bash\npoetry add git+https://gitlab.com/ds.team/general/yastyleguide\n```\n<details><summary>Публичный вариант</summary>\n\n```bash\npoetry add git+https://github.com/levkovalenko/yastyleguide\n```\n</details>\n\n## Nitpick styleguide\n\nYou can use base settings for linters with [nitpick](https://github.com/andreoliwa/nitpick):\n```toml\n[tool.nitpick]\nstyle = "https://gitlab.com/ds.team/general/yastyleguide/-/blob/master/styles/nitpick-yastyle.toml"\n```\n<details><summary>Публичный вариант</summary>\n\n```toml\n[tool.nitpick]\nstyle = "https://raw.githubusercontent.com/levkovalenko/yastyleguide/master/styles/nitpick-yastyle.toml"\n```\n</details>\n\n## Running\nIt\'s just plugin **flake8**, so:\n```bash\nflake8 .\n```\n\n## Violations\nOur own codes:\n|Code|Description|\n|----|-----------|\n|YASG101|`Don\'t use any \'for\' loops.`|\n|YASG102|`Don\'t use any \'while\' loops.`|\n|YASG201|`Line is to complex, {0} > {1}. To many ast nodes per line.`|\n|YASG202|`To big median line complexity in module, {0} > {1}.`|\n|YASG203|`To many lines per module, {0} > {1}.`|\n|YASG204|`To many function definitions per module, {0} > {1}.`|\n|YASG205|`To many class definitions per module, {0} > {1}.`|\n\nYou can read about external plugins violations at [/docs/eng/plugin_list.md](docs/eng/plugin_list.md)',
    'author': 'levkovalenko',
    'author_email': 'levozavr@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/levkovalenko/yastyleguide',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
