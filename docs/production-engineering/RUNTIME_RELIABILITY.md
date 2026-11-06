# Runtime reliability

The durable advisor consumes checkpoint status from the original SQLite journal. An in-flight claim remains subject to reconciliation even after deadline. The separate SQLite demo simulates interruption before and after a local effect across subprocesses. After an effect, restart records a verified receipt without creating another row; before it, restart records no effect before a new claim.

The revision-loop fixture preserves a verified score of .76 even when an unverified candidate scores .98; the remaining budget stops another iteration. Trace tests distinguish three failed calls with unchanged state from progress and preserve the difference between a textual success and observed failure. No remote provider, Temporal cluster or production replay was exercised.
