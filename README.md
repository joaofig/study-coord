# study-coord

Research study coordination manager.

## Overview

`study-coord` is a Python-based application designed to help manage and coordinate research studies. It provides a user-friendly interface for tracking studies, researchers, and participants using a clean MVVM architecture.

## Features

- **Study Management**: Comprehensive tracking of study information including name, sponsor, dates, and comments. Now includes **Protocol Deviation** and **Monitoring Visit** tracking.
- **Researcher Management**: Manage teams of researchers with role-based details and contact information.
- **Patient Management**: Comprehensive tracking of participants with dedicated sub-grids for **Visits** and **Adverse Events** (Clinical Events).
- **Global Dashboard**: Real-time summary of studies, patients, researchers, visits, and events across the entire project or per-study metrics.
- **User & Admin Management**: Robust **Role-Based Access Control (RBAC)** with a dedicated admin interface for managing users and roles.
- **Security**: Secure authentication with password hashing and automatic **inactivity session timeout** for enhanced data protection.
- **Data Export**: Built-in support for exporting study data, monitoring logs, user lists, and event records to **Excel** for external reporting and analysis.
- **Interactive UI**: Data-rich interface powered by NiceGUI and AgGrid with flexible layouts, splitters, and dynamic data binding for efficient data navigation.
- **Clean Architecture**: Strictly follows the **MVVM** (Model-View-ViewModel) and **Repository** patterns, utilizing asynchronous database operations and externalized SQL scripts.
- **Developer Guides**: Comprehensive "Agent Skills" documentation for consistent implementation of new features.
- **Knowledge Graph**: Integrated with `code-review-graph` for advanced code analysis and structural insights.

## Tech Stack

- **Language**: Python 3.14+
- **UI Framework**: [NiceGUI](https://nicegui.io/) (3.14.0+)
- **Data Grid**: AgGrid (via NiceGUI)
- **Database**: [Supabase](https://supabase.com/) (PostgreSQL)
- **Build Tool**: [uv](https://github.com/astral-sh/uv)
- **Deployment**: [Fly.io](https://fly.io/)
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

The application uses environment variables for configuration. You can create an `.env` file in the root directory:

```env
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-anon-key
```

### Running the Application

To start the application, run:

```bash
uv run python app/main.py
```

The web interface will typically be available at `http://localhost:8080`.

## Project Structure

- `app/`: Main application directory
  - `src/`: Main source code
    - `dtos/`: Data Transfer Objects for type-safe data handling
    - `models/`: Core data models
    - `repositories/`: Supabase repository implementations
    - `viewmodels/`: ViewModels handling logic and state (MVVM)
    - `views/`: UI components and layouts (NiceGUI)
    - `db/`: Legacy SQLite database configuration and repositories
    - `tools/`: Utility functions (Excel export, messaging, etc.)
  - `tests/`: Automated test suite
  - `images/`: Application assets and icons
  - `main.py`: Application entry point
- `docs/`: Project documentation (Architecture, Schema, Messaging)
- `supabase/`: SQL schema and migrations for Supabase
- `AGENTS.md`: Development guidelines and project rules
- `Dockerfile`: Container configuration
- `fly.toml`: Fly.io deployment configuration

## Knowledge Graph

This project uses `code-review-graph` to maintain a structural understanding of the codebase. It helps in:
- Identifying impact radius of changes.
- Detecting architectural patterns and anti-patterns.
- Providing context-aware code reviews.

Refer to `AGENTS.md` for more details on using graph tools.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
