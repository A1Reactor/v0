# ADR 002: Deterministic artifact caching

## Context
We need a pragmatic path to iterate quickly while keeping the system testable and swappable.

## Decision
We implement **Deterministic artifact caching** as a first-class concern.

## Consequences
- Easier debugging and reproducibility
- Slightly more boilerplate up front
- Cleaner integration points for future providers/UI
