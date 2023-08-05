# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['readtime_cli']

package_data = \
{'': ['*']}

install_requires = \
['readtime>=1.1.1,<2.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['readtime = readtime_cli.main:app']}

setup_kwargs = {
    'name': 'readtime-cli',
    'version': '0.1.1',
    'description': "CLI to calculates the time some text takes the average human to read, based on Medium's read time forumula.",
    'long_description': "# 📖 Readtime-CLI\n\nCLI to calculates the time some text takes the average human to read, based on Medium's [read time forumula](https://help.medium.com/hc/en-us/articles/214991667-Read-time).\n\n\n## 🧮 Algorithm\n\nMedium's Help Center says,\n\n> Read time is based on the average reading speed of an adult (roughly 265 WPM). We take the total word count of a post and translate it into minutes, with an adjustment made for images. For posts in Chinese, Japanese and Korean, it's a function of number of characters (500 characters/min) with an adjustment made for images.\n\n[Source](https://help.medium.com/hc/en-us/articles/214991667-Read-time)\n\nDouble checking with real articles, the English algorithm is:\n\n    seconds = num_words / 265 * 60 + img_weight * num_images\n\nWith `img_weight` starting at `12` and decreasing one second with each image encountered, with a minium `img_weight` of `3` seconds.\n\n\n## Requirements\n\nPython 3.9+\n\nReadtime-CLI stands on the shouders of giants:\n\n* [Typer](https://github.com/tiangolo/typer)\n* [Readtime](https://github.com/alanhamlett/readtime)\n\n\n## 🛠 Installation\n\n### Poetry\n\n    poetry add readtime_cli\n\n### Pip\n\n    virtualenv venv\n    . venv/bin/activate\n    pip install readtime_cli\n\n\n## 💻 Usage\n\n\n### Version\n\n```sh\nreadtime version\n```\n\n### Calculate Read time Markdown files\n\n```sh\nreadtime md FILE_PATH [OPTIONS]\n```\n\n### Calculate Read time HTML files\n\n```sh\nreadtime html FILE_PATH [OPTIONS]\n```\n\n### Calculate Read time Text files\n\n```sh\nreadtime text FILE_PATH [OPTIONS]\n```\n\n### Options for all commands\n\n    --wpm INTEGER  Word Per Minute  [default: 265]\n    --help         Show help and exit.\n",
    'author': 'Felipe Guedes',
    'author_email': 'contatofelipeguedes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/guedesfelipe/readtime_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
