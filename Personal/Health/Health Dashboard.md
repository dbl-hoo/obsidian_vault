# Health Dashboard

A self-hosted health monitoring system running on a Proxmox homelab. It pulls data from four sources, stores it in two databases, visualizes everything in Grafana, and can generate a PDF report suitable for doctor visits.

---

## Infrastructure

| Component | Details |
|---|---|
| **Proxmox host** | hyperion (OptiPlex 7070) — `ssh root@10.10.10.3` |
| **App server** | dathomir — LXC container 103 — `ssh root@10.10.10.36` |
| **Repo** | `git@github.com:dbl-hoo/health-dashboard.git` |
| **App directory** | `/opt/health-dashboard` on dathomir |

All services run as Docker Compose containers on dathomir.

---

## Data Sources

### Dexcom Stelo (CGM)
The Stelo does not support Dexcom Share, so data flows through **Zukka** on the iPhone. Zukka reads directly from the Stelo app and uploads to Nightscout every 5 minutes. No bridge plugin is involved server-side.

### Oura Ring
A Python poller (`oura-poller`) runs continuously on dathomir and calls the Oura API v2 daily at 11am. On startup it backfills 90 days of history automatically. Pulls: sleep architecture, HRV, resting heart rate, readiness, SpO2, stress, activity, resilience.

### Withings Body Smart Scale
Data arrives via Withings webhooks. When you step on the scale, Withings calls the health-api, which fetches the full measurement and writes it to InfluxDB. Captured metrics: weight, body fat %, fat-free mass, muscle mass, bone mass, hydration (kg), visceral fat index.

### Withings BPM
Same webhook flow as the scale. Captures systolic, diastolic, and pulse at time of measurement.

### Apple Health (Health Auto Export)
The Health Auto Export app on iPhone sends a webhook to health-api whenever new data is available. Captures: weight, body fat %, lean mass, heart rate, HRV, blood pressure, steps, active energy.

---

## Services

| Service | Port | Purpose |
|---|---|---|
| **nightscout** | 1337 | CGM web UI, receives Zukka uploads, Pushover alerts |
| **mongo** | — | Nightscout's data store |
| **influxdb** | 8086 | Time-series store for all non-CGM data |
| **grafana** | 3000 | Unified dashboard across all sources |
| **health-api** | 8090 | FastAPI: Withings webhooks + Apple Health webhooks |
| **oura-poller** | — | Daily Oura API polling |

External access is via Cloudflare Tunnels (configured separately):
- `https://health.kirkham.cloud` → Grafana
- `https://nightscout.kirkham.cloud` → Nightscout
- `https://health-api.kirkham.cloud` → health-api (required for Withings webhooks)

---

## Databases

**MongoDB** (`nightscout` database)
- `entries` collection — CGM readings (SGV, timestamp)

**InfluxDB** (org: `homelab`)
- `oura_data` bucket — all Oura Ring data
- `health_metrics` bucket — Withings + Apple Health data

---

## Grafana Dashboard

Visit `http://10.10.10.36:3000` (or via Cloudflare tunnel). Dashboard: **Health Dashboard**.

Current panels:
- Glucose (CGM, from MongoDB)
- Weight, Body Fat %, Lean Body Mass, Muscle Mass, Bone Mass, Hydration, Visceral Fat Index
- Blood Pressure
- HRV (daily avg, Apple Health + Oura)
- Resting HR
- Sleep Score, Sleep Architecture, SpO2
- Readiness Score, Steps

---

## Doctor Report

A Python script that queries all three data sources and generates a multi-page PDF.

**Sections in the report:**
1. Cover page (name, date range)
2. CGM summary — mean glucose, std dev, CV%, estimated A1C (GMI), time-in-range breakdown, Ambulatory Glucose Profile (AGP) chart
3. Sleep & Recovery — avg duration, efficiency, sleep score, sleep architecture chart, HRV trend with 7-day rolling average, resting HR, SpO2
4. Blood Pressure — avg/min/max, trend chart with AHA threshold lines
5. Weight & Body Composition — current weight, change over period, body fat %, muscle mass, visceral fat index, hydration, bone mass
6. Activity — avg daily steps, active calories, readiness score trend
7. Notes (optional free text)

### Generating a Report

SSH into dathomir, then:

```bash
cd /opt/health-dashboard/report

# 90-day report (typical for quarterly doctor visit)
./report.sh --name "Jason" --days 90 --output ~/report.pdf

# With clinical notes
./report.sh --name "Jason" --days 90 \
  --notes "Started lisinopril 5mg on March 1. BP trending down." \
  --output ~/report.pdf

# Shorter window
./report.sh --name "Jason" --days 30 --output ~/report.pdf
```

Copy to local machine (run on bespin, not dathomir):

```bash
scp root@10.10.10.36:~/report.pdf .
```

The script automatically reads credentials from `/opt/health-dashboard/.env` — no need to pass tokens manually.

---

## Operations

### Restart a service
```bash
ssh root@10.10.10.36
cd /opt/health-dashboard
docker compose restart <service>   # e.g. grafana, oura-poller
```

### View logs
```bash
docker compose logs -f oura-poller
docker compose logs -f health-api
```

### Deploy a code change
```bash
# From bespin (local machine), after pushing to git:
ssh root@10.10.10.36 "cd /opt/health-dashboard && git pull && docker compose build <service> && docker compose up -d <service>"
```

### Manually backfill Withings data
```bash
API_TOKEN=$(grep API_AUTH_TOKEN /opt/health-dashboard/.env | cut -d= -f2)
curl -X POST "http://localhost:8090/api/v1/withings/backfill?days=90" \
  -H "Authorization: Bearer $API_TOKEN"
```

### Re-authorize Withings (if tokens expire)
Visit `https://health-api.kirkham.cloud/api/v1/withings/auth` in a browser. Completes OAuth2 flow and re-subscribes webhooks automatically.

---

## Alerts

Nightscout handles all CGM alerts and sends them via Pushover:
- BG High: > 180 mg/dL
- BG Low: < 55 mg/dL
- Target range: 70–140 mg/dL

Grafana alerting for BP and weight staleness is configured separately in the Grafana UI.
