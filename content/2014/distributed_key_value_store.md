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
commit protocol (2PC) for atomic PUT and DEL operations across multiple slave servers.

The figure below shows an example distributed key-value storage system.
Three clients send a master server simultaneous requests, and the master server coordinates with three
slave servers.
![Alt text](http://www.raydevblog.us/images/distributed_kvstore_master.jpeg)

## Registration

Slave servers will send to the master a registration message with a 64-bit globally unique ID 
when they start.

+ The master listens for registration requests from slaves on port 9090.
+ When a slave starts it should listen in a random free port for 2PC requests, and register that port
number with the master so that the master can send requests to it.
+ Assuming no errors regarding registration, the master sends a response and the slave accepts the response.

## Consistent Hashing

+ Each key will be stored using 2PC in __two__ slave servers; the first of them will be selected using
consistent hashing, while the second will be placed in the successor of the first one.
+ The master will hash the key to 64-bit address space, because each slave server has a unique 64-bit ID.
+ Each slave will store the first copies of key with hash values greater than the ID of its immediate
predecessor up to its own ID, and also the keys whose first copies are stored in its predecessor. 

## Two-phase Commit

+ The master will select replica locations using consistent hashing.
+ A slave will send vote-abort to the master if the key does not exist for DEL, or invalid key/value;
+ When sending phase-1 requests, the master must contact slaves, even if the first slave sends an abort. The master
does this by sequentially making the requests or concurrently by forking off threads.
+ Only a single 2PC operation can be executed at a time. The master does not support concurrent update
operations across different keys, but GET operations of different keys must be concurrent unless restricted
by an ongoing update operation on the same set.

## Failures, Timeouts, and Recovery

For this particular design, assume that the master will never go down. However, slave servers must log
necessary information to survive from failures.

+ When the slave comes back with the same ID, it will be rebuilt using the log, and know if the last 
request it received was a phase-1 or phase-2 request.
+ If a slave crashes during phase-1, if master does not get a vote within a single timeout period, it should
assume the slave voted abort.
+ If a slave crashes during phase-2, the master must retry until it receives a response to its decision. 
Note that when the slave restarts, it may bind to a new port and re-register. The master must retry with
the latest port the slave has registered with. 

## Components

Master Server = TPCMaster + SocketServer attached (port 8080) with KVClientHandler
TPCMaster = Master Cache + SocketServer attached (port 9090) with TPCRegistrationHandler
Slave Server = TPCLog + KVServer + SocketServer (free port) attached with TPCMasterHandler

## Java Source Code Breakdown

* TPCMasterHandler.java: a network handler to handler 2PC operation requests from the master server.

The latest Java source code of my implementation is available in my [github repository](https://github.com/garudareiga/computer_system_design/tree/master/distributed_kvstore/src/edu/berkeley/cs162)
