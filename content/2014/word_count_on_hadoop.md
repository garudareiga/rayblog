Title: Word Count on Hadoop 
Date: 2014-04-10 22:07
Author: Ray Chen
Category: Hadoop 
Tags: hadoop, mapreduce 

### Hadoop WordCount

WordCount is a simple program which counts the number of occurrences of each word in an input data set. It is a great example to understand the Hadoop MapReduce programming model.

Generally Hadoop can be run in three modes.
- __Standalone (or local) mode__: There are no daemons running in this mode. Hadoop uses the local file system instead of HDFS.
- __Pseudo-distributed mode__: All the daemons run on a single machine locally using the HDFS protocol and this setting mimics the behavior of a cluster.
- __Fully-distributed mode__: This is how Hadoop runs on a real cluster.

### Hadoop Installation

You can install Hadoop on your local machine folowing the instruction from ###, or you can download and use Cloudera Quickstart VM. I installed Hadoop 1.2.1 on my Ubuntu 12.04 LTS.

### WordCount Java Version 1

You can download the WordCount Java source code from my github repository. I will show you how to prepare the data set in HDFS and submit Hadoop MapReduce job step by step:

1. Create the input directory /user/<name>/wordcount/input in HDFS:
```shell
$ hadoop fs -mkdir wordcount/input
```
2. Create sample text files as input and move to the input directory:
```shell
$ echo "Hello Bye" > file0 && echo "Hello Goodbye" > file1
$ hadoop fs -copyFromLocal file* wordcount/input
```
3. Compile WordCountV1.java and create a JAR
```shell
$ mkdir wordcount && javac -cp /usr/local/hadoop/hadoop-core-1.2.1.jar -d classes WordCount.java && jar -cvf wordcount.jar -C classes/ .
```
4. Run the application
```shell
$ hadoop jar wordcount.jar
```
5. Examine the output:
```shell
$ hadoop fs -cat wordcount/part-00000
Bye	1
Goodbye	1
Hello	2
```
