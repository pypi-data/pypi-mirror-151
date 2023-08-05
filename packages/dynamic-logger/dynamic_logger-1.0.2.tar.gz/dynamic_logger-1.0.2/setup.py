# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_logger', 'dynamic_logger.examples']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dynamic-logger',
    'version': '1.0.2',
    'description': 'Dynamic Logger Class for logging',
    'long_description': '# DynamicLogger\n\nDynamicLogger is an extension of logging.Logger to provide additional functionality to log "extra" values quickly and dynamically. </br>\n\n# Installation\n\n## One Liner\n```bash\npython -m pip install dynamic_logger\n```\n\n## Or if you prefer Manual Installation\n``` bash\ngit clone https://github.com/ajatkj/dynamic_logger.git\ncd dynamic_logger\npip install .\n```\n\n# Usage\n```python\nimport dynamic_logger\nimport logging\nlogging.setLoggerClass(dynamic_logger.Logger)\n\n# Set-up log formatter with user-definied attributes\nfmt = \'[%(asctime)s] <%(app)s> [%(levelname)s] <%(id)s> <%(customer_id)s> --- %(message)s\' # Note: format attributes in <> are user-definited\n\n# Load config\nlogging.basicConfig(format=fmt, datefmt=\'%d-%b-%y %H:%M:%S\', level=\'INFO\')\n\napplogger = logging.getLogger(__name__)\n\n@applogger.log_extras(\'id\',int=0,customer_id=\'obj.customer_id\') # Log value of \'id\' and \'obj.customer_id\'\ndef example_1(id=0,id2=0,obj=None):\n    applogger.info(\'This example shows how to log values from function arguments\')\n\nif __name__ = "__main__":\n    example_1(id=123456,obj={"customer_id":777})\n```\n\nAbove will produce log output as below for all logging calls from the function:\n\n```\n[2022-04-19 12:53:51,658] [INFO] <123456> <customer_id:777> --- This example shows how to log values from function arguments\n```\n\n`dynamic_logger` exposes 2 main API\'s\n\n1. log_extras decorator  \n   `log_extras()` will log values dynamically from the decorated function\n2. set_extras function  \n    `set_extras()` will log static values for all subsequent `logger` calls till you call the `clear()` function.\n\nSee more examples in `example.py`\n\n## Some Notes\n1. To use with FastAPI, make sure `log_extras()` decorator is added after the path decorator of FastAPI.\n\n# Contribution\nAlways open to PRs :)\n\n<p align="center"><a href="https://github.com/ajatkj/dynamic_logger/blob/main/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=License&message=MIT&logoColor=eceff4&logo=github&colorA=4c566a&colorB=88c0d0"/></a></p>',
    'author': 'ajatkj',
    'author_email': 'ajatkj@yahoo.co.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajatkj/dynamic_logger',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
