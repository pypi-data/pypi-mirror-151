# Clearcut: A straightforward and lightweight logging wrapper library

[![Build Status](https://cloud.drone.io/api/badges/tangibleintelligence/clearcut/status.svg)](https://cloud.drone.io/tangibleintelligence/clearcut)

This provides some helpful wrapper and util functions for logging, and formats log messages in a more human-readable way by default.

## Use

At the top of the file:

```python
from clearcut import get_logger

...

logger = get_logger(__name__)
```

Logging can be performed ad-hoc:

```python
logger.info("info log")
logger.warning("warn log", exc_info=e)
```

"log blocks" can also be created which automatically log entrance/exits as well as performance information

```python
from clearcut import log_block, get_logger

...

logger = get_logger(__name__)

...

with log_block("block name", logger):
    ...
```

## TODO
- Would like to use contextvars to create a contextmanager where additional "metadata" can be specified (and unspecified) which would be
included with logging automatically. (may not be import with OTLP tracing.)
- json logging