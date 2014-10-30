Title: CAP Theorem and NoSQL Database Systems
Date: 2014-10-15 21:00 
Author: Ray Chen 
Category: System

## CAP Theorem

CAP is an abbreviation for consistency, availability, and partition tolerance. The [CAP Theorem] states that in a distributed system, you can have only two of these properties, but not all three at once. One of them must be sacrificed. 

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
I
The ["Visual Guide to NoSQL Systems"](http://blog.nahurst.com/visual-guide-to-nosql-systems) offers a quick overview of the major trade-offs involved with relational and NoSQL database systems.
![Alt text](http://www.raydevblog.us/images/nosql.png)

## Key-based NoSQL Database Systems

The data model of a database specifies how data is logically organized. Its query model dictates how the data can be retrieved and updated. Common data models are the relational model, key-based model, or various graph models. Query languages include SQL, key lookups, and MapReduce [1].

Key-based NoSQL systems restrict lookups on a dataset to a single key field. The key-based lookup model is beneficial because the database has a consistent query pattern - the entire workload consists of key lookups whose performance is relatively uniform and predictable.

#### Key-Value Stores
In key-value stores, such as Dynamo and Voldemort, each key is mapped to a value containing arbitrary data. The key-value store has no knowledge of the contents of its payload, and it might map the key to a [blob] containing JSON or binary format. In order to use structured formats to store complex data for a key, developers must operate against the data in the application space. Key-value stores shine in the simplicity of their query model.

#### Key-Data Structure Stores
Key-data structure stores assign each value a type. In Redis, the available types are integer, string, list, set, and sorted set. By providing simple type-specific functionality while avoiding multi-key operations such as aggregation or joins, Redis balances functionality and performance.

#### Key-Document Stores
Key-document stores, such as CouchDB9, MongoDB10, and Riak11, map a key to some document that contains structured information. These systems store documents in a JSON or JSON-like format. They store lists and dictionaries, which can be embedded recursively inside one-another.

#### BigTable Column Family Stores
HBase and Cassandra are based on Google's BigTable. In this model, a key identifies a row, which contains data stored in one or more Column Families (CFs). Within a CF, each row can contain multiple columns. The values within each column are timestamped, so that several versions of a row-column mapping can live within a CF. Conceptually, one can think of Column Families as storing complex keys of the form (row ID, CF, column, timestamp), mapping to values which are sorted by their keys.

## Data Durability
Different NoSQL systems make different data durability guarantees in order to improve performance. No all NoSQL systems protect us against failures.

#### Single-server Durability
The simplest form of durability is a single-server durability. The single-server durability usually means writing the changed data to disk, which often bottlenecks your workload. To ensure efficient single-server durability, we need minimize the number of random writes between *fsync* system calls, and maximize the number of sequential writes per hard drive.

+ Control *fsync* frequency: Memcached offers no on-disk durability in exchange for extremely fast in-memory operations. Redis offers developers several options for when to call *fsync*. 
+ Increase sequential writes by logging: To reduce random writes, systems such as Cassandra, HBase, Redis, and Riak append update operations to a sequentially-written log file, which is frequently fsynced.

#### Multi-server Durability
Many NoSQL systems offer multi-server durability by copying data across nodes.

+ Redis takes a traditional **master-slave** approach to replicating data. All operations executed against a master are communicated in a log-like fashion to slave machines, which replicate the operations on their own hardware. If a master fails, a slave can step in and serve the data from the state of the operation log that it received from the master. CouchDB facilitates a similar form of directional replication.
+ MongoDB provides the notion of replica sets, where some number of servers are responsible for storing each document. It gives developers the option of ensuring that all replicas have received updates, or to proceed without ensuring that replicas have the most recent data.
+ HBase receives multi-server durability through HDFS. All writes are replicated to two or more HDFS nodes before returning control to the user, ensuring multi-server durability.
+ Riak, Cassandra, and Voldemort support quorum-based configurable forms of replication. They allow the user to specify $N$, the number of nodes which should have a copy of the data, and $W < N$, the number of machines that should confirm the data has been written before returning control to the user.

## Horizontal Scalability

#### Do Not Shard
There are two ways to scale without sharding: **read replicas** and **caching**. Read replicas and caching allow us to scale up our read-heave workloads.

+ Read replicas: Make copies of the data on multiple nodes. All write requests still go to a master node. Read requests go to nodes which replicate the data, and are often slightly stale with respect to the data on the write master.
- Caching: Memcached dedicates blocks of memory on multiple nodes to cache data from data storage. Memcached clients distribute load across Memcached installations on different nodes.

#### Consistent Hashing

#### Range Partitioning
In the range partitioning approach, some nodes in our system keep metadata about which nodes contain which key ranges. This range partitioning splits the keyspace into ranges, which each key range being managed by one machine and potentially replicated to others. 

+ HBase employs Google BigTable's hierarchical approach to range-partitioning. THe master server maintains the tablet assignment in a metadata table. The metadata table is also sharded into tablets, when this metadata gets large. Underlying tablet data is stored in HDFS, and HDFS handles data replication and consistency among replicas. ZooKeeper manage secondary master servers and tablet server reassignment.
+ MongoDB use configuration nodes to specify which storage nodes is responsible for which key ranges. These configuration nodes stay in sync through a protocol called **two-phase commit**. Storage nodes are arranged in replica sets to handle replication.

## Consistency

There are two major approaches to data consistency in the NoSQL systems. The first is **strong consistency**, where all replicas remain in sync. The second is **eventual consistency**, where replicas are allowed to get out of sync, but eventually catch up with one-another.

### References
- [CAP Theorem: Revisited]
- [The NoSQL Ecosystem]

[1]:http://aosabook.org/en/nosql.html
[The NoSQL Ecosystem]:http://aosabook.org/en/nosql.html
[blob]:http://en.wikipedia.org/wiki/Binary_large_object
[CAP Theorem]:http://en.wikipedia.org/wiki/CAP_theorem
[CAP Theorem: Revisited]:http://robertgreiner.com/2014/08/cap-theorem-revisited
[NoSQL Databases Explained]:http://www.mongodb.com/nosql-explained



















































