Title: Implementing a Multi-Client Echo Server using Go
Date: 2014-09-05 10:00 
Author: Ray Chen 
Category: System

### Server Characteristic 

The multi-client echo server must have the following characteristics:

- The server must manage and interact with its clients concurrently using goroutines and channels. Multiple clients should be able to connect/disconnect to the server simultaneously. 
- When the server reads a newline-terminated message from a client, it must respond by writing that exact message to all connected clients. 
- The server must be responsive to slow-reading clients. Consider when a client does not call *Read* for an extended period of time. If during this time the server continues to write messages to the client's TCP connection, eventually the TCP connection's output buffer will reach maximum capacity and subsequent calls to *Write* made by the server will block. The server should keep a queue of at most 100 outgoing messages to be written to the client. Messages sent to a slow-reading client whose outgoing message buffer has reached the maximum capacity of 100 should simply be dropped.

### Go's Concurrency Model

Go's approach to concurrency differs from the traditional use of threads and shared memory. Go encourages an approach in which shared values are passed around on channels and never actively shared by separate threads of execution. It can be summarized:

> Don't communicate by sharing memory; share memory by communicating.

As a high-level approach, using channels to control access makes it easier to write clear, correct programs.

#### Goroutines

Goroutine is a functon executing concurrently with other goroutines in the same address space. They are lightweight and cheap, costing little more than the allocation of small stack space. Goroutines are multiplexed onto multiple OS threads, hiding the complexities of thread creation and management. They silently manages their own threading, and silently returns when they have finished.

#### Channels

Channels act like pipes. By default, the channel is unbuffered, which provides communication with synchronization. A buffered channel is asynchronous; sending or receiving will not wait unless the channel is full. It can be used like a semaphore, for instance to limit throughput. Channels allow you to pass references to data structures between goroutines. If consider this as passing around ownership of the data (the ability to read and write it), it becomes a powerful synchronization mechanism.

### Echo Server Implementation

Next I'll explain some Go-specific mechanisms to meet the design requirement. 

#### Support Clients Concurrently

When the server starts, it creates a central goroutine that opens a socket and keeps listening for incoming TCP requests on a given port. For each TCP request from a client, the server creates two goroutines for reading from and writing to the connection. When client disconnects from the server, these two goroutines will finish silently. Thus, server is able to interact with mutliple clients concurrently.

#### Avoid Data Race

A data race occurs when two goroutines access the same variable concurrently and at least one of the accesses is a write. The server manages clients using a map, unique client ids as keys and pointers of client objects as values. This map is a goroutine-global variable. In order to avoid data race, its ownership has to be passed around goroutines, adding/deleting clients when clients connect/disconnect to the server concurrently. I choose to use a channel **eclChan** of size one, that stores the map and acts like a binary semaphore (or mutex) to provide synchronization among goroutines.

```go
// New creates and returns (but does not start) a new MultiEchoServer.
func New() MultiEchoServer {
    ptrServer := &multiEchoServer{
        host:    "localhost",
        eclChan: make(chan map[int]*echoClient, 1),
        stop:    make(chan bool),
    }
    return MultiEchoServer(ptrServer)
}
```

#### Use Message Queue

To be responsive to possible slow **READ** clients, we need a message queue of at most 100 outgoing messages for each client. Apparently, a buffered string channel named as **"ch"** fits this role:

```go
type echoClient struct {
    conn net.Conn
    ch   chan string
}
```

To drop messages when the channel is full, I asked for some help from [stackoverflow](http://stackoverflow.com/questions/25657207/golang-how-to-know-a-buffered-channel-is-full?noredirect=1#comment40125761_25657207) and solve the issue using the **select** statement:

```go
select {
case echoClient.ch <- msg:
default: // discard value if channel is full
}
```

#### Stop Server Gracefully

When the server stops, I need terminate the central goroutine listening on a given port gracefully. Here, an unbuffered boolean channel **stop** (defined in **MultiEchoServer** type above) will pass the termination signal to the central goroutine, and the magic **select** statement again decide when to emit the signal:

```go
// central goroutine
for {
    conn, err := mes.ln.Accept() // listen for TCP connections
    if err != nil {
        select {
        case <-mes.stop: // stop listening
            return
        default:
        }
        continue
    }
    // create goroutines for each connection from clients ...
}
```

### Finished

We now have a fully functional echo server that supports multiple clients concurrently. The full source code for a multi-client echo server is available [here](https://github.com/garudareiga/cmu-440/tree/master/p0). Your criticism or suggestion is welcome.