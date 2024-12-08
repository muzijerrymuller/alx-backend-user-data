This project would teach you several key skills related to backend development, databases, and authentication processes:

SQLAlchemy and Database Modeling:

You will learn how to use SQLAlchemy, a powerful ORM (Object Relational Mapper) library for Python, to interact with databases. By defining models like User, you'll understand how to map Python classes to database tables and perform CRUD operations (Create, Read, Update, Delete).
Specifically, tasks such as creating a User model, interacting with the database through a DB class, and utilizing SQLAlchemy's session and query mechanisms will enhance your skills in backend architecture.
Database Operations:

Through tasks like adding, finding, and updating a user, you'll practice how to handle database transactions, ensuring data integrity and efficient queries.
You'll learn to deal with common exceptions like NoResultFound and InvalidRequestError, which helps in writing robust and error-resilient database code.
User Authentication:

The implementation of a password hashing mechanism using bcrypt will give you a solid understanding of how to securely store passwords in databases.
You'll learn how to handle user registration, ensuring unique emails and securely storing passwords, which is a common challenge in user authentication systems.
Error Handling:

The tasks emphasize proper exception handling. You’ll learn how to raise and handle exceptions like ValueError when validation fails (e.g., user already exists), ensuring a smooth and predictable experience for users of your system.
Class Design and Property Encapsulation:

By working with the Auth and DB classes, you'll practice principles like encapsulation and property management. Understanding how to structure classes and define private properties (_session), while still allowing access through controlled methods (like add_user), is important for designing maintainable and scalable code.
Integration of Multiple Components:

This project teaches you to integrate different components, such as a database interface (DB class), user authentication logic (Auth class), and password hashing into a complete working system.
You'll also gain experience in modular programming by splitting functionality into different files (e.g., auth.py, db.py, user.py) while maintaining clear responsibility boundaries between components.
