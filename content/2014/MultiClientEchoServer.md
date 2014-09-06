Title: Implementing a Multi-Client Echo Server using Go
Date: 2014-09-05 10:00 
Author: Ray Chen 
Category: System design

### Server Characteristic 

The multi-client echo server must have the following characteristics:

- The server must manage and interact with its clients concurrently using goroutines and channels. Multiple clients should be able to connect/disconnect to the server simultaneously. 
- When the server reads a newline-terminated message from a client, it must respond by writing that exact message to all connected clients. 
- The server must be responsive to slow-reading clients. Consider when a client does not call **Read** for an extended period of time. If during this time the server continues to write messages to the client's TCP connection, eventually the TCP connection's output buffer will reach maximum capacity and subsequent calls to **Write** made by the server will block. The server should keep a queue of at most 100 outgoing messages to be written to the client. Messages sent to a slow-reading client whose outgoing message buffer has reached the maximum capacity of 100 should simply be dropped.

### Go's Concurrency Model

Go's approach to concurrency differs from the traditional use of threads and shared memory. Go encourages an approach in which shared values are passed around on channels and never actively shared by separate threads of execution. It can be summarized:

> Don't communicate by sharing memory; share memory by communicating.

As a high-level approach, using channels to control access makes it easier to write clear, correct programs.

#### Goroutines

Goroutine is a functon executing concurrently with other goroutines in the same address space. They are lightweight and cheap. Goroutines are multiplexed onto multiple OS threads, hiding the complexities of thread creation and management.

#### Channels

By default, the channel is unbuffered, which provides communication with synchronization. A buffered channel can be used like a semaphore, for instance to limit throughput. Channels allow you to pass references to data structures between goroutines. If consider this as passing around ownership of the data (the ability to read and write it), it becomes a powerful synchronization mechanism.

