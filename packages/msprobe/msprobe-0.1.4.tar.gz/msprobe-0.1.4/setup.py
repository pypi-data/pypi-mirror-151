# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msprobe',
 'msprobe.lib',
 'msprobe.lib.adfs',
 'msprobe.lib.exch',
 'msprobe.lib.rdp',
 'msprobe.lib.skype']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click>=8.1.2,<9.0.0',
 'lxml>=4.8.0,<5.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.2.0,<13.0.0']

entry_points = \
{'console_scripts': ['msprobe = msprobe.msprobe:cli']}

setup_kwargs = {
    'name': 'msprobe',
    'version': '0.1.4',
    'description': 'Finding all things on-prem MS!',
    'long_description': '# msprobe\n\n+ [About](#about)\n+ [Installing](#installing)\n+ [Usage](#usage)\n+ [Examples](#examples)\n+ [Coming Soon](#coming)\n+ [Acknowledgements](#acknowledgements)\n\n\n\n## About <a name = "about"></a>\n\nFinding all things on-prem Microsoft for password spraying and enumeration. \n\nThe tool will used a list of common subdomains associated with your target apex domain to attempt to discover valid instances of on-prem Microsoft solutions. Screenshots of the tool in action are below:\n\n![FLqt1cWXEAklMP1](https://user-images.githubusercontent.com/8538866/163191875-61040ed3-b318-4ad4-97c1-c06fb3f7eeba.jpeg)\n\n### Installing <a name = "installing"></a>\n\nInstall the project using [pipx](https://pypa.github.io/pipx/installation/)\n\n```\npipx install git+https://github.com/puzzlepeaches/msprobe.git\n```\n\n\n## Usage <a name = "usage"></a>\n\nThe tool has four different modules that assist with the discovery of on-prem Microsoft products:\n\n* Exchange\n* RD Web\n* ADFS\n* Skype for Business\n\nThe help menu and supported modules are shown below:\n\n```\nUsage: msprobe [OPTIONS] COMMAND [ARGS]...\n\n  Find Microsoft Exchange, RD Web, ADFS, and Skype instances\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  adfs   Find Microsoft ADFS servers\n  exch   Find Microsoft Exchange servers\n  full   Find all Microsoft supported by msprobe\n  rdp    Find Microsoft RD Web servers\n  skype  Find Microsoft Skype servers\n```\n\n\n\n\n## Examples <a name = "examples"></a>\n\nFind ADFS servers associated with apex domain:\n\n```\nmsprobe adfs acme.com\n```\n\nFind RD Web servers associated with apex domain with verbose output:\n\n```\nmsprobe rdp acme.com -v\n```\n\nFind all Microsoft products hostsed on-prem for a domain:\n\n```\nmsprobe full acme.com\n```\n\n## Coming Soon <a name = "coming"></a>\n- Full wiki for each module\n- Fixes for lxml based parsing in RD Web module\n\n\n## Acknowledgements <a name = "acknowledgements"></a>\n- [@p0dalirius](https://twitter.com/intent/follow?screen_name=podalirius_) for [RDWArecon](https://github.com/p0dalirius/RDWArecon) \n- [@b17zr](https://twitter.com/b17zr) for the `ntlm_challenger.py` script\n- [@ReverendThing](https://github.com/ReverendThing) for his project [Carnivore](https://github.com/ReverendThing/Carnivore) and it\'s included subdomains\n- [@busterbcook](https://twitter.com/busterbcook) and their tool [msmailprobe](https://github.com/busterb/msmailprobe) heavily influenced the creation of this project \n',
    'author': 'Nicholas A',
    'author_email': 'nicholasanastasirepair@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/puzzlpeaches/msprobe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
