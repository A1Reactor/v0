# ADR 010: UI kept static (no build step)

## Context
We need a pragmatic path to iterate quickly while keeping the system testable and swappable.

## Decision
We implement **UI kept static (no build step)** as a first-class concern.

## Consequences
- Easier debugging and reproducibility
- Slightly more boilerplate up front
- Cleaner integration points for future providers/UI
