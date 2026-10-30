# Operational runbook

These are reusable procedures derived from the lab, not remote commands for the original environment.

## Before a network or proxy change

1. Record the request, owner, scope, dependencies and expected impact.
2. Capture the current configuration in restricted storage, outside Git if it includes secrets.
3. Confirm a physical-console or alternate management path.
4. Prepare rollback and a verification checklist before applying the change.
5. Change one layer at a time; do not simultaneously alter routing, DNS, TLS and authentication without checkpoints.

## Troubleshooting sequence

| Layer | Check | What a pass does not prove |
|---|---|---|
| Physical | Cable, carrier, speed/duplex, PoE where applicable | Correct VLAN or IP |
| Switching | Port mode, VLAN membership, forwarding state, MAC table | Correct routing |
| Addressing | IP/prefix, duplicate ownership, gateway, ARP | Application availability |
| Routing | Selected route and return path | Name resolution |
| DNS | Answer from intended resolver | Destination service health |
| Transport | Authorized TCP connection test | TLS trust |
| TLS | CA chain, hostname and expiry | Successful application login |
| Application | Authenticated action and authorization | Collection/backup coverage |

A failed ping does not establish that an address is unassigned. Check ARP, allocations,
DHCP leases/reservations and potential offline owners before allocating it.

## After a change

- Test from the intended user zone as well as an administrator's zone.
- Confirm unauthorized paths remain denied.
- Verify backend trust, not just the browser padlock.
- For group policy, inspect the resulting policy and target certificate store.
- For monitoring, generate an approved test event and verify receipt and timestamps.
- Record what was observed, what remains unverified, rollback availability and whether persistence was authorized.

## Recovery checklist

1. Define what is being recovered: host configuration, guest, database, file store or vault.
2. Use an application-consistent backup, not an arbitrary copy of a running database.
3. Retain decryption keys independently of the failed host.
4. Restore to an isolated environment first.
5. Validate integrity, application login and authorization before declaring recovery.
6. State recovery time/data-loss observations only after measuring a real exercise.

## Evidence template

```text
Change:
Operator / reviewer:
Scope and authorization:
Pre-change state:
Rollback path:
Actions:
Verification from each relevant zone:
Denied-path checks:
Remaining uncertainties:
Persistence/backup status:
```
