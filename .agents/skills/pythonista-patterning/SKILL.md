---
name: pythonista-patterning
description: Use when writing new code, implementing features, or refactoring. Triggers on "pattern", "reuse", "duplicate", "extract", "helper", "refactor", "architecture", "DRY", "don't repeat yourself", "abstract", "reusable", "similar", "existing code", or when about to write new functionality.
---

# Pattern Discovery and Code Reuse

## Core Philosophy

**Before writing ANY new code, actively search for existing patterns and reuse opportunities.**

Duplicating code with subtle variations is one of the most damaging things you can do to a codebase.

## Pattern Discovery Workflow

### 1. Search for Similar Implementations

```bash
# In Claude Code, use the Grep tool instead of bash grep:
# pattern="similar_function" path="src/"

# Check sibling files in same directory
ls src/services/

# Look at parallel structures
# If writing campaign_api.py, check drip_api.py, prompt_api.py
```

### 2. Document Patterns Found

- Note the common structure/approach
- Identify what varies vs what stays the same
- List helper functions or utilities used

### 3. Follow Established Patterns Exactly

- Use the same parameter names and types
- Use the same error handling approach
- Use the same validation strategy

### 4. Identify Reuse Opportunities

- Spot duplicated logic that can be extracted
- Find DB queries that appear multiple times
- Notice validation patterns repeated across files

## Balance: Don't Over-Engineer, Don't Under-Engineer

### Under-Engineering (BAD)

```python
# campaign_api.py
async def update_campaign(handle: str, campaign: Campaign):
    if campaign.version == 0:
        current = await collection.find_one({"handle": handle})
        next_version = (current["campaign"]["version"] + 1) if current else 1
        campaign.version = next_version

# drip_api.py - DUPLICATE with subtle variation!
async def update_drip(handle: str, drip: Drip):
    if drip.version == 0:
        current = await collection.find_one({"handle": handle})
        next_version = (current["drip"]["version"] + 1) if current else 1
        drip.version = next_version
```

### Over-Engineering (BAD)

```python
# Creating a generic "VersionedEntityManager" for only 2 entities
class VersionedEntityManager(ABC, Generic[T]):
    # 50+ lines of generic infrastructure for 2 use cases
```

### Right Balance (GOOD)

```python
# Simple, focused helper
async def auto_increment_version(
        collection, handle: str, field_name: str, entity: VersionedEntity
) -> VersionedEntity:
    """Auto-increment version using version=0 sentinel."""
    if entity.version == 0:
        current = await collection.find_one({"handle": handle})
        current_version = current._get_by_id(field_name, {})._get_by_id("version", 0) if current else 0
        entity.version = current_version + 1
    return entity


# Usage
campaign = await auto_increment_version(collection, handle, "campaign", campaign)
drip = await auto_increment_version(collection, handle, "drip", drip)
```

## Simple Helper vs Infrastructure

### Simple Helper - Extract Immediately
- Duplicated calculations
- Repeated DB queries (same query in 3+ places)
- Filtering/validation logic repeated across functions
- **Action**: Extract now, include in current PR

### Infrastructure - Ask First
- Affects how multiple components interact
- Introduces new architectural layer
- **Action**: Ask user, likely separate PR

## Trust the Architecture

**NEVER duplicate validation that already exists in lower layers.**

```python
# WRONG - Service layer blocks API
async def _create_item(self, name, item):
    versions = await api.list_versions(id)  # Checking what API handles!
    if versions:
        raise ValueError(f"Already exists")

# CORRECT - Service layer trusts API
async def _create_item(self, name, item):
    validate_name(name)  # Only validate what service should
    return await api.create_item(item)  # Let API handle versioning
```

## Checklist

Before writing new code:
- [ ] Searched for existing patterns (Grep tool, sibling files)
- [ ] Documented patterns found
- [ ] Following established patterns exactly
- [ ] Identified reuse opportunities
- [ ] Not duplicating validation from lower layers
- [ ] Simple helpers extracted, infrastructure changes discussed

## Related Skills

- [/pythonista-debugging](../pythonista-debugging/SKILL.md) - Root cause analysis
- [/pythonista-testing](../pythonista-testing/SKILL.md) - Testing patterns
- [/pythonista-reviewing](../pythonista-reviewing/SKILL.md) - Code review
- [/pythonista-typing](../pythonista-typing/SKILL.md) - Type patterns
