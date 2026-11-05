# Use cases

- **Conflicting papers:** one benchmark uses warm cache and another cold cache. Record the mismatch; propose a paired run with both states rather than averaging the results.
- **Offline design:** supplied ADRs show one retry policy. Document whether the provider's dedupe window is unknown, prepare a primary-source lookup, and propose an isolated replay before adoption.
