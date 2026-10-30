# Engineering case studies

These summaries describe recorded lab work, not production incidents or a fresh audit. Addresses, credentials and personal details are omitted.

## Commissioning a tagged-management hypervisor

**Problem:** a freshly installed Proxmox host initially placed its management address on an untagged bridge, while the intended switch uplink carried management as a tagged VLAN.

**Approach:** identify the actual physical NIC; back up the network configuration; make the base bridge VLAN-aware without an IP; move management to a VLAN subinterface; apply from the physical console. Keep the unused secondary NIC unchanged.

**Verification:** inspect switch access/trunk mode, native VLAN, allowed VLANs, active VLANs, spanning-tree forwarding and the learned host MAC. Then validate ARP, ICMP, SSH and the web endpoint separately.

**Recorded result:** the uplink negotiated full-duplex gigabit operation, the host MAC appeared on the correct management VLAN, SSH authenticated and the private-CA-backed management endpoint returned HTTP 200. No guest routers existed at that time.

**Lesson:** a configuration file that looks correct is not proof of the cable, VLAN state or application path. Physical-console access is an important rollback tool during management-plane changes.

## Turning private services into named HTTPS endpoints

**Problem:** applications were reached by IP and nonstandard ports, with inconsistent client trust and per-device routing friction.

**Approach:** use a private DNS facade and host-based NGINX routing. Issue a frontend service certificate from the existing lab CA; preserve restricted access; verify the backend's certificate and expected hostname. Extend certificate renewal checks when adding a new service.

**Verification:** test name resolution, CA-validated HTTPS from an approved client, and backend trust. Keep direct-backend certificate behavior distinct from proxy-hostname behavior.

**Recorded result:** selected administrative services, including the satellite hypervisor frontend, returned successful trusted HTTPS responses through the remote-admin path. LAN DNS for some newly added endpoints still required confirmation.

**Lesson:** DNS resolution, TCP reachability, certificate validation and application authentication are four different tests. A reverse proxy does not replace routing or authorization.

## Diagnosing a missing Windows trust policy

**Problem:** the workstation reported successful `gpupdate`, but the expected CA certificate was absent.

**Approach:** inspect the actual certificate store, applied policies, GPO existence and computer distinguished name rather than assuming policy processing meant the desired policy applied.

**Finding:** the expected GPO did not exist, and the newly joined workstation was in the default Computers container. The domain controller did not yet have the lab trust anchor either.

**Status:** a domain-wide certificate-trust deployment script was prepared at the administrator's request. Successful execution and client trust remained unconfirmed.

**Lesson:** policy refresh success is not policy-content verification; group policy scope follows AD objects, not the client VLAN number.

## Source control and shared administration

**Problem:** scripts and configuration history needed different handling from documents, diagrams and browser uploads.

**Approach:** deploy Forgejo for private repositories and Nextcloud for shared files. Create individual application accounts, a private organization/group, persistent storage and restricted registration. Bind container web ports to loopback and place access restrictions at the TLS entry point.

**Verification:** verify authenticated repository visibility and shared-file readback as each administrator, not just the instance owner.

**Recorded result:** all three intended administrators could access their shared resources. Backup scheduling for these new services remained a follow-up item.

**Lesson:** successful deployment includes authorization checks and recovery ownership, not just a responding login page.

## Learning from recovery boundaries

**Work:** capture a baseline of existing VMs and verify an encrypted Vaultwarden backup copy on a separate Windows server using integrity and restore checks.

**Limit:** the baseline did not include services created afterward; automated off-host copies and protected off-host recovery-key custody were not complete.

**Lesson:** snapshots, backup archives, a recoverable database and possession of the decryption key are separate requirements. Documenting a known gap is safer than labeling the environment fully backed up.
