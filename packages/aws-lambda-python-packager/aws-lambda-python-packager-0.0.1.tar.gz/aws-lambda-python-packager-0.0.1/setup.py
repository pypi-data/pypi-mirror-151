# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_lambda_python_packager']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['lambda-packager = aws_lambda_python_packager.cli:main']}

setup_kwargs = {
    'name': 'aws-lambda-python-packager',
    'version': '0.0.1',
    'description': 'Description',
    'long_description': '# AWS Lambda Python Packager\n',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mumblepins/aws-lambda-python-packager/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
