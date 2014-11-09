Title: Creational Patterns in Java
Date: 2014-11-09 10:30 
Author: Ray Chen 
Category: Java

## Factory Design Pattern

### Factory Pattern
**Factory pattern** is used to create instances of different classes of same type, based on different parameters. It helps encapsulate object creation. The example below is about creating **Pizza** in a factory:

+ Pizza: product of the factory
+ CheesePizza/VeggiePizza: concrete products that implement the Pizza interface
+ PizzaFactory: factory where create concrete products
+ PizzaStore: client of the factory

In design patterns, the phrase "implement an interface" does NOT always mean "write a class that implements a Java interface, by using the **implements** keyword in the class declaration." In the general use of the phrase, a concrete class implementing a method from a **supertype** (which could be a class OR interface) is still considered to be "implementing the interface" of that supertype.

[gist:id=4bc01df870e1c1b87843,file=factory-pattern.java]

### Factory Method Pattern
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

### Factory Method and Abstract Factory compared:

Factory Method

+ Provides an abstract interface for creating ***one*** product.
+ PizzaStore is implemented as a Factory Method because we want to be able to create a product that varies by region. With the Factory Method, each region gets its own concrete factory that knows how to make pizzas which are appropriate for the area. 

Abstract Factory

+ Provides an abstract interface for creating a ***family*** of products.
+ PizzaIngredientFactory is implemented as an Abstract Factory because we need to create families of products (the ingredients). Each subclass implements the ingredients using its own regional suppliers. Methods to create products are often implemented with a Factory Method.
