# study-coord

Research study coordination manager.

## Overview

`study-coord` is a Python-based application designed to help manage and coordinate research studies. It provides a user-friendly interface for tracking studies, researchers, and participants using a clean MVVM architecture.

## Features

- **Study Management**: Detailed tracking of study information including name, sponsor, dates, protocol visits, and comments.
- **Researcher Management**: Manage the team of researchers associated with each study with role-based details.
- **Patient Management**: Comprehensive tracking of participants in studies with dedicated grids and dialogs.
- **Visit & Event Tracking**: Log and manage study visits and clinical events with patient-specific history.
- **Monitoring Reports**: Track monitoring activities and documentation for study compliance.
- **Interactive UI**: Data-rich interface powered by NiceGUI and AgGrid for efficient data management.
- **Clean Architecture**: Follows MVVM (Model-View-ViewModel) pattern and Repository pattern for better maintainability and testability.
- **Developer Guides**: Comprehensive "Agent Skills" documentation for consistent implementation of new features.
- **Knowledge Graph**: Integrated with `code-review-graph` for advanced code analysis and structural insights.

## Tech Stack

- **Language**: Python 3.14+
- **UI Framework**: [NiceGUI](https://nicegui.io/)
- **Data Grid**: AgGrid (via NiceGUI)
- **Database**: SQLite
- **Build Tool**: [uv](https://github.com/astral-sh/uv)
- **Code Analysis**: [code-review-graph](https://github.com/astral-sh/code-review-graph)

## Getting Started

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/study-coord.git
   cd study-coord
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

### Configuration

The application uses a configuration file named `study-coord.toml` in the root directory for database settings.

```toml
[database]
path = "./study-coord.db"
```

### Running the Application

To start the application, run:

```bash
uv run python main.py
```

The web interface will typically be available at `http://localhost:8080`.

## Project Structure

- `src/`: Main source code
  - `db/`: Database configuration, repositories, and SQL scripts
  - `models/`: Core data models (dataclasses)
  - `viewmodels/`: ViewModels handling logic and state (MVVM)
  - `views/`: UI components and layouts (NiceGUI)
  - `tools/`: Utility functions, observability, and infrastructure
- `tests/`: Automated tests
- `docs/`: Project documentation and architecture overviews
- `ref/`: Reference materials and Agent Skills for development patterns
- `main.py`: Application entry point
- `study-coord.toml`: Database configuration
- `AGENTS.md`: Development guidelines and project rules

## Knowledge Graph

This project uses `code-review-graph` to maintain a structural understanding of the codebase. It helps in:
- Identifying impact radius of changes.
- Detecting architectural patterns and anti-patterns.
- Providing context-aware code reviews.

Refer to `AGENTS.md` for more details on using graph tools.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
