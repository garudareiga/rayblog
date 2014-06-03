Title: Java Reentrant Lock 
Date: 2014-06-02 20:10
Author: Ray Chen
Category: Java 
Tags: java, concurrency

### Intrinsic Lock

__Synchronized__ uses intrinsic locks. Every object in Java has an associated intrinsic lock. Whenever a thread tries to access a synchronized block or method, it acquires the intrinsic lock on that object.

The intrinsic locking mechanism have some limitations as follows:

- It is not possible to attempt to acquire a lock without being willing to wait for it forever. 
- It is not possible to interrupt a thread waiting to acquire a lock.

As an alternative, ReentrantLock provides more control on lock acquisition. ReentrantLock allows threads to re-request locks they already own. It provides timed or polled lock acquisition. It also has support for configurable fairness policy, allowing more flexible thread scheduling.

### Polled and Timed Lock Acquisition

Let's see some example code:
```java
public void transferMoney(Account from, Account to, float amount) {
	synchronized(from) {
		synchronized(to) {
			from.debit(amount);
			to.credit(amount);
		}
	}
}
```
In _transferMoney()_ method above, there is a possibility of __deadlock__ when two threads A and B are trying to transfer money at the same time. For example, when thread A has acquired a lock on _account_1_ object and is waiting to acquire a lock on the _account_2_ object, thread B has acquired a lock on the _account_2_ object and is waiting for a lock on _account_1_. This will lead to deadlock.
``` java
transferMoney(account_1, account_2, 10);
transferMoney(account_2, account_1, 10);
```

Using _tryLock_, a __timed and polled lock acquisition__ mechanism lets you regain control if you can not acquire all the required locks, release the ones you have acquired and retry. If we can not acquire both, we will release if one of these has been acquired, then retry. If the locks can not be acquired within the specified time, the transferMoney method will return a failure.
```java
public boolean transferMoney(Account from, Account to, float amount) {
	long startTime = System.nanoTime();
	while (true) {
		if (from.getReentrantLock().tryLock()) {
			try {
				if (to.getReentrantLock().tryLock()) {
					try {
						from.debit(amount);
						to.credit(amount);
					} finally {
						to.getReentrantLock().unlock();
					}
				}
			} finally {
				from.getReentrantLock().unlock();
			}
		}
		if (System.nanoTime() - startTime > 5000)
			return false;

		Thread.sleep(100);
	}
}
```
