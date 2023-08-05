# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apiclient_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['api-client>1.2.1', 'pydantic>=1.7,<2.0']

setup_kwargs = {
    'name': 'api-client-pydantic',
    'version': '2.2.0',
    'description': 'API Client extension for validate and transform requests / responses using pydantic.',
    'long_description': '![GitHub issues](https://img.shields.io/github/issues/mom1/api-client-pydantic.svg)\n![GitHub stars](https://img.shields.io/github/stars/mom1/api-client-pydantic.svg)\n![GitHub Release Date](https://img.shields.io/github/release-date/mom1/api-client-pydantic.svg)\n![GitHub commits since latest release](https://img.shields.io/github/commits-since/mom1/api-client-pydantic/latest.svg)\n![GitHub last commit](https://img.shields.io/github/last-commit/mom1/api-client-pydantic.svg)\n[![GitHub license](https://img.shields.io/github/license/mom1/api-client-pydantic)](https://github.com/mom1/api-client-pydantic/blob/master/LICENSE)\n\n[![PyPI](https://img.shields.io/pypi/v/api-client-pydantic.svg)](https://pypi.python.org/pypi/api-client-pydantic)\n[![PyPI](https://img.shields.io/pypi/pyversions/api-client-pydantic.svg)]()\n![PyPI - Downloads](https://img.shields.io/pypi/dm/api-client-pydantic.svg?label=pip%20installs&logo=python)\n\n<a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg" alt="Gitmoji"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="black"></a>\n\n# Python API Client Pydantic Extension\n\n## Installation\n\n```bash\npip install api-client-pydantic\n```\n\n## Usage\n\nThe following decorators have been provided to validate request data and converting json straight to pydantic class.\n\n```python\nfrom apiclient_pydantic import params_serializer, response_serializer, serialize, serialize_all_methods\n\n# serialize incoming kwargs\n@params_serializer(by_alias: bool = True, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = True)\n\n# serialize response in pydantic class\n@response_serializer(response: Optional[Type[BaseModel]] = None)\n\n# serialize request and response data\n@serialize(response: Optional[Type[BaseModel]] = None, by_alias: bool = True, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = True)\n\n# wraps all local methods of a class with a specified decorator. default \'serialize\'\n@serialize_all_methods(decorator=serialize)\n```\n\nUsage:\n1. Define the schema for your api in pydantic classes.\n    ```python\n    from pydantic import BaseModel, Field\n\n\n    class Account(BaseModel):\n        account_number: int = Field(alias=\'accountNumber\')\n        sort_code: int = Field(alias=\'sortCode\')\n        date_opened: datetime = Field(alias=\'dateOpened\')\n    ```\n\n2. Add the `@response_serializer` decorator to the api client method to transform the response\ndirectly into your defined schema.\n   ```python\n    @response_serializer(List[Account])\n    def get_accounts():\n        ...\n    # or\n    @response_serializer()\n    def get_accounts() -> List[Account]:\n        ...\n    ```\n3. Add the `@params_serializer` decorator to the api client method to translate the incoming kwargs\ninto the required dict for the endpoint:\n   ```python\n    @params_serializer(AccountHolder)\n    def create_account(data: dict):\n        ...\n    # or\n    @params_serializer()\n    def create_account(data: AccountHolder):\n        # data will be exactly a dict\n        ...\n    create_account(last_name=\'Smith\', first_name=\'John\')\n    # data will be a dict {"last_name": "Smith", "first_name": "John"}\n    ```\n4. `@serialize` - It is a combination of the two decorators `@response_serializer` and`@params_serializer`.\n5. For more convenient use, you can wrap all APIClient methods with `@serialize_all_methods`.\n   ```python\n    from apiclient import APIClient\n    from apiclient_pydantic import serialize_all_methods\n    from typing import List\n\n    from .models import Account, AccountHolder\n\n\n    @serialize_all_methods()\n    class MyApiClient(APIClient):\n        def decorated_func(self, data: Account) -> Account:\n            ...\n\n        def decorated_func_holder(self, data: AccountHolder) -> List[Account]:\n            ...\n    ```\n\n## Related projects\n\n### apiclient-pydantic-generator\n\nThis code generator creates a [ApiClient](https://github.com/MikeWooster/api-client) app from an openapi file.\n\n[apiclient-pydantic-generator](https://github.com/mom1/apiclient-pydantic-generator)\n\n## Mentions\n\nMany thanks to [JetBrains](https://www.jetbrains.com/?from=api-client-pydantic) for supplying me with a license to use their product in the development\nof this tool.\n\n![JetBrains Logo (Main) logo](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg)\n',
    'author': 'MaxST',
    'author_email': 'mstolpasov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mom1/api-client-pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
