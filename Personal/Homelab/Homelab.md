---
project: Homelab
status: Ongoing
area: Home
tags: [personal]
---

# Homelab

Status: Ongoing

## Tasks

## Notes

Area: Home
Related Project: Homelab 
Status: Processed
Type: Reference

# Static IPs

Typology:

| Physical Infrastructure (router, hypervisors) | .1-.10 |  |
| --- | --- | --- |
| Physical devices (NAS, printers) | .11-30 |  |
| Hosts (VMs) | .31-50 |  |
| Services | .51-70 |  |
| Expansion | .71-100 |  |
| DCHP | .101-.199 |  |
| Reserved | .200-.254 |  |


|   |   |   |
|---|---|---|
|Kessel|10.10.10.1|Opnsense hosted on Mustafar|
|Hyperion|10.10.10.3|Promox server used for immich and *arr|
|Jedi_scribe|10.10.10.11|Brother TN803|
|Alderan|10.10.10.12|Synology NAS|
|Dagobah|10.10.10.32|Home Assistant VM|
|Ryloth|10.10.10.33|LXC hosting *arr stack|
|Naboo|10.10.10.34|LXC hosting immich; installed debian; ssh kirkham via key|
|Coruscant|10.10.10.35|LXC hosting actual budget and cloudflared|
|Dathomir|10.10.10.36|LXC host running my health dashboard|

| **Sonarr** | http://10.10.10.33:8989 | 8989 | TV series management |
| --- | --- | --- | --- |
| **Radarr** | http://10.10.10.33:7878 | 7878 | Movie management |
| **Bazarr** | http://10.10.10.33:6767 | 6767 | Subtitles for Sonarr/Radarr |
| **SABnzbd** | http://10.10.10.33:8080 | 8080 | Usenet downloader |
| **Prowlarr** | http://10.10.10.33:9696 | 9696 | Indexer management |
| Overseerr | http://10.10.10.33:5055 | 5055 | Request management |



Link for tunnels:  https://one.dash.cloudflare.com/c0fdec92d83afe69bc272f6d15436bc2/networks/connectors/cloudflare-tunnels/cfd_tunnel/d4938e98-14e6-4c8d-b081-cca6bfdccb50/edit?tab=publicHostname
