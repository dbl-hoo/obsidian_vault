# Hermes Agent Project Plan **Decoupled AI-Augmented Second Brain** *Offload heavy lifting to Proxmox • Slack as remote command center • Obsidian + Syncthing workflow*

**Version:** 1.0 **Author:** Grok (xAI) **Date:** April 3, 2026 **Target Completion:** 7–10 days (part-time, evenings) **Status:** Ready to Execute

---

## 1. Project Overview

You are building a **headless Second Brain** that keeps your laptop lightweight (native Obsidian only) while moving all AI processing, metadata extraction, and RAG queries to your existing Proxmox home lab.

**Core Goal:** A 24/7 AI chief-of-staff (Hermes) that: - Reads new/changed notes via Syncthing - Runs nightly EOD structured extraction (dates, parties, legal cites, action items) - Answers any vault query instantly via Slack DMs - Keeps **all** your real-estate/legal data 100% on your own hardware

**Why this wins for you:** - Zero new apps (you already live in Slack + Obsidian) - Office WiFi friendly (Slack is never blocked) - Extremely low cost (~$2–5/month via OpenRouter) - Leverages your Stoic daily-reflection habit and Proxmox/Docker stack

---

## 2. Success Criteria (Definition of Done)

- [x] Hermes answers vault queries accurately from Slack (phone or desktop) while you are at the office - [ ] Nightly EOD job runs automatically, extracts structured metadata, and updates master tracking files - [ ] Syncthing two-way sync works without merge conflicts - [ ] Entire system runs in a single Docker container on Proxmox with auto-restart - [ ] Total monthly AI cost < $5 - [ ] You can ask “@Hermes what’s the closing date for Kirkham?” and get an instant, cited answer ✅ 2026-04-06

---

## 3. High-Level Architecture (The Triad)

1. **The Brain** – Hermes Agent (Docker container on Proxmox) 2. **The Interface** – Slack (DMs only) 3. **The Sync** – Syncthing (mirrors your Obsidian vault in real-time)

---

## 4. Project Phases & Tasks

### Phase 0: Preparation (1–2 hours) - [ ] Confirm Proxmox node has ≥16 GB RAM + 4 cores available for the container - [ ] Create a new directory on your Proxmox host: `/opt/hermes-agent` - [ ] Install Syncthing on Proxmox (if not already running) and share your Obsidian vault folder - [ ] Get your Slack Bot Token and Signing Secret (create a new Slack app) - [ ] Decide on LLM backend: - Option A (recommended start): OpenRouter + Hermes-4 70B (or cheaper 13B for extraction) - Option B: Local quantized 70B via Ollama (if you have GPU)

**Deliverable:** Folder structure created + Slack app ready

### Phase 1: Infrastructure Setup (2–3 hours) - [ ] Create `docker-compose.yml` (I will provide full file) - [ ] Create `.env` with all secrets (Slack tokens, OpenRouter key, paths) - [ ] Set up persistent volumes: - `/data/vault` → mounted to your Syncthing Obsidian folder - `/data/vectorstore` → Chroma/LanceDB for RAG - `/data/logs` - [ ] Deploy the stack with `docker compose up -d` - [ ] Verify container health and auto-restart policy

**Deliverable:** Running empty Hermes container

### Phase 2: Core Agent Development (4–6 hours) - [ ] Implement Slack Bolt Python skeleton (DM listener only) - [ ] Add scheduled EOD job (cron-style inside container, runs at 6 PM your time) - [ ] Build RAG query pipeline: - RecursiveCharacterTextSplitter + embeddings - Vector store (Chroma) - Retrieval + 70B context window for answers - [ ] Structured extraction prompts (JSON output for dates, parties, cites, action items) - [ ] Master tracking file updater (append-only to avoid conflicts)

**Deliverable:** Functional bot that can answer “hello” and run a test EOD pass

### Phase 3: Integration & Polish (3–4 hours) - [ ] Connect Syncthing folder to Hermes container - [ ] Add file-watcher or nightly diff to detect changed notes - [ ] Implement conflict-safe write strategy for master files - [ ] Add Stoic daily reflection template (auto-appended to your journal) - [ ] Health-check endpoint + simple monitoring (UptimeRobot or Proxmox alert)

**Deliverable:** End-to-end workflow working

### Phase 4: Testing & Validation (2–3 hours) - [ ] Add 5–10 real notes from your vault and test EOD extraction - [ ] Test 10 sample Slack queries from your phone on office WiFi - [ ] Simulate laptop offline → server processes → phone query - [ ] Measure cost on first full run

**Deliverable:** All success criteria met

### Phase 5: Go-Live & Iteration (ongoing, 1 hour/week) - [ ] Document your personal prompts in the repo - [ ] Add optional features later: - n8n for advanced workflows - Voice-to-text via phone → Slack - Multi-model routing (cheap model for extraction, 70B for complex queries) - [ ] Monthly cost & accuracy review

---

## 5. Timeline (Realistic for You)

| Phase | Time Estimate | Target Date (start today) | |----------------|---------------|---------------------------| | 0: Preparation | 1–2 hrs | Today | | 1: Infra | 2–3 hrs | Today / Tomorrow | | 2: Core Agent | 4–6 hrs | Tomorrow / Day 3 | | 3: Integration | 3–4 hrs | Day 4 | | 4: Testing | 2–3 hrs | Day 5 | | **Total** | **7–10 days**| April 10–13, 2026 |

---

## 6. Resources & Files You Will Need (I Will Provide All)

- `docker-compose.yml` (full production version) - `.env.example` - Folder layout diagram - `agent.py` skeleton (Slack Bolt + LangChain/LlamaIndex + scheduler) - Exact system prompts for extraction and RAG - Troubleshooting checklist

---

## 7. Risks & Mitigations

| Risk | Likelihood | Mitigation | |-----------------------------|------------|-----------------------------------------| | Syncthing merge conflicts | Medium | Append-only master files + ignore rules | | LLM cost overrun | Low | Start with cheaper model for EOD | | Container downtime | Low | Docker restart:always + healthchecks | | RAG hallucination on dates | Medium | 70B model + citation requirement | | Office WiFi issues | None | Slack is already whitelisted |

---

## 8. Next Action (Right Now)

Reply with **“Ship it”** and I will immediately drop the complete starter kit:

1. Full `docker-compose.yml` 2. `.env` template 3. Folder structure 4. `agent.py` core code (ready to copy-paste)