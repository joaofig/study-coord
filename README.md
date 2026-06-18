# study-coord

Research study coordination manager.

## Overview

`study-coord` is a Python-based application designed to help manage and coordinate research studies. It provides a user-friendly interface for tracking studies, researchers, and participants.

## Features

- **Study Management**: View and add study details including name, sponsor, and dates.
- **Researcher Management**: Track the team of researchers.
- **Extensible Architecture**: Structured with repositories and SQL scripts for easy expansion to visits, patients, and adverse events.
- **Integrated Database**: Uses SQLite for lightweight, local data storage.

## Tech Stack

- **Language**: Python 3.14+
- **UI Framework**: [NiceGUI](https://nicegui.io/)
- **Data Grid**: AgGrid (via NiceGUI)
- **Database**: SQLite
- **Build Tool**: [uv](https://github.com/astral-sh/uv)

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
  - `db/`: Database models, repositories, and SQL scripts
  - `models/`: Core data models (dataclasses)
  - `views/`: UI components and page layouts (NiceGUI)
  - `tools/`: Utility functions and classes
- `main.py`: Application entry point
- `study-coord.toml`: Database configuration
- `AGENTS.md`: Development guidelines and project rules

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
