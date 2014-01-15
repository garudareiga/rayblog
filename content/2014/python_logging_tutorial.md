Title: Python Logging Tutorial
Date: 2014-01-14 22:38
Author: Ray Chen
Category: Python
Tags: python, logging

The Python [logging documentation](http://docs.python.org/2/library/logging.html) is initially confusing to me, therefore I decide to write this tutorial as a quick reference.

# Root Logger 

We can use the default (*root*) logger directly on module level.

```python
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

As we can see the message emitted by the root logger, the _debug_ and _info_ messages are ignored. 
Besides, it prefixes all output by something like WARNING:root. It is because the root logger's
debug level is set to *WARN* by default, and it has its own formatter. Let's quickly confirm
that and then change the level from *WARN* to *DEBUG*.

```python
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

- Logger, Handler and LogRecord have a *severity* level.
- We can messages to a Logger using the Logger's log method. The log method needs two parameters -
  a msg (message) and a severity level. Logger also has a few methods defined - *debug*, *info*, 
  *warn*, *error*, and 'critical'. Each of them has a pre-defined severity level.
- Logger looks at the message and ignores it if the message level is less severe than its own level.
  If not, it creates a LogRecord object from the message string and pass to its Handlers. A Logger 
  can have multiple custom Handlers such as StreamHandler, FileHandler, HTTPHandler etc.
- Handler is responsible for emitting messages to a stream, file, socket etc. THe Handerl also has
  its own level. After receiving the LogRecord, Handler ignores any LogRecord that has a less severe 
  level, otherwise it passes the LogRecord to its Formatter.
- Formatter formats the LogRecord message and then sends back to its Handler. A Handler is associated 
  with exactly one Formatter.
- Finally the Handler emits the formatted LogRecord message to our destination.

Now, let's use our own logger instead of root:

```python
""" logger1.py """

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler_stream = logging.StreamHandler()
handler_stream.setFormatter(formatter)
handler_stream.setLevel(logging.INFO)

handler_file = logging.FileHandler(__name__ + '.log')
handler_file.setFormatter(formatter)

logger.addHandler(handler_stream)
logger.addHandler(handler_file)

def foo():
    logger.debug('Dump debug message')
    logger.info('Dump info message')
    logger.warn('Dump warn message')
    logger.error('Dump error message')
    logger.critical('Dump critical message')

>>> import logger1
>>> logger1.foo()
[INFO] Dump info message
[WARNING] Dump warn message
[ERROR] Dump error message
[CRITICAL] Dump critical message
>>> print(open('logger1.log').read())
[DEBUG] Dump debug message
[INFO] Dump info message
[WARNING] Dump warn message
[ERROR] Dump error message
[CRITICAL] Dump critical message
```

We ask logging for a reference using the **getLogger** function. If the logger with that 
name does not exist it is created, else a reference is returned.
We add two handlers to the logger, one is a StreamHandler which by default prints to stderr,
while the other is a FileHandler which writes to a file **logger1.log**, and both of them 
use a custom formatter. In the example above, we log all messages to a file and log messages
with a severity level of INFO or higher to stderr.


