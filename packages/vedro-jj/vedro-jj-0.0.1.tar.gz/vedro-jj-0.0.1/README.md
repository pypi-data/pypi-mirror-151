# vedro-jj

# Vedro Interactive

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/vedro-jj/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/vedro-jj)
[![PyPI](https://img.shields.io/pypi/v/vedro-jj.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-jj/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/vedro-jj?style=flat-square)](https://pypi.python.org/pypi/vedro-jj/)
[![Python Version](https://img.shields.io/pypi/pyversions/vedro-jj.svg?style=flat-square)](https://pypi.python.org/pypi/vedro-jj/)

## Installation

### 1. Install package

```shell
$ pip3 install vedro-jj
```

### 2. Enable plugin

```python
# ./vedro.cfg.py
import vedro
import vedro_jj

class Config(vedro.Config):

    class Plugins(vedro.Config.Plugins):

        class RemoteMock(vedro_jj.RemoteMock):
            enabled = True
```

## Usage

```python
# ./scenarios/get_users.py
import jj
import vedro
from httpx import AsyncClient
from jj.mock import mocked

class Scenario(vedro.Scenario):
    subject = "get users"

    def given(self):
        self.mock_matcher = jj.match("GET", "/users")
        self.mock_response = jj.Response(json=[])

    async def when(self):
        async with mocked(self.mock_matcher, self.mock_response):
            async with AsyncClient() as client:
                self.response = await client.get("http://localhost:8080/users")

    def then(self):
        assert self.response.status_code == 200
        assert self.response.json() == []
```

```shell
$ vedro run -vv
```
