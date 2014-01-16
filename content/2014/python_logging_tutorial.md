Title: Python Logging Tutorial
Date: 2014-01-14 22:38
Author: Ray Chen
Category: Python
Tags: python, logging

The Python [logging documentation](http://docs.python.org/2/library/logging.html) is initially confusing to me, therefore I decide to write this tutorial as a quick reference.

## Root Logger 

We can use the default (*root*) logger directly on module level. You can view and download the file 
[logger0.py](https://gist.github.com/garudareiga/8451107) from my Gist.

```python
>>> import logger0
>>> logger0.foo()
WARNING:root:Dump warn message
ERROR:root:Dump warn message
CRITICAL:root:Dump warn message
```

As we can see the message emitted by the root logger, the _debug_ and _info_ messages are ignored. 
Besides, it prefixes all outputs by something like WARNING:root. It is because the root logger's
severity level is set to *WARN* by default, and it has its own formatter. Let's quickly confirm
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

## Customized Logger

Let me introduce four main objects in the Python standard logging module - **Logger**, **Handler**,
**Formatter** and **LogRecord**, to understand how the logging process works.

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

Now, let's use our own logger instead of root. You can view and download the file 
[logger1.py](https://gist.github.com/garudareiga/8446080) from my Gist.

```python
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

### Log Hierarchy

Loggers are arranged in a hierarchy based on their names as python module names. So we choose 
to use the module name as the logger name, with '.' dots separating hierarchy levels. 
The root logger is at the top of this hierarchy. The name of the root logger is an empty string.
The hierarchy is created and managed automatically by the logging system. All message send to a
logger is automatically sent to its parent. We can turn off this upward propagation by setting the
attribute **propagate** to false. Configuring the parent logger will cascade down to the other loggers.  

```python
appLogger = logging.getLogger("myapp")
appLogger.setLevel(logging.INFO)
```

All myapp.* loggers will have the level INFO as their default.

### Exception with Traceback

In reality, it is helpful to record whith traceback when something goes wrong.
By calling logger methods with *exc_info=True* parameter, traceback is dumped
to the logger.

```python
for record in database:
	try:
		process(record)
		if changed:
			update(record)
	execpt (KeyboardInterrupt, SystemExit):
		raise
	except Exception as e:
		logger.error('Failed to process record', exc_info=True)
```

### Use RotatingFileHandler

When we use FileHandler for writing the log, the size of log file grows quickly
with time. We'd better use RotatingFileHandler instead of FileHandler in production 
environment.

```python
handler_rotate_file = logging.RoFileHandler(filename=__name__ + '.log', maxBytes=10485760, backupCount=20)
```

## Use JSON Logging Configuration

It is not flexible to configure out logging system in Python code. Instead, we can load the logging configuration from a JSON file. You can download the following three files [logging.json](https://gist.github.com/garudareiga/8445508), [logger2.py](https://gist.github.com/garudareiga/8445881), [logger3.py](https://gist.github.com/garudareiga/8445890) from my Gist.

```python
>>> import logging.config, json, logger2, logger3
>>> with open('logging.son', 'r') as f:
		config = json.loads(f.read())
>>> logging.config.dictConfig(config)
>>> logger2.foo()
logger2 - DEBUG - Dump debug message
logger2 - INFO - Dump info message
logger2 - WARNING - Dump warn message
logger2 - ERROR - Dump error message
logger2 - CRITICAL - Dump critical message
>>> logger3.foo()
logger3 - WARNING - Dump warn message
```

Pay attention to the argument name "disable_existing_loggers". When we create the logger at module level, and them import the module before we load the logging configuration, the **logging.dictConfig** disable existing loggers by default, unless we set "disable_existing_loggers" to false. For example, if we set "disable_existing_loggers" to true, logger3.foo() will not print out anything.

I hope this blog can help clear up Python's logging module for you.

## Extra Links

Some credits go to the following links which help me understand the Python logging module.

- [Good logging practice in Python](http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python)
- [How Python logging module works](http://www.shutupandship.com/2012/02/how-python-logging-module-works.html)
- [Learning Python logging](http://eric.themoritzfamily.com/learning-python-logging.html)
- [A Logging System for Python](http://www.red-dove.com/python_logging.html)
