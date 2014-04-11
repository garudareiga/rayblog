Title: Distributed Key-Value Store 
Date: 2014-04-10 22:07
Author: Ray Chen
Category: System Programming
Tags: distributed, two-phase commit, logging and recovery, consistent hashing 

Special thanks go to Berkeley CS162 course providing a nice document and starter code for 
a distributed key-value store system design.

## Overview 

This distributed key-value storage system has multiple clients communicating 
with a single master server in a given messaging format. The master server contains a set-associative 
cache, and it uses the cache to serve GET requests without going to the key-value slave servers it
coordinates. The slave servers are contacted for a GET request only upon a cache miss on the master. 
The master will forward PUT and DEL client requests to multiple slave servers and follow the two-phase 
commit protocol for atomic PUT and DEL operations across multiple slave servers.

The figure below shows an example distributed key-value storage system.
Three clients send a master server simultaneous requests, and the master server coordinates with three
slave servers.
![Alt text](http://www.raydevblog.us/images/distributed_kvstore_master.jpg)

## Registration

## Consistent Hashing

## Two-phase Commit

## Failures, Timeouts, and Recovery

## Source Code

The latest source code of my implementation is available in my [github repository](https://github.com/garudareiga/computer_system_design/tree/master/distributed_kvstore/src/edu/berkeley/cs162)
