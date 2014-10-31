Title: Scaling Memcache at Facebook
Date: 2014-10-30 20:50 
Author: Ray Chen 
Category: System

A summary of how Facebook took **memcached** as a basic building block, which provides a network attached in-memory hash table and supports LRU based eviction, and built a large distributed key-value storage system. The scaling is from a single cluster of servers to multiple geographically distributed clusters. Details are described in the paper "[Scaling Memcache at Facebook](http://pdos.csail.mit.edu/6.824-2013/papers/memcache-fb.pdf)".

## Overview

Memcache vs. memchached

+ memcached is the standalone server software
+ Memcache is the distributed caching system

Facebook rely on **memcache** to lighten the read load on databases, as a *demand-filled look-aside* cache as shown in Figure:

![Alt text](http://www.raydevblog.us/images/memcache_wr.jpg)

Memcache Usage at Facebook

+ Caching results of complex RPC calls, such as timeline aggregations
+ Query cache for expensive TAO/DB queries, such as birthday index, typeahead bootstrap data
+ Write-heavy, non-durable storage, such as complex calculation analytics

## Latency and Load
Within a cluster, Facebook focus on reducing either the latency of fetching cached data or the road imposed due to a cache miss.

### Reducing Latency
The latency of memcache's response is a critical factor in the response time of a user's request. Facebook provision hundreds of memcached servers in a cluster to reduce load on databases. Items are distributed across the memcached servers through consistent hashing. All web servers communicate with every memcached server. This all-to-all communication pattern can cause a single server to become the bottleneck for many web servers. Facebook reduce latency from memcache client, which runs on each web server.

+ **Parallel request and batching**: Structure web application code to
	- Construct a directed acyclic graph (DAG) representing the dependencies between data
	- Maximize the number of items that can be fetched concurrently
	- Minimize the number of network round trips necessary to respond to page requests.  
+ **Client-server communication**: Clients use UDP and TCP to communicate with memcached servers.
	- Use UDP for **get** requests to reduce latency and overhead.
	- Use TCP for **set** and **delete** requests for reliability, through **mcrouter** running on the same machine as the web server.

### Reducing Load	

#### Leases
Two problems:

- A **stale set** occurs when concurrent updates to memcache get reordered.
- A **thundering herd** occurs when a specific key undergoes heavy read and write operations. Many reads default to the expensive paths such as database queries, as write operations repeatedly invalidates the recent values.

A memcached instance gives a **lease** to a client to set data back into the cache when that client experiences a cache miss. With the lease token, memcached can verify and determine whether data should be stored. Each memcached server also regulates the rate at which it returns token. 

#### Memcache Pools
Using memcache as a general-purpose caching layer requires workloads to share infrastructure. Due to heterogenous workloads, Facebook partition a cluster's memcached server into separate pools. For example, Facebook provision a small pool for keys that are accessed frequently but for which a cache miss is inexpensive, and provision a large pool for infrequently accessed keys for which cache misses are prohibitively expensive.

#### Replication Within Pools
Within some pools, Facebook use replication to improve the latency and efficiency of memcached servers. A client's request can be sent to any replica. This approach requires delivering invalidations to all replicas to maintain consistency.

### Handling Failures
In a large distributed system, something is always broken. When a memcached client receives no response to its get request, the client assumes the server has failed and issues the request to a special **Gutter** pool. If this second request misses, the client will insert the key-value pair into the Gutter machine after querying the database.Entries in Gutter expire quickly. Gutter limits the load on databases at the cost of slightly stale data.

## In a Region: Replication

Facebook split web and memcached servers into multiple **frontend clusters**. These clusters, along with a storage cluster that contain the databases, define a **region**.

The figure below illustrates the final architecture of organizing co-located clusters into regions.

![Alt text](http://www.raydevblog.us/images/memcache.jpg)

## Across Regions: Consistency

Facebook designate one region to hold the master databases and the other regions to contain read-only replicas. They rely on MySQL's replication mechanism to keep replica databases up-to-date with their masters. Replica databases may lag behind the master database. 

## Reference
- [Scaling Memcache at Facebook](https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala)
- [Turning Caches into Distributed Systems with mcrouter](https://www.youtube.com/watch?v=e9lTgFO-ZXw)




