[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Description

Python client library for interacting with TestLodge.

# Installation

`pip install testlodge`

# Usage

```python
import os

from testlodge import Client


tl = Client(
    email='my.email@email.com',
    api_key=os.environ['TESTLODGE_API_KEY'],
    account_id=os.environ['TESTLODGE_ACCOUNT_ID'],
)
```

## Users

```python
from testlodge.typing import UserJSON
from testlodge.typing import UserListJSON


user_json: UserJSON = dict(
    id=123456,
    firstname='First',
    lastname='Last',
    email='user@email.com',
    created_at="2022-01-01T20:30:40.123456Z",
    updated_at="2022-05-16T01:08:41.493190Z",
)

# Get a list of users (Default: page 1)
user_list_json: UserListJSON = tl.get_user_list_json()
```
