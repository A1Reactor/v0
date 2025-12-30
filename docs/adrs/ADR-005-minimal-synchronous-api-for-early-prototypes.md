# ADR 005: Minimal synchronous API for early prototypes

## Context
We need a pragmatic path to iterate quickly while keeping the system testable and swappable.

## Decision
We implement **Minimal synchronous API for early prototypes** as a first-class concern.

## Consequences
- Easier debugging and reproducibility
- Slightly more boilerplate up front
- Cleaner integration points for future providers/UI
