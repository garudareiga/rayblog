Title: Fibonacci Sequence
Date: 2014-05-14 23:15
Author: Ray Chen
Category: Algorithm
Tags: algorithm

Problem: Implement a function which returns the n-th number in Fibonacci sequence with an input n. 

Fibonacci sequence is defined as:
$f_{n} = f_{n-1} + f_{n-2}$, with seed values $f_{0} = 0, f_{1} = 1$.

### Naive Recursive Solution

```java
int fib(int n) {
	if (n == 0 || n == 1)
		return n;
	else
		return fib(n - 1) + fib(n - 2)
}	
```
It is not difficult to notice that there are many duplicate nodes after we draw a recursion tree. The number of duplicated nodes increases dramatically when __n__ increases.

### Optimized Recursive Solution

Since $Fibonacci_{n}$ needs to add the previous two Fibonacci numbers, it makes more sense to define a Fibonnacci function that keeps track of the two previous values.

```java
int fib(int n) {
	return n == 0 ? 0 : fib_recursive(n, 0, 1);
}
int fib_recursive(int n, int p0, int p1) {
	return n == 1 : p1 : fib_recursive(n - 1, p1, p0 + p1);
}
```

### Iterative Solution

```java
int fib(int n) {
	if (n == 0 || n == 1)
		return n;
	int result, p0 = 0, p1 = 1;
	for (int i = 2; i <= n; i++) {
		result = p0 + p1;
		p0 = p1;
		p1 = result;
	}
	return result;
}
```
