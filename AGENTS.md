# AGENTS.md

## Project overview
- Language: Python
- Build tool: uv
- Database: SQLite
- User interface: nicegui (https://nicegui.io/documentation)

## Repository structure
- All code is in the `src` directory
- All tests are in the `tests` directory
- All documentation is in the `docs` directory
- `src/db` contains the database-related code and models
- `src/models` contains the data models (data classes)
- `src/views` contains the views and controllers

## Common tasks
- Run tests: `uv run pytest`

## Definition of done
- All tests pass
- New code includes tests
- No build warnings
- Code is well-documented
- Code is formatted
- Code is linted
- Code is covered by tests
- Code is covered by static analysis
- Code is free of security vulnerabilities
- Code is free of technical debt
- Code is free of anti-patterns
- Code is free of code smells
- Code is free of performance issues
- Code is free of complexity issues
- Code is free of coupling issues

<!-- code-review-graph MCP tools -->
## MCP Tools: code-review-graph

**IMPORTANT: This project has a knowledge graph. ALWAYS use the
code-review-graph MCP tools BEFORE using Grep/Glob/Read to explore
the codebase.** The graph is faster, cheaper (fewer tokens), and gives
you structural context (callers, dependents, test coverage) that file
scanning cannot.

### When to use graph tools FIRST

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of Grep
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to Grep/Glob/Read **only** when the graph doesn't cover what you need.

### Key Tools

| Tool | Use when |
| ------ | ---------- |
| `detect_changes` | Reviewing code changes — gives risk-scored analysis |
| `get_review_context` | Need source snippets for review — token-efficient |
| `get_impact_radius` | Understanding blast radius of a change |
| `get_affected_flows` | Finding which execution paths are impacted |
| `query_graph` | Tracing callers, callees, imports, tests, dependencies |
| `semantic_search_nodes` | Finding functions/classes by name or keyword |
| `get_architecture_overview` | Understanding high-level codebase structure |
| `refactor_tool` | Planning renames, finding dead code |

### Workflow

1. The graph auto-updates on file changes (via hooks).
2. Use `detect_changes` for code review.
3. Use `get_affected_flows` to understand impact.
4. Use `query_graph` pattern="tests_for" to check coverage.
