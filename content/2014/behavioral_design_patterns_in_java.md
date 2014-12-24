Title: Behavioral Patterns in Java
Date: 2014-12-03 10:12 
Author: Ray Chen 
Category: Java

### Strategy Design Pattern

The **Strategy Pattern** defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it.

Design Principle: 

- Identify the aspects of your application that vary and seperate them from what stays the same.
- Program to an interface, not an implementation.
- Favor composition over inheritance.

Consider the **Duck** class design using strategy pattern.

- The *fly* and *quack* methods are the parts of the *Duck* class that vary across ducks. Therefore, we will pull both methods out of the Duck class and create a new set of classes to represent each behavior.
- Use interface to represent each behavior, *FlyBehavior* and *QuackBehavior*. The Duck subclasses will use a behavior represented by an interface, so that the actual implementation of the behavior won't be locked into the Duck subclass.
- Each Duck will *delegate* its flying and quacking behavior. Instead of inheriting its behavior, it gets its behavior by being composed by the right behavior object. Using Composition gives more flexibility, such as it can change behavior at runtime. 

[gist:id=227649a29eb478234c12,file=strategy-pattern.java]

### Observer Design Pattern

The **Observer Pattern** defines a one-to-many dependency between objects so that when one object changes state, al of its dependents are notified and updated automatically.