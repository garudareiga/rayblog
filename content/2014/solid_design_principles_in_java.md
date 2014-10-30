Title: SOLID Design Principles in Java
Date: 2014-10-28 16:00 
Author: Ray Chen 
Category: Java

A summary of SOLID design principles of OOP in Java.

+ S: Single Responsibility Principle
+ O: Open Closed Principle
+ L: Liskov Substitution Principle
+ I: Interface Segregation Principle
+ D: Dependency Inversion Principle

### Single Responsibility Principle - Classes should change for only a single reason
Key Points:

+ The responsibility of a class is the only reason for the class to change.
+ If a class has more than one responsibility, then responsibilities become coupled. Changes to one responsibility may impact other responsibilities. The class should be broken up into smaller components.
+ This principle promotes cohesion of software components.

[gist:id=df9f7250c484983a584c,file=single-responsibility-principle.java]

### Open Closed Principle - Classes should open for extension but closed to modification
Key Points:

+ This principle enables us to add features without modifying the existing components.
+ Java supports this through extending parent classes and implementing of interfaces.
+ Instead of modifying the parent class which is more abstract consider creating a sub class with the more specific attributes and methods.

[gist:id=df9f7250c484983a584c,file=open-closed-principle.java]

### Liskov Substitution Principle - Objects in a program should be replaceable with instances of their sub types without altering the correctness of that program
Key Points:

+ Care must be taken to ensure that a class hierarchy does not violate this principle.
+ Any subclass fullfills the IS-A contract with its parent class may or may not fullfill this principle.

[gist:id=df9f7250c484983a584c,file=liskov-substitution-principle.java]

### Interface Segregation Principle - Many specific interfaces are better than a single generic interface
Key Points:

+ Larger Java interfaces should be broken down into smaller and more specific ones.
+ A client should never be made to depend on methods it does not use.
+ Adherence to this principle reduces the change footprint in the system when interfaces are modified.

[gist:id=df9f7250c484983a584c,file=interface-segregation-principle.java]

### Dependency Inversion Principle - Depend on abstraction not on concretions
Key Points:

+ High-level modules should not depend on low-level modules. Both should depend on abstractions.
+ Abstractions should not depend on details. Details should depend upon abstractions.

[gist:id=df9f7250c484983a584c,file=dependency-inversion-rinciple.java]