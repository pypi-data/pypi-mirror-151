# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydamain',
 'pydamain.adapter',
 'pydamain.adapter.in_',
 'pydamain.adapter.out_',
 'pydamain.adapter.out_.repository',
 'pydamain.adapter.out_.unit_of_work',
 'pydamain.domain',
 'pydamain.domain.messages',
 'pydamain.domain.models',
 'pydamain.domain.service',
 'pydamain.port',
 'pydamain.port.in_',
 'pydamain.port.out_']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.2.0,<5.0.0']

extras_require = \
{'aiosmtplib': ['aiosmtplib>=1.1.6,<2.0.0'],
 'sqlalchemy': ['SQLAlchemy>=1.4.36,<2.0.0']}

setup_kwargs = {
    'name': 'pydamain',
    'version': '0.4.5',
    'description': '도메인 주도 설계 라이브러리.',
    'long_description': '# Pydamain\n\n작성중...',
    'author': 'Jongbeom-Kwon',
    'author_email': 'bolk9652@naver.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/by-Exist/pydamain',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
