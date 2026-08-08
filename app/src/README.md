# Developer Guide: `app/src`

This directory contains the core application logic and user interface for the Study Coordinator application. The project follows a modular architecture based on the **Model-View-ViewModel (MVVM)** pattern, ensuring a clean separation of concerns between data, business logic, and presentation.

## Directory Structure Overview

### [models/](./models)
Domain-level service classes. Models in this application act as an orchestration layer between the ViewModels and the Repositories. They encapsulate business rules and provide a clean API for data operations, often wrapping Repository calls with additional logic (e.g., `TimelineModel` aggregates data from multiple sources).

### [viewmodels/](./viewmodels)
The bridge between Models and Views. ViewModels manage the state of the UI and handle user interactions. They are typically implemented as bindable classes (using NiceGUI's binding system) to allow the View to reflect state changes automatically.
- **Key Class**: `ViewModel` (base class providing messaging and property access).
- **Naming Convention**: `*_list.py` for collection management, `*.py` for individual entity management.

### [views/](./views)
The presentation layer, built with **NiceGUI**. This directory contains the definitions for pages, panels, grids, and dialogs.
- **`main.py`**: The entry point for the NiceGUI application.
- **`dialogs/`**: Reusable modal components for data entry and confirmation.
- **`*_grid.py`**: Components specialized in displaying data in tabular format (using AG Grid).
- **`*_panel.py`**: UI components for specific application sections.

### [repositories/](./repositories)
The data access layer (DAL). It abstracts the underlying storage mechanisms using the Repository pattern.
- **`postgres/`**: Direct PostgreSQL implementation using standard SQL queries.
- **`supabase/`**: Implementation for Supabase, leveraging its client library for data operations.
- **`base.py`**: Abstract base classes defining the repository interface.

### [dtos/](./dtos)
Data Transfer Objects (DTOs) used for type-safe data exchange across application layers. They are primarily responsible for serialization and deserialization (e.g., to/from dictionaries or database records) and often contain validation helpers.

### [tools/](./tools)
Shared infrastructure and utility modules. This includes:
- **`bindable.py`**: Utilities for NiceGUI data binding.
- **`messenger.py`**: A lightweight pub/sub system for inter-component communication.
- **`validation.py`**: Common validation logic for DTOs and ViewModels.
- **`singleton.py`**: Utility for enforcing singleton patterns on service classes.
- **`observability.py`**: Helpers for logging and monitoring.

## Architectural Patterns

### MVVM Implementation
The application leverages NiceGUI's reactive binding. ViewModels expose properties that Views bind to. When a property in the ViewModel changes, the UI updates automatically. Components often use the `@binding.bindable_dataclass` decorator.

### Messaging System
To maintain loose coupling, components communicate via the `messenger` tool. This allows one component (like a ViewModel) to notify others (like a List View) to refresh their state without direct references. Messages are sent using `broadcast` or `send_message`.

### Data Flow
1. **View** captures user input and calls methods on the **ViewModel**.
2. **ViewModel** validates input and calls the **Model**.
3. **Model** interacts with the **Repository** to persist or retrieve **DTOs**.
4. **ViewModel** updates its bindable properties based on the result.
5. **View** reflects the changes automatically via data binding.
