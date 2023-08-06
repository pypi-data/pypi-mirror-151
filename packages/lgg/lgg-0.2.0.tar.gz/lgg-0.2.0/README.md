# python-logger
A simple yet fancy logger for Python scripts

## Install
- Using pip:
```shell
pip install lgg
```

- Using Poetry:
```shell
poetry add lgg
```

## Usage
```python
# This way
from lgg import logger
# Or
from lgg import get_logger
logger = get_logger()
# End Or

logger.info('This is an info message')

logger.debug('Debugging message')

logger.error('error message')

logger.warning('File not found! An empty one is created')
```
![Result](.resources/nameless.png)

```python
from lgg import get_logger
logger = get_logger('python-logger')

logger.info('This is an info message')

logger.debug('Debugging message')

logger.error('error message')

logger.warning('File not found! An empty one is created')
```
![Result](.resources/python-logger.png)

**Notice the change after each log's datetime, the former shows the filename and line of code,
the latter displays the logger name instead**
