[![Stable Version](https://badge.fury.io/py/awesome-exception.svg)](https://pypi.org/project/awesome-exception/)
[![tests](https://github.com/MoBagel/awesome-exception/workflows/develop/badge.svg)](https://github.com/MoBagel/awesome-exception)
[![Coverage Status](https://coveralls.io/repos/github/MoBagel/awesome-exception/badge.svg?branch=develop)](https://coveralls.io/github/MoBagel/awesome-exception)

# Awesome Exception

A library designed to handle http exception elegantly with customization support like i18n support.

## Feature

- [x] common http exception class that support custom message and status code

## Usage

### Installation

1. `pip install awesome-exception`

### Exceptions

Using fast API as example, we may simply throw exception with a proper status code, and an optional error code. We may
also supply arbitrary key value in args dict, to help frontend render better error message.

```python
from awesome_exception.exceptions import NotFound
from fastapi import APIRouter

router = APIRouter()


@router.get('/transactions')
def get(id: str):
    try:
        obj = find_by_id(id)
    except Exception as e:
        raise NotFound(message='transaction not found' % id, error_code='A0001', args={id: id})
    ...
```

And we may implement a common error handler to convert all these errors to proper response schema

```python
from awesome_exception.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'detail': exc.detail,
            'error_code': exc.error_code,
        }
    )
```

This would result in a response with status code 404, and body

```json
{
  "status_code": 404,
  "detail": {
    "message": "transaction not found",
    "id": "some_id"
  },
  "error_code": "A0001"
}
```

With this response, frontend can decide to simply render detail, or map it to detailed message. If error_code "A0001"
correspond to the following i18 n entry

```json
"error.A0001": {"en-US": "transaction can not be found with supplied {id}: {message}"}
```

we may format message accordingly with

```typescript
errorMessage = formatMessage({ id: `error.${error.data.error_code}` }, error.data.detail);
```

Note that error code is not supplied, is default to status code. So it is always safe to simply use error_code in
frontend to decide what to render.

## Development

### Installing Poetry

1. create your own environment for poetry, and simply run: `pip install poetry`
2. alternatively, you can refer to [poetry's official page](https://github.com/python-poetry/poetry)
3. to be able to use `poe` directly, `pip install poethepoet`

### Contributing

1. project setup: `poetry install`
2. create your own branch to start developing new feature.
3. before creating pr, make sure you pass `poe lint` and `./run_test.sh`.
    - what happened inside `./run_test.sh` is that a minio server is setup for you temporarily, and teardown and unit
      test is finished.
    - notice that `poe test` would also work if you already have a minio up and running. You need the following env
      variable: `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY`, `MINIO_ADDRESS` upon running `poe test`.
4. for a list of available poe command, `poe`
5. after you submit a pr, you should check if pipeline is successful.

### Releasing

1. `poetry version [new_version]`
2. `git commit -m"Bump version"`
3. `git push origin develop`
4. [create new release](https://github.com/MoBagel/awesome-exception/releases/new) on github.
5. Create release off develop branch, auto generate notes, and review release note. 
6. Publish release

