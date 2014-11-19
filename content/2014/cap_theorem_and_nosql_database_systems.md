Title: CAP Theorem and Key-based NoSQL Database Systems
Date: 2014-10-15 21:00 
Author: Ray Chen 
Category: System

## CAP Theorem

CAP is an abbreviation for **C**onsistency, **A**vailability, and **P**artition tolerance. The [CAP Theorem] states that in a distributed system, you can have only two of these properties, but not all three at once. One of them must be sacrificed. 

#### Consistency
A read request in a distributed system sees all previously completed writes. Traditional ways to achieve this in relational database systems are distributed transactions. 

#### Availability
The distributed system guarantees responses for requests within a reasonable amount of time, even though one or more nodes are down. To achieve availability data in a cluster must be replicated to a number of nodes, and every node must be ready to claim master status at any time.

#### Partition Tolerance
Nodes can be physically separated from each other, and are not able to reach each other at any point and for any length of time, when network partitions occur. During the partition, the distributed system should still be able to serve both read and write quests.

#### CP and AP 
Given completely unreliable networks, we must tolerate partitions in a distributed system. It's considered impossible to offer both full consistency and 100% availability at the same time, there will always be trade-offs involved. 

- CP - Consistency/Partition Tolerance: choose consistency over availability when your business requirements dictate atomic reads and writes.
- AP - Availability/Partition Tolerance: choose availability over consistency when your business requirements allow for some flexibility and the system needs to continue to function in spite of external errors.

The ["Visual Guide to NoSQL Systems"](http://blog.nahurst.com/visual-guide-to-nosql-systems) offers a quick overview of the major trade-offs involved with relational and NoSQL database systems as follows:
![Alt text](http://www.raydevblog.us/images/nosql.jpg)

## Key-based NoSQL Database Systems

The **data model** of a database specifies how data is logically organized. Its **query model** dictates how the data can be retrieved and updated. Common data models are the relational model, key-based model, or various graph models. Query languages include SQL, key lookups, and MapReduce [1]. NoSQL systems combine different data and query models, resulting in different architectures.

Key-based NoSQL systems restrict lookups on a dataset to a single key field. The key-based lookup model is beneficial because the database has a consistent query pattern - the entire workload consists of key lookups whose performance is relatively uniform and predictable.

Let's quickly look at the data associated with each key. Various NoSQL systems offer different solutions.

#### Key-Value Stores
The simplest form of NoSQL store is a key-value store.
In key-value stores, such as Dynamo and Voldemort, each key is mapped to a value containing arbitrary data, which is a [blob] containing JSON or binary format. The key-value store has no knowledge of the contents of its payload. In order to use structured formats to store complex data for a key, developers must operate against the data in application space. 

Key-value stores shine in the simplicity of their query model, usually consisting of set, get, and delete primitives, but discard the ability to add simple in-database filtering capabilities due to the opacity of their values.

#### Key-Data Structure Stores
Key-data structure stores assign each value a type. In Redis, the available types are integer, string, list, set, and sorted set. By providing simple type-specific functionality while avoiding multi-key operations such as aggregation or joins, Redis balances functionality and performance.

#### Key-Document Stores
Key-document stores, such as CouchDB, MongoDB, and Riak, map a key to some document that contains structured information. These systems store documents in a JSON or JSON-like format. They store lists and dictionaries, which can be embedded recursively inside one-another.

The freedom and complexity of document stores is a double-edged sword: application developers have a lot of freedom in modeling their documents, but application-based query logic can become exceedingly complex.

#### BigTable Column Family Stores
HBase and Cassandra are based on Google's BigTable. In this model, a key identifies a row, which contains data stored in one or more Column Families (CFs). Within a CF, each row can contain multiple columns. The values within each column are timestamped, so that several versions of a row-column mapping can live within a CF. 

Conceptually, one can think of Column Families as storing complex keys of the form (row ID, CF, column, timestamp), mapping to values which are sorted by their keys. The model is particularly good at modeling historical data with timestamps.

## Data Durability
Data durability is in tension with performance. Different NoSQL systems make different data durability guarantees in order to improve performance. No all NoSQL systems protect us against failures.

#### Single-server Durability
The simplest form of durability is a single-server durability. The single-server durability usually means writing the changed data to disk, which often bottlenecks your workload. To ensure efficient single-server durability, we need minimize the number of random writes between *fsync* system calls, and maximize the number of sequential writes per hard drive.

+ Control *fsync* frequency: Memcached offers no on-disk durability in exchange for extremely fast in-memory operations. Redis offers developers several options for when to call *fsync*. 
+ Increase sequential writes by logging: To reduce random writes, systems such as Cassandra, HBase, Redis, and Riak append update operations to a sequentially-written log file, which is frequently fsynced. The log is treated as the ground-truth state of the database after a crash.

#### Multi-server Durability
Many NoSQL systems offer multi-server durability by copying data across nodes.

+ Redis takes a traditional **master-slave** approach to replicating data. All operations executed against a master are communicated in a log-like fashion to slaves, which replicate the operations on their own hardware. If a master fails, a slave can step in and serve the data from the state of the operation log that it received from the master. CouchDB facilitates a similar form of directional replication.
+ MongoDB provides the notion of replica sets, where some number of servers are responsible for storing each document. It gives developers the option of ensuring that all replicas have received updates, or to proceed without ensuring that replicas have the most recent data.
+ HBase receives multi-server durability through HDFS. All writes are replicated to two or more HDFS nodes before returning control to the user, ensuring multi-server durability.
+ Riak, Cassandra, and Voldemort support quorum-based configurable forms of replication. They allow the user to specify $N$, the number of nodes which should have a copy of the data, and $W < N$, the number of nodes that should confirm the data has been written before returning control to the user.
+ Cassandra, HBase, and Voldemort support multi-server replication across data centers. Updates are streamed across data centers without confirmation to back up data centers.

## Horizontal Scalability

Sharding is the act of splitting your read and write wordload across multiple nodes to scale out your system. 

#### Do Not Shard Until You Have To
There are two ways to scale without sharding: **read replicas** and **caching**. Read replicas and caching allow us to scale up our read-heavy workloads.

+ Read replicas: Make copies of the data on multiple nodes. All write requests still go to a master node. Read requests go to nodes which replicate the data, and are often slightly stale with respect to the data on the master node.
- Caching: Memcached dedicates blocks of memory on multiple nodes to cache data from data storage. Memcached clients distribute load across Memcached installations on different nodes.

#### Sharding Through Coordinators

Twitter built the notions of sharding and replication into a coordinating framework called [Gizzard](https://github.com/twitter/gizzard). Gizzard is designed to replicat data acroos any network-available data storage service SQL or NoSQL. It handles partitioning by mapping ranges of data to particular shards, and these mappings are stored in a forwarding table. 

#### Consistent Hashing

Good hash functions distribute a set of keys in a uniform manner, which make them a powerful tool for distributing key-value pairs among multiple nodes. The **consistent hashing** technique was first adopted by Amazon's Dynamo, and then it appears in Cassandra, Voldemort, and Riak.  

Consistent hashing works as follows. Say we have a hash function $H$ that maps keys to the range of [0, 2^128] (e.g. MD5 hash). Given a list of $N$ nodes, hash them to integers in the range by taking each node's unique identifier (e.g. IP address). To map a key to a server, we hash it to a single integer, move clockwise on the consistent hash ring until finding the first node it encounters.

![Alt text](http://www.raydevblog.us/images/consistent_hash_ring.gif)

Replication for multi-server durability is achieved by passing the keys and values in one server's assigned range to the servers following it in the ring. For example, with a replication factor of 3, keys mapped to server A will be stored on servers A, B, C.

Hashing requires many nodes before it distributed evenly. We often start with a small number of physical nodes, so we create a number of virtual nodes to achieve better load balancing. The hash-space is divided into $P$ evenly sized partitions, and assign $P/N$ partitions per physical node. When a physical node joins, all data from partitions of other physical nodes are uniformly get assigned to the new physical node. When a physical node leaves, it gives back to remaining nodes. The number of virtual nodes is picked once during building of the ring and never changes over the lifetime of the cluster. 

![Alt text](http://www.raydevblog.us/images/virtual_nodes.gif)

How should the clients find and talk to the nodes in the consistent hashing ring? There are a few options on how we keep track of consistent hash ring.

+ Centralized coordination: A dedicated machine keeps track of a ring configuration and works as a central load-balancer which routes client's request to appropriate nodes.
+ Full decentralized configuration: Each node keeps a full copy of the ring configuration. Join/Leave of a node from the ring requires notification of all other nodes in the ring. This option is used in Amazon Dynamo.
+ Distributed configuration with an external nanny: The overall system would depend on an independent monitor of the ring. Clients keep a local copy of the ring configuration, and periodically sync with the external monitor. Zookeeper is good at this kind of thing.

#### Range Partitioning
In the range partitioning approach, some nodes in our system keep metadata about which nodes contain which key ranges. This metadata is consulted to route key and range lookups to the appropriate servers. This range partitioning splits the keyspace into ranges, which each key range being managed by one node and potentially replicated to others. Two keys that are next to each other in the key's sort order are likely to appear in the same partition.

+ HBase employs Google BigTable's hierarchical approach to range-partitioning. The master maintains the tablet assignment in a metadata table. When this metadata gets large, the metadata table is also sharded into tablets that map key ranges to tablets and tablet servers responsible for those ranges. Underlying tablet data is stored in HDFS, and HDFS handles data replication and consistency among replicas. ZooKeeper manage secondary master servers and tablet server reassignment.
+ In MongoDB, several configuration nodes store and manage the routing tables that specify which storage nodes is responsible for which key ranges. These configuration nodes stay in sync through a protocol called two-phase commit. Storage nodes are arranged in replica sets to handle replication.
+ Cassandra provides an order-preserving partitioner. Rather than hashing a key-value pair onto the consistent hashing ring, the key is simply mapped onto the server which controls the range in which the key naturally fits.

### Consistency

Keeping replicas of data on multiple machines consistent with on-another is hard. There are two major approaches to data consistency in the NoSQL ecosystem: **strong consistency** (all replicas remain in sync) and eventual consistency (replicas are allowed to get out of sync, but eventually catch up with one-another). Other approaches exist, such as the relaxed consistency and relaxed availability appoach presented in Yahoo!'s PNUTS system.

#### Strong Consistency

Say we replicate a key on $N$ machines. Some machines, perhaps one of the $N$, serves as a coordinator for each user request. The coordinator ensures that a certain number of the $N$ machines has received and acknowledged each request. When a write or update occurs to a key, the coordinator does not confirm with the user that the write occurred util $W$ replicas confirm that they have received the update. When a user wants to read the value for some key, the coordinator responds when at least R have responded with the same value. We say that the system exemplifies strong consistency if $R + W > N$. 

When $W$ replicas do not respond to a write request, or $R$ replicas do not respond to a read request with a consistent response, the coordinator can timeout eventually and send the user an error, or wait until the situation correct itself. Either way, the system is considered unavailable for that request for at least some time.

You choice of $R$ and $W$ affect how many machines can act strangely before your system becomes unavailable for different actions on a key. A common choice is $R + W = N + 1$, the minimum required for strong consistency while still allowing for temporary disagreement between replicas. Many strong consistency systems opt for $W=N$ and $R=1$, since they do not have to design for nodes going out of sync.

#### Eventual Consistency

Dynamo-inspired system, including Cassandra, Riak and Voldemort, allow the user to specify $N$, $R$, and $W$ to their needs, even if $R + W <= N$. User can achieve either strong or eventual consistency. Let's find out how various systems determine that data has gotten out of sync, how they synchronize replicas, and how to speed up the synchronization process.

##### Versioning and Conflicts

Because two replicas might see two different versions of a value for some key, data versioning and conflict detection is important. Dynamo uses a type of versioning called **vector clocks**. 

A vector clock is a vector assigned to each key which contains a counter for each replica. Each time a replica modifies a key, it increments its counter in the vector. Say we have two replicas A and B. If vector clock counters in A are all less than the ones in B, then A has a stale version and can overwrite its own copy with B's. If A and B have vector clocks in which some counters are greater than others in both clocks, we identify a conflict.

##### Conflict Resolution

Conflict resolution varies across the different systems.
- Dynamo and Voldemort leave conflict resolution to the application using the storage system.
- Cassandra, which stores a timestamp on each key, uses the most recently timestamped version of a key when two versions are in conflict.

##### Read Repair

When the coordinator identifies a conflict on read, even if a consistent value has been returned to the user, the coordinator starts conflict-resolution protocols between conflicted replicas. 

##### Hinted Handoff

If one of the replicas for a key does not respond to a write request, another node is selected to temporarily take over its write workload. Writes for the unavailable node are kept separately, and when the backup node notices the previously unavailable node become available, it forward all of the writes to the newly available replica. 

##### Anti-Entropy

In anti-entropy, replicas exchange **Merkel Trees** to identify parts of their replicated key ranges which are out of sync. A Merkel tree is a hierarchical hash verification: if the hash over the entire keyspace is not the same between two replicas, they will exchange hashes of smaller and smaller portions of the replicated keyspace until the out-of-sync keys are identified. This approach reduces unncessary data transfer between replicas which contain mostly similar data.

#### Gossip

System employs gossip protocol to keep track of nodes. Periodically, a node will pick a random node it once communicated with to exchange of the health of the other nodes in the system. If provoiding this exchange, nodes learn which other nodes are down, and know where to route clients in search of a key.

### References
- [CAP Theorem: Revisited]
- [The NoSQL Ecosystem]
- [How automatic sharding works or consistent hashing under the hood]
- [Distributed Algorithms in NoSQL Databases]

[1]:http://aosabook.org/en/nosql.html
[The NoSQL Ecosystem]:http://aosabook.org/en/nosql.html
[blob]:http://en.wikipedia.org/wiki/Binary_large_object
[CAP Theorem]:http://en.wikipedia.org/wiki/CAP_theorem
[CAP Theorem: Revisited]:http://robertgreiner.com/2014/08/cap-theorem-revisited
[NoSQL Databases Explained]:http://www.mongodb.com/nosql-explained
[How automatic sharding works or consistent hashing under the hood]:http://ivoroshilin.com/2013/07/15/distributed-caching-under-consistent-hashing/
[Distributed Algorithms in NoSQL Databases]:http://highlyscalable.wordpress.com/2012/09/18/distributed-algorithms-in-nosql-databases/



















































