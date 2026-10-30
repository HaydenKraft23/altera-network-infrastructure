# Security decisions and limitations

## Controls used in the lab

- Segmented user, service, identity, monitoring, management and transport roles.
- Restricted private administrative access rather than public port forwarding.
- Private DNS names and a lab CA for client-to-proxy TLS.
- Explicit backend certificate and hostname verification at the proxy.
- Secure session cookies, origin/CSRF checks and rate limiting in the internal Flask application.
- Separate individual accounts in collaboration applications; private repositories and disabled public registration/sharing where configured.
- Loopback-published container ports behind a controlled entry point; no direct database/Redis publication in the collaboration deployment.
- Encrypted recovery material and restricted operational records, with unresolved key-custody work documented.

These are targeted controls, not evidence that every host or firewall path was exhaustively audited.

## Lab shortcuts not suitable for production

Some original lab accounts used shared setup passwords, and the internal admin portal included a requested plaintext credential register. Those are limitations, not recommended patterns. This repository includes neither the register nor its export code.

For a production-oriented redesign:

1. Rotate shared credentials to unique secrets, require individual accounts and use MFA where supported.
2. Store and share secrets through a dedicated vault; remove plaintext credential pages.
3. Separate the remote-access gateway from CA signing and proxy responsibilities where practical.
4. Protect CA and backup recovery keys outside the main failure domain.
5. Separate public-style company content from administrative applications before introducing a DMZ.
6. Restore camera isolation after onboarding; a temporary management-zone exception is not a hardened IoT design.
7. Reconcile subnet-mask drift and maintain authoritative addressing and DHCP reservations.
8. Validate central log delivery with controlled test events, then establish retention and alert ownership.

## Publication boundary

The repository uses documentation-only IP ranges and example hostnames. It intentionally omits real addresses, overlay identifiers, host fingerprints, internal usernames, CA certificates, operational logs, passwords and restricted documents.

The local checker detects common mistakes but is not a complete secret detector. Manual review and an independent scanner remain necessary before making the repository public.
