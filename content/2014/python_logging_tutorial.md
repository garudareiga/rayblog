Title: Python Logging Tutorial
Date: 2014-01-14 22:38
Author: Ray Chen
Category: Python
Tags: python, logging

The Python [logging documentation](http://docs.python.org/2/library/logging.html) is initially confusing to me, therefore I decide to write this tutorial as a quick reference.

# Root Logger 

We can use the default ('the _root_') directly on module level.

```Python
""" logger0.py """

import logging

def foo():
    logging.debug('Dump debug message')
    logging.info('Dump info message')
    logging.warn('Dump warn message')
    logging.error('Dump error message')
    logging.critical('Dump critical message')

>>> import logger0
>>> logger0.foo()
WARNING:root:Dump warn message
ERROR:root:Dump warn message
CRITICAL:root:Dump warn message
```

As you can see the message emitted by 'root', the _debug_ and _info_ messages are ignored. 
Besides, it prefixes all output by something like WARNING:root. It is because the root logger's
debug level is set to *WARN* by default, and it has its own formatter. Let's quickly confirm
that and then change the level from *WARN* to *DEBUG*.

```Python
>>> import logging
>>> logging.root.level == logging.WARN
True
>>> logging.root.handlers[0].formatter._fmt
'%(levelname)s:%(name)s:%(message)s'
>>> logging.root.setLevel(logging.DEBUG)
>>> logger0.foo()
DEBUG:root:Dump debug message
INFO:root:Dump info message
WARNING:root:Dump warn message
ERROR:root:Dump error message
CRITICAL:root:Dump critical message
```

# Customized Logger

Let me introduce four main objects in the Python standard logging module - *Logger*, *Handler*,
*Formatter* and *LogRecord*, to understand how the logging process works.
- Logger, Handler and LogRecord have a _severity_ level.
- We can messages to a Logger using the Logger's log method. The log method needs two parameters -
  a msg (message) and a severity level.
- 
