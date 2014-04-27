Title: Hadoop MapReduce - Running WordCount 
Date: 2014-04-25 22:07
Author: Ray Chen
Category: Hadoop 
Tags: hadoop, mapreduce 

#### WordCount Example

WordCount is a simple program which counts the number of occurrences of each word in an input data set. It is a great example to understand the Hadoop MapReduce programming model.

Generally Hadoop can be run in three modes:

- __Standalone (or local) mode__: There are no daemons running in this mode. Hadoop uses the local file system instead of HDFS.
- __Pseudo-distributed mode__: All the daemons run on a single machine locally using the HDFS protocol and this setting mimics the behavior of a cluster.
- __Fully-distributed mode__: This is how Hadoop runs on a real cluster.

I run WordCount application in pesudo-distributed mode here.

#### Hadoop Installation

You can install Hadoop on your local machine following the [instruction](http://www.bigdataplanet.info/2013/10/Hadoop-Installation-on-Local-Machine-Single-node-Cluster.html), or you can download and use Cloudera Quickstart VM. I already have Hadoop version 1.2.1 installed on my Ubuntu 12.04 LTS.

#### Plain Java Version

You can download the WordCount Java source code from this [link](http://www.cloudera.com/content/cloudera-content/cloudera-docs/HadoopTutorial/CDH4/Hadoop-Tutorial/ht_wordcount1_source.html). Then I will show you how to prepare the data set in HDFS and submit Hadoop MapReduce job step by step:

+ Create the input directory wordcount/input in HDFS:
```bash
$ hadoop fs -mkdir wordcount/input
```
+ Create sample text files as input and move to the input directory:
```bash
$ echo "Hello Bye" > file0 && echo "Hello Goodbye" > file1
$ hadoop fs -copyFromLocal file* wordcount/input
```
+ Compile WordCount.java and create a JAR
```bash
$ mkdir wordcount && javac -cp /usr/local/hadoop/hadoop-core-1.2.1.jar -d classes WordCount.java && jar -cvf wordcount.jar -C classes/ .
```
+ Run the application
```bash
$ hadoop jar wordcount.jar us.raydevblog.hadoop.WordCount wordcount/input wordcount/output1
```
+ Examine the output:
```bash
$ hadoop fs -cat wordcount/part-00000
Bye	1
Goodbye	1
Hello	2
```
#### Using Maven Project

If you are not familiar with Maven, You can find an excellent, short
post on the Maven website called ["Maven in 5 minutes"](http://maven.apache.org/guides/getting-started/maven-in-five-minutes.html). I use the following commands to create a Maven project and adjust the POM:

+ First thing is to create a project structure using Maven:
```bash
$ mvn archetype:generate -DgroupId=us.raydevblog.hadoop -DartifactId=WordCountV2 -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```
+ Reference the Hadoop libraries in the pom.xml:
```xml
<dependency>
  <groupId>org.apache.hadoop</groupId>
  <artifactId>hadoop-core</artifactId>
  <version>1.2.1</version>
</dependency>
``` 
+ Inorder to make us an executable JAR, we need tell Maven what class is holding our "main" function. I create a __build__ node and within that node create a __plugins__ node and then add the following:
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <configuration>
    <archive>
      <manifest>
        <addClasspath>true</addClasspath>
        <mainClass>us.raydevblog.hadoop.WordCount</mainClass>
      </manifest>
    </archive>
  </configuration>
</plugin>
```
+ Also need add this plugin to use Java 1.7 for compilation. Otherwise, we will have the error "generics are not supported in -source 1.3":
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <source>1.7</source>
    <target>1.7</target>
  </configuration>
</plugin>
```
+ I copy WordCount.java into src/main/java/us/raydevblog/hadoop/ and remove the template provided "App.java" in this folder. Now it is time to compile our project and run the application:
```bash
$ mvn clean install
$ hadoop jar target/WordCountV2-1.0-SNAPSHOT.jar wordcount/input wordcount/output2
``` 

We now have a WordCount Map-Reduce example running successfully on the Hadoop. You can download my WordCount maven project from my [github reposity](https://github.com/garudareiga/hadoopstudy/tree/master/wordcount)
