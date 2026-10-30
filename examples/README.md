# Sanitized configuration references

These small examples illustrate patterns used in the lab. They are reconstructed
documentation templates, not complete live configurations or a turnkey deployment.
Use only in an environment you own or are authorized to administer.

| Example | Demonstrates | Required adaptation |
|---|---|---|
| proxmox/interfaces.example | Tagged management on a VLAN-aware Linux bridge | NIC, address allocation, switch trunk and console rollback |
| cisco/satellite-uplink.example | Restricted allowed VLANs and unused native VLAN | Actual interface, VLAN creation, routing, platform syntax and authorized persistence |
| nginx/private-service.conf.example | Separate frontend and backend TLS validation | Real certificates, CA trust, authentication, network ACLs and upstream name |
| monitoring/prometheus.yml.example | A single explicit local scrape target | Exporter install, bind address, authorization, TLS and retention |

All example IPv4 addresses come from documentation-only ranges and are not globally
routable service endpoints. Test syntax and behavior on your actual software versions.
The NGINX example is parse-tested in an isolated container by CI, not deployed by CI.

Never copy a CA private key, password export or unredacted running configuration into Git.
