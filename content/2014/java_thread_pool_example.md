Title: Java Thread Pool Example 
Date: 2014-03-20 22:06
Author: Ray Chen
Category: Java 
Tags: java, concurrency 

A thread pool from the executor implementation in _java.util.concurrent_ manages the pool 
of _worker threads_. Using worker threads minimizes the overhead due to thread creation.

The _java.util.concurrent.Executor_ interface accepts the collection of _Runnable_ objects and 
running worker threads execute _Runnable_ objects from the task queue. The queue holds extra
tasks whenever there are more active tasks than threads.

First, let's have a Runnable class.

WorkerThread.java
```java
public class WorkerThread implements Runnable {
	private static final int SECONDS = 2;
	private String msg;
	
	public WorkerThread(String msg) {
		this.msg = msg;
	}
	
	@Override
	public void run() {
		System.out.println(Thread.currentThread().getName() + " start.");
		System.out.println(this.msg);
		try {
			Thread.sleep(SECONDS*1000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println(Thread.currentThread().getName() + " end.");
	}
}
```

There are two common type of thread pools: the fixed thread pool _newFixedThreadPool_
and the expandable thread pool _newCachedTheadPool_. Let's use a fixed thread pool here

FixedThreadPool.java
```java
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;

public class FixedThreadPool {
	private final static int NUM_WORK_THREADS = 4; 
	
	public static void main(String[] args) {
		ExecutorService executor = Executors.newFixedThreadPool(2);
		for (int i = 1; i <= NUM_WORK_THREADS; i++) {
			Runnable r = new WorkerThread("Hello from worker thread " + i);
			executor.execute(r);
		}
		executor.shutdown();
		while (!executor.isTerminated()) {}
		System.out.println("Threads all done!");
	}
}
```

In above program, we create a fixed thread pool of 2 worker threads, and submit 3 tasks
to this pool. Here is the output of the above program:

```
pool-1-thread-1 start.
Hello from worker thread 1
pool-1-thread-2 start.
Hello from worker thread 2
pool-1-thread-1 end.
pool-1-thread-1 start.
Hello from worker thread 3
pool-1-thread-2 end.
pool-1-thread-2 start.
Hello from worker thread 4
pool-1-thread-1 end.
pool-1-thread-2 end.
Threads all done!
```

The output confirms that there are two threads in the pool named as "pool-1-thread-1" 
and "pool-1-thread-2". With the _ThreadFactory_, we can set more descriptive thread names.
Here is the implementation of _ThreadFactory_ and we use _CachedThreadPool_ instead.

WorkerThreadFactory.java
```java
import java.util.concurrent.*;

public class WorkerTreadFactory implements ThreadFactory {
	private int counter = 0;
	private String prefix = "";
	
	public WorkerTreadFactory(String prefix) {
		this.prefix = prefix;
	}
	
	@Override
	public Thread newThread(Runnable r) {
		return new Thread(r, prefix + " - " + counter++);
	}
}
```

CachedThreadPool.java
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class CachedThreadPool {
	private final static int NUM_WORK_THREADS = 4; 
	
	public static void main(String[] args) throws InterruptedException {
		ExecutorService executor = Executors.newCachedThreadPool(new WorkerTreadFactory("WorkerThread"));
		for (int i = 1; i <= NUM_WORK_THREADS; i++) {
			Runnable r = new WorkerThread("Hello from worker thread " + i);
			executor.submit(r);
		}
		executor.shutdown();
		while (!executor.isTerminated()) {}
		System.out.println("Threads all done!");
	}
}
```

The output of above program will be:
```
WorkerThread - 0 start.
Hello from worker thread 1
WorkerThread - 2 start.
Hello from worker thread 3
WorkerThread - 1 start.
Hello from worker thread 2
WorkerThread - 3 start.
Hello from worker thread 4
WorkerThread - 0 end.
WorkerThread - 2 end.
WorkerThread - 1 end.
WorkerThread - 3 end.
Threads all done!
```
