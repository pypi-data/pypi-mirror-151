# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['longpython']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['longpython = longpython.main:main']}

setup_kwargs = {
    'name': 'longpython',
    'version': '0.0.1',
    'description': 'CLI tool to print long python',
    'long_description': '# longpython\n\n*looooooooooooooooooooong python!*\n\n## Usage\n\n```shellsession\n$ longpython\n  _\n(" ヽ\n   \\ \\\n   / /\n   \\ \\ _ ,\n    \\___/\n\n$ longpython -h\nusage: longpython [-h] [-l INT]\n\nCLI tool to print long python\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -l INT, --length INT  length of python (default: 1)\n```\n\n## Installation\n\n```sh\npip install git+https://github.com/4513ECHO/longpython\n```\n\n## Derived Projects\n\n- [syumai/longify](https://github.com/syumai/longify): A command to output longified any ascii art\n- [arrow2nd/longdeno](https://github.com/arrow2nd/longdeno): Looooooooooooooooooooooooooooooooooooooooooooooong [Deno](https://deno.land)\n- [ikanago/longferris](https://github.com/ikanago/longferris): Long [Ferris](https://github.com/ciusji/ferris) written in Rust\n- [sheepla/longgopher](https://github.com/sheepla/longgopher): ʕ◉ϖ◉ʔ loooooooooooooooooooooong gopher\n\n## License\n\nMIT\n',
    'author': 'Hibiki(4513ECHO)',
    'author_email': '4513echo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4513ECHO/longpython',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
