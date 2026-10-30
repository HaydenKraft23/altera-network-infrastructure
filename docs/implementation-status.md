# Implementation and evidence register

Baseline: retained October 26–28, 2026 lab records. No new live checks were performed to prepare this portfolio. Sanitized artifacts are not substitutes for raw evidence, which remains private.

| Capability | Recorded implementation/evidence | Remaining boundary |
|---|---|---|
| Main Proxmox environment | Application guests deployed and accessed | Not a highly available cluster |
| Satellite hypervisor | Live switch trunk/MAC, management SSH and proxy HTTPS verified | No relay VM deployment at last check |
| DNS and reverse proxy | Selected private names and trusted HTTPS responses verified | New-service LAN DNS records not all confirmed |
| Windows domain | Lab account sign-in on domain-joined workstation confirmed | GPO trust application still unverified |
| Internal mail | Webmail logins, delivery and optional-email contact workflow verified | Internal lab only; no public mail-deliverability claim |
| Forgejo / Nextcloud | Individual authentication and shared-resource readback verified | Scheduled independent backups pending |
| Vaultwarden | Deployed; encrypted backup copy and database recovery checks recorded | No claim that every supplied credential was imported or rotated |
| Prometheus / Grafana | Services available; selected monitoring functions configured | Current target inventory and alert coverage need audit |
| Loki | Service active and listener present | Full source ingestion and retention not established |
| Wazuh | SIEM deployed; domain-controller agent configured | Recent event ingestion and coverage need confirmation |
| Windows Exporter | WinRM listener setup discussed and locally checked | Remote authentication/exporter installation not confirmed |
| IoT | Camera port, PoE and selected browser access verified | Temporary management-VLAN exception requires resolution |
| Recovery | Baseline snapshots; a verified encrypted manual copy | Newer VMs and automated off-host recovery not fully covered |
| Satellite intersite design | Two virtual-router paths proposed | OSPF, IPsec, Site B wiring and failover not verified |
| DMZ / traffic analytics | Design discussion | Not deployed |

## What is reproducible here

- Offline validation of documentation-only inventory addresses and duplicates.
- Analysis of clearly marked synthetic telemetry, including injected degradation.
- Unit tests for expected output and malformed/unsafe inputs.
- A repository publication guardrail and sanitized configuration references.

## What is not asserted

No production SLAs, availability percentages, revenue impact, incident response times,
penetration-test results, compliance certification or measured real satellite performance
are claimed. The project has not established production-grade hardening or disaster recovery.
