Title: Bloom Filter
Date: 2014-07-28 10:00 
Author: Ray Chen 
Category: Algorithm
Tags: data structure, bloom filter

I've never used Bloom filters in practice, but I often heard about them. All I intended to do here is study general ideas and applications about Bloom filter.

Bloom filter is a space-efficient **probabilistic** data structure used to test set membership. It tells us that the element either *definitely* is not in the set or *may be* in the set. In other words, **false positives** are possible, however **false negatives** are not.

### Data Structure

Bloom filter is not a key-value store. The base data structure of a bloom filter is a **Bit Vector**, a vector of bit buckets indicating the presence of an element in the filter. 

To add an element, we simply hash it a few times and set the bits in the bit vector at the bucket index of those hashes to 1. To test for membership, we simply hash the element with the same hash functions, then see if those values are set in the bit vector. If they aren't, we know that the element isn't in the set. If they are, we only know that it *might be*, because some combination of other elements could have set the same bits. Removing an element from the filter is not possible. The more elements that are added to the set, the larger the probability of false positives. The website [Bloom Filters by Example] shows you how to add and test strings in the bloom filter.

![Alt text](http://www.raydevblog.us/images/bloom_filter.jpg)

### Hash Functions

The hash functions used in a bloom filter should be independent, uniformly distributed and as fast as possible. Examples of fast, simple hashes include [MurmurHash], the fnv series of hashes, and Jenkins Hashes. Cryptographic hashes such as sha1 and MD5 are not very good choices.

Let's assume a bloom filter with k hashes, m bits in the filter, and n elements to be inserted. [Wikipedia] provides the math for choosing these values. 

The false positive rate of our filter will be approximately:

\begin{equation} fpr = (1 - e^{-kn/m})^k \end{equation}

The more hash functions we have, the slower our bloom filter, and the quicker it fills up. If we have too few, we may suffer too many false positives. Given an m and an n, we have a function to choose the optimal value of k:

\begin{equation} k_{opt} = \frac{m}{n}\ln 2 \approx 0.7\frac{m}{n} \end{equation}

This results in:

\begin{equation} m = -\frac{n\ln fpr}{(\ln 2)^2} \end{equation}

This means that for a given false positive probability fpr, the length of a Bloom filter m is proportionate to the the number of elements being filtered n. A bloom filter with an optimal value for k and 1% error rate only needs 9.6 bits per key. Add 4.8 bits/key and the error rate decreases by 10 times.

### Extensions

Removing elments from the filter can be addressed with a **counting** bloom filter. A counting filter uses an n-bit counter instead of a single bit in each bucket. The insert operation increments the value of the buckets, and the delete operation decrements the value of the buckets. The n-bit counters must be large enough to avoid overflow.

[Almeida et al.][1] proposed a variant of Bloom filters that can adapt dynamically to the number of elements stored, while assuring a minimum false positive probability. If we can not estimate the number of elements to be inserted, we maybe better off with a scalable Bloom filter. 

### Applications and Implementations

- Bloom filters are present in a lot of NoSQL systems. Take [Cassandra] for example, Bloom filter provides a lightweight in-memory structure to reduce the number of I/O reads when performing a key loopup. Each SSTable has a bloom filter associated with it. Cassandra checks before doing any disk seeks, skipping queries for keys that don't exist. 

- The URL shortening service company Bitly, Inc. open sourced a scalable, counting bloom filter library **[dablooms]**. You can read [bitly's engineering blog post](http://word.bitly.com/post/28558800777/dablooms-an-open-source-scalable-counting-bloom) for implemetation details.

- I also found an interesting [discussion] on Quora about the best applications of Bloom filters.

- This blog [post](http://maxburstein.com/blog/creating-a-simple-bloom-filter/) shows how to create a simple bloom filter using Python. We also have a Python implementation **[PyBloom]**. 

### References

- [Bloom Filters by Example](http://billmill.org/bloomfilter-tutorial)
- [Modern Algorithms and Data Structures - Bloom Filters](http://www.slideshare.net/quipo/modern-algorithms-and-data-structures-1-bloom-filters-merkle-trees)

[Bloom Filters by Example]:http://billmill.org/bloomfilter-tutorial
[1]:http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
[discussion]:http://www.quora.com/Bloom-Filters/What-are-the-best-applications-of-Bloom-filters
[dablooms]:https://github.com/bitly/dablooms
[MurmurHash]:https://code.google.com/p/smhasher
[Wikipedia]:http://en.wikipedia.org/wiki/Bloom_filter#Probability_of_false_positives
[PyBloom]:https://github.com/jaybaird/python-bloomfilter
[Cassandra]:http://wiki.apache.org/cassandra/ArchitectureOverview

[Stackoverflow: Modern, high performance bloom filter in Python?]:http://stackoverflow.com/questions/311202/modern-high-performance-bloom-filter-in-python
[All you ever wanted to know about writing bloom filters]:http://spyced.blogspot.com/2009/01/all-you-ever-wanted-to-know-about.html
