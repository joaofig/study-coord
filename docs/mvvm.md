# MVVM

This document describes the interpretation of the MVVM (Model-View-ViewModel) design pattern in the context of this project. 
MVVM is a software architectural pattern that facilitates the separation for the development of the graphical user interface (the view) from the business logic or back-end logic (the model).
This separation allows for a more modular and testable codebase.


## Views

A view contains the visual elements of the application and is responsible for displaying data to the user.
All user interface elements in this project are implemented using NiceGUI (nicegui.io).
Views are designed to be as simple as possible, focusing solely on the presentation layer.
Each view knows about its corresponding ViewModel, which provides the data and commands needed for the view to function.
The view binds to properties and commands exposed by the ViewModel, allowing for a clean separation of concerns.
Any attached view model is handled in an abstract fashion, allowing for easy swapping of view models without modifying the view itself.

All views must derive from the `View` base class.

## ViewModels

A ViewModel is responsible for managing the data and business logic of the application.
It acts as an intermediary between the view and the model, providing the necessary data and commands for the view to function.
ViewModels are typically implemented as Python classes and are responsible for handling user interactions and updating the view accordingly.
They expose properties and commands that the view can bind to, ensuring a clear separation of concerns between the presentation and business logic layers.

All view models must derive from the `ViewModel` base class.

## Models

A model represents the data and business logic of the application.
It is responsible for managing the state of the application and providing methods for data manipulation and retrieval.
Models are typically implemented as Python classes and can be designed to interact with databases, APIs, or other data sources.
They encapsulate the core functionality of the application and provide a clean interface for the ViewModel to interact with, ensuring that the business logic is decoupled from the presentation layer.
