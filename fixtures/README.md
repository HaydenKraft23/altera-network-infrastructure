# Offline fixtures

- `inventory.json`: four fictional devices in documentation-only address blocks.
- `telemetry.json`: 192 deterministic synthetic observations, 96 per relay,
  retained from an original Altera training exercise. The first relay has eight
  injected degraded samples; the second remains nominal in the model.

The timestamps identify a fictional exercise, not collection from live equipment.
There are no customer records, credentials, real host addresses or RF observations.
The fixture does not simulate physical interplanetary light-time or prove redundancy.

Missing or malformed records are rejected by the analyzer; it does not silently
replace missing measurements with zero or claim absent data means a healthy link.
