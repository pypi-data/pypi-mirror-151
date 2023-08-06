# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['awesome_exception', 'awesome_exception.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['pydantic[email]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'awesome-exception',
    'version': '1.0.0',
    'description': 'common http exception that support custom status code and message',
    'long_description': '[![Stable Version](https://badge.fury.io/py/awesome-exception.svg)](https://pypi.org/project/awesome-exception/)\n[![tests](https://github.com/MoBagel/awesome-exception/workflows/develop/badge.svg)](https://github.com/MoBagel/awesome-exception)\n[![Coverage Status](https://coveralls.io/repos/github/MoBagel/awesome-exception/badge.svg?branch=develop)](https://coveralls.io/github/MoBagel/awesome-exception)\n\n# Awesome Exception\n\nA library designed to handle http exception elegantly with customization support like i18n support.\n\n## Feature\n\n- [x] common http exception class that support custom message and status code\n\n## Usage\n\n### Installation\n\n1. `pip install awesome-exception`\n\n### Exceptions\n\nUsing fast API as example, we may simply throw exception with a proper status code, and an optional error code. We may\nalso supply arbitrary key value in args dict, to help frontend render better error message.\n\n```python\nfrom awesome_exception.exceptions import NotFound\nfrom fastapi import APIRouter\n\nrouter = APIRouter()\n\n\n@router.get(\'/transactions\')\ndef get(id: str):\n    try:\n        obj = find_by_id(id)\n    except Exception as e:\n        raise NotFound(message=\'transaction not found\' % id, error_code=\'A0001\', args={id: id})\n    ...\n```\n\nAnd we may implement a common error handler to convert all these errors to proper response schema\n\n```python\nfrom awesome_exception.exceptions import HTTPException\nfrom fastapi.requests import Request\nfrom fastapi.responses import JSONResponse\n\n\n@app.exception_handler(HTTPException)\nasync def http_exception_handler(request: Request, exc: HTTPException):\n    return JSONResponse(\n        status_code=exc.status_code,\n        content={\n            \'detail\': exc.detail,\n            \'error_code\': exc.error_code,\n        }\n    )\n```\n\nThis would result in a response with status code 404, and body\n\n```json\n{\n  "status_code": 404,\n  "detail": {\n    "message": "transaction not found",\n    "id": "some_id"\n  },\n  "error_code": "A0001"\n}\n```\n\nWith this response, frontend can decide to simply render detail, or map it to detailed message. If error_code "A0001"\ncorrespond to the following i18 n entry\n\n```json\n"error.A0001": {"en-US": "transaction can not be found with supplied {id}: {message}"}\n```\n\nwe may format message accordingly with\n\n```typescript\nerrorMessage = formatMessage({ id: `error.${error.data.error_code}` }, error.data.detail);\n```\n\nNote that error code is not supplied, is default to status code. So it is always safe to simply use error_code in\nfrontend to decide what to render.\n\n## Development\n\n### Installing Poetry\n\n1. create your own environment for poetry, and simply run: `pip install poetry`\n2. alternatively, you can refer to [poetry\'s official page](https://github.com/python-poetry/poetry)\n3. to be able to use `poe` directly, `pip install poethepoet`\n\n### Contributing\n\n1. project setup: `poetry install`\n2. create your own branch to start developing new feature.\n3. before creating pr, make sure you pass `poe lint` and `./run_test.sh`.\n    - what happened inside `./run_test.sh` is that a minio server is setup for you temporarily, and teardown and unit\n      test is finished.\n    - notice that `poe test` would also work if you already have a minio up and running. You need the following env\n      variable: `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_ADDRESS` upon running `poe test`.\n4. for a list of available poe command, `poe`\n5. after you submit a pr, you should check if pipeline is successful.\n\n### Releasing\n\n1. `poetry version [new_version]`\n2. `git commit -m"Bump version"`\n3. `git push origin develop`\n4. [create new release](https://github.com/MoBagel/awesome-exception/releases/new) on github.\n5. Create release off develop branch, auto generate notes, and review release note. \n6. Publish release\n\n',
    'author': 'Schwannden Kuo',
    'author_email': 'schwannden@mobagel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MoBagel/awesome-exception',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
