Title: A Single Server Key-Value Store 
Date: 2014-03-31 22:11
Author: Ray Chen
Category: System
Tags: key-value store, concurrency 

On the basis of Bekerley CS163 project 3, I will implement a single-node key-value storage system using Java.

## Summary

Multiple clients will be communicating with a single-node key-value server by sending and receiving
formatted messages through sockets. The sever uses a thread pool to support concurrent operations
accross multiple sets and a set-associative cache, which is backed by a disk storage.

The figure below shows a single-node key-value server with three clients making simultaneous requests:
![Alt text](http://www.raydevblog.us/images/kvstore.jpg)

## Requirements

* The key-value server will support 3 interfaces:
    - _Value GET (Key k)_: Retrieves the key-value pair corresponding to the provided key.
    - _PUT (Key k, Value v)_: Inserts the key-value pair into the store.
    - _DEL (Key k)_: Removes the key-value pair corresponding to the provided key from the store.

* The key-value server has a set-associative cache with the second-change eviction policy within each set.
  Each set in the cache will have a fixed number of entries, and evict entries using the second-chance algorithm.
  The cache follows a write-through caching policy. If a key exists in the cache for a _GET_ request, do not access
  the store.

* All requests (get/put/del) are atomic in that they must modify the state of both the cache and the store together.  
  Requests must be parallel across different sets and serial with the same set. The threadpool in the server shall
  maintain a queue of tasks, assign free threads to tasks and execute them asynchronously.

* The server will create a serversocket that listens on a port for connections, and service requests from the client.
  A socket shall be passed to the client handler for each request that comes in.

## Source Code

The latest source code of my implementation is available in my [github repository](https://github.com/garudareiga/computer_system_design/tree/master/kvstore/src/edu/berkeley/cs162)
