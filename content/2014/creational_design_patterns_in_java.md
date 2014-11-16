Title: Creational Patterns in Java
Date: 2014-11-09 10:30 
Author: Ray Chen 
Category: Java

### Singleton Design Pattern

Singleton design pattern restricts the instantiation of a class and ensures that only one instance of the class exists in the JVM. It is used for logging, caching and thread pool.

#### Eager Initialization
Using eager initialization, we rely on the JVM to create the unique Singleton instance when the class is loaded. The JVM guarantees that the instance will be created before any thread accesses the static uniqueInstance variable.
If a singleton is expected to carry state, then those state variables should have synchronized access to make them thread safe.

[gist:id=198c94bae70cb36cf5fe,file=singleton-pattern.java]

#### Lazy Initialization
Use "double-checked locking" to reduce the use of synchronization in **getInstance()**. The volatile keyword ensures that multiple threads handle the uniqueInstance variable correctly when it is being initialized to the Singleton instance.

[gist:id=198c94bae70cb36cf5fe,file=singleton-lazy-initialization.java]

#### Bill Pugh Approach
The Bill pugh approach suggests to use static inner class. Until we need an instance, the SingletonHolder class will not be initialized until required. 

[gist:id=198c94bae70cb36cf5fe,file=singleton-bill-pugh.java]

#### Unit Test
Singletons are hard to mock in unit tests due to their private constructors. We should always have singletons implement an interface which allows for mock instances in unit tests. As follows, we can use **Dependency Injection** to make the **Client** class to receive the **Server** singleton instance in its constructor, instead of using the static **getInstance** method.

[gist:id=198c94bae70cb36cf5fe,file=singleton-server-interface.java]

### Factory Design Pattern

#### Factory Pattern
**Factory pattern** is used to create instances of different classes of same type, based on different parameters. It helps encapsulate object creation. The example below is about creating **Pizza** in a factory:

+ Pizza: product of the factory
+ CheesePizza/VeggiePizza: concrete products that implement the Pizza interface
+ PizzaFactory: factory where create concrete products
+ PizzaStore: client of the factory

In design patterns, the phrase "implement an interface" does NOT always mean "write a class that implements a Java interface, by using the **implements** keyword in the class declaration." In the general use of the phrase, a concrete class implementing a method from a **supertype** (which could be a class OR interface) is still considered to be "implementing the interface" of that supertype.

[gist:id=4bc01df870e1c1b87843,file=factory-pattern.java]

#### Factory Method Pattern
**The Factory Method Pattern** defines an interface for creating an object, but lets subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses. This decouples the client code in the superclass from the object creation code in the subclass.
```java
abstract Product factoryMethod(String type)
```

The example below is about creating Pizza using a factory method:

[gist:id=4bc01df870e1c1b87843,file=factory-method-pattern.java]

### Abstract Factory Pattern

The abstract factory pattern provides an interface for creating families of related or dependent objects without specifying their concrete classes.

The example below is about creating Pizza using abstrace factory pattern:

+ PizzaIngredientFactory: defines the interface that all concrete factories must implement.
+ NYPizzaIngredientFactory: concrete pizza factory making pizza ingredients.
+ NYPizzaStore: client which composed at runtime with an actual factory.
+ Dough/Cheese/Pepperoni: product family. Each concrete factory can produce a different set of products.

[gist:id=4bc01df870e1c1b87843,file=abstract-factory-pattern.java]

#### Factory Method and Abstract Factory compared:

Factory Method

+ Provides an abstract interface for creating ***one*** product.
+ PizzaStore is implemented as a Factory Method because we want to be able to create a product that varies by region. With the Factory Method, each region gets its own concrete factory that knows how to make pizzas which are appropriate for the area. 

Abstract Factory

+ Provides an abstract interface for creating a ***family*** of products.
+ PizzaIngredientFactory is implemented as an Abstract Factory because we need to create families of products (the ingredients). Each subclass implements the ingredients using its own regional suppliers. Methods to create products are often implemented with a Factory Method.

### Reference

- [Singleton design pattern in java](http://howtodoinjava.com/2012/10/22/singleton-design-pattern-in-java/)
- [Using Dependancy Injection to Avoid Singletons](http://googletesting.blogspot.com/2008/05/tott-using-dependancy-injection-to.html)
