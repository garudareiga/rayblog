Title: Dynamo: Amazon's Highly Available Key-Value Store
Date: 2014-07-20 22:07
Author: Ray Chen
Category: System
Tags: key-value store 

This [paper](http://www.allthingsdistributed.com/2007/10/amazons_dynamo.html) was first released in SOSP'07, describes Dynamo, the underlying storage technology for several core services in Amazon's e-commerce platform. Since then, Several Dynamo-inspired databases have appeared (either entirely or partially) by this paper, such as Riak, Cassandra and Voldemort. Hence, I decide to read this paper and briefly describe some well-know technologies implemented by Dynamo.

### Introduction

Dynamo is a completely decentralized system targeting applications that operate with weaker consistency and high availability. It is built to be an **"always writeable"** data store. Hence, Dynamos allows conflicting updates in the system. 

Dynamo achieves scalability and availability by the following technologies:

- Data is partitioned and replicated using consistent hashing.
- Consistency is facilitated by object versioning. 
- The consistency among replicas during updates is maintained by a quorum-like technique and a decentralized replica synchronization protocol. 
- A gossip based distributed failure detection and membership protocol. 

### System Architecture

Table 1 presents a summary of the list of techniques Dynamo uses and their respective advantages.
![Alt text](http://www.raydevblog.us/images/dynamo.jpeg)

The paper gives details on the partitioning, replication, versioning, membership, and failure handling components of Dynamo.

### Partitioning

#### Consistent Hashing

Dynamo's partitioning scheme relies on a variant of consistent hashing for load balancing. It applies a MD5 hash on the key to generate a 128-bit identifier, which is used to determine the storage nodes. The hash output range forms a ring, and each node in the system is assigned a position on the ring. Thus, each node is responsible for the region in the ring between it and its predecessor node. To know the detail about consistent hashing, please refer to this blog [post](http://www.tomkleinpeter.com/2008/03/17/programmers-toolbox-part-3-consistent-hashing).

#### Virtual Node

Dynamo uses the concept of "virtual nodes", and each physical node can be responsible for more than one virtual node on the ring. Using virtual nodes makes the key distribution load balancing more fine-grained and more uniform:

- The load handled by an unavailable node is evenly dispersed across the remaining available nodes.
- A new node accepts a roughly equivalent of load from each of the other available nodes.
- The number of virtual nodes that a physical node is responsible can be decided by its capacity.

#### Replication

To achieve high availability, each data is replicated at N storage hosts. Each key is assigned to a coordinator node. The coordinator stores each key locally and replicates at the N-1 clockwise successor nodes in the ring. The list of nodes responsible for storing a particular key is called the **preference list**.

### Object Versioning

Dynamo provides [eventual consistency](http://en.wikipedia.org/wiki/Eventual_consistency), which allows for updates on replicas **asynchronously**. Dynamo treats the result of every modification as a new and immutable version of data. It uses **vector clocks** to capture causality between different versions of the same object. One verctor clock is associated with every version of every object. Upon processing a read request, Dynamo detects conflicts and employs application-assisted conflict resolution if necessary. 

### Sloppy Quorum

Dynamo uses a "sloppy quoram" instead of strict quorum. All read and write operations are performed on the first N healthy nodes in the preference list, skipping those that are down or inaccessible. To maintain consistency among its replicas, Dynamo uses a consistency protocol similar to quorum-based voting. This protocol has two key configurable values: R and W. R is the minimum number of nodes that must participate in a successful read operation. W is the minimum number of nodes that must participate in a successful write operation. Setting R and W such that R + W > N yields a quorum-like system. 

### Merkle Tree

A [Merke tree](http://en.wikipedia.org/wiki/Merkle_tree) is a hash tree where leaves are hashes of the values of individual keys. Parent nodes higher in the tree are hashes of their respective children. If the hash values of the root of two trees are equal, then the values of the leaf nodes in the tree are equal and the nodes require no synchronization. If not, it implies that the values of some replicas are different. 

Dynamo uses Merkle Trees for anti-entropy to keey the replicas synchronized. Each virtual node maintains a seperate Merkle tree for each key range it hosts. This allows nodes to compare whether the keys within a key range are up-to-date.

### Gossip-based Membership and Failure Detection

Decentralized failure detection protocols use a simple gossip-style protocol that enable each node in the system to learn about the arrival or departure of other nodes.

### Reference

- [Dynamo: Amazon's highly available key-value store](http://muratbuffalo.blogspot.com/2010/11/dynamo-amazons-highly-available-key.html)
- [Dynamo: A flawed architecture](http://jsensarma.com/blog/?p=55)
- [Riak docs](http://docs.basho.com/riak/1.3.2/references/dynamo/)
