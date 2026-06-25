# Repositories

A repository is a class that encapsulates the logic required to access data sources.
It centralizes common data access functionality, providing better maintainability and decoupling the infrastructure or technology used to access databases from the domain model layer.

A repository has no concept of existing models or view-models.
It is only concerned with persisting and retrieving data from the data source.
As such, it is not responsible for any business logic or validation.
Also, it communicates the application components using Python dictionaries.
These must later be converted to models or view-models by the application layer.