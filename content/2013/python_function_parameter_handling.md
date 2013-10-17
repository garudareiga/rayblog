Title: Python Function Parameter Using * and ** Operators
Date: 2013-09-08 13:00
Category: Python
Tags: python
Author: Ray Chen

Python lets us define a function that can take a variable number of arguments. 

Using * operator for positional arguments
-----------------------------------------
A parameter name that begins with * *gathers* arguments into a tuple. You can
only provide one such variable after the ordinary positional parameters in
the function definition. For example, *printall* takes any number of arguments
and print them:

    >>> def print_all(*args)
        print args
    >>> print_all(1, 2.0, 'foo')
    (1, 2.0, 'foo')

The complement of gather is *scatter*. If you have a sequence of values and you 
want to pass it to a function as multiple arguments, you can use the * operator.
For example, *divmond* takes exactly two argument:

    >>> t = (7, 3)
    >>> divmond(*t)
    (2, 1)

The *chain* function from the *itertools* module provides an example for gather
and scatter:

    >>> import itertools
    >>> myList = [[1, 2], [3, 4]]
    >>> list(iterools.chain(*myList))
    [1, 2, 3, 4]

Using ** operator for keyword arguments
---------------------------------------
A parameter name that begins with ** gathers arguments into a dictionary: 

    >>> def print_kwargs(**kwargs):
            print kwargs
    >>> print_kwargs(a=1, b=2, c=3)
    {'a': 1, 'c': 3, 'b': 2}

You can also use ** operator as a scatter when calling a function:

    >>> def print_args(arg1, arg2)
            print "arg1:", arg1, "arg2:", arg2
    >>> kwargs = {'arg1': 2, 'arg2': 1}
    >>> print_args(kwargs)
    arg1: 2 arg2: 1
