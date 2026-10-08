---
tags: [knowledgebase, amazon, rdc]
last_updated: 2026-10-05
---

# RDC — Knowledge Base

**RDC = Regional Distribution Center.** Gen1 program, launches 2027+. Covers internal conversions and Spec-to-Suit (STS) builds of existing buildings.

**Source:** ![[RDC Gen1 Site Guidance and Program Summary v2.pdf]]
NA_RDC Gen1_Site Guidance and Program Summary_v2 (GBDR), "for Review" draft. BRS dates: 1M SF 09/14/2026; 1.2M SF 09/11/2026. The full RDC Gen1 BRS (Appendix 9) is on Shield and marked internal-only.

**Overall approach:** Reuse existing site and building components where possible to keep scope down. RGM (Remote Gate Management), safety and regulatory items still can't be compromised. Where the guidance gives options, Pre-con takes the most conservative case for every attribute.

---

## Spec Building Screen — Go/No-Go Criteria

These are the attributes that can't be fixed cheaply in an existing building. Screen these first.

| Attribute | 1M SF Program | 1.2M SF Program | Notes |
|---|---|---|---|
| **Building SF** | 1,000,000 | 1,200,000 | WWDE **prefers 1.2M** (more storage cube) |
| **Clear height** | **40' min** | **40' min** | Required for VNA racking |
| **Max ceiling height** | **48'** | **48'** | Over 48' isn't preferred: may need extra fire protection, ceiling or aisle changes |
| **Dock config** | Two sides (cross-dock or L-shape) | Two sides (cross-dock or L-shape) | Single-load buildings don't qualify |
| **Dock doors (min)** | 80 (30 IB / 50 OB) | 90 (35 IB / 55 OB) | 1M IB includes 10 plumbed doors |
| **Dock door spacing** | 13' O.C. min | 13' O.C. min | Added in v2 specifically for existing-building screening |
| **Trailer slips (incl. doors)** | 266 | 319 | If the site can't hit this, an **offsite yard is required** to operate |
| **Site acreage** | ±56 ac | ±60.4 ac | |
| **Associate parking** | 497 | 582 | 0.9 stalls per peak-shift headcount (PSHC). Pending LT approval |
| **Building dims (FlexShell ref.)** | 1,736' × 588' | 1,848' × 640' | Reference only, not a hard requirement |
| **Column spacing** | 56' L × 52' W preferred | 56' L × 52' W preferred | Existing spacing on site stays |
| **Slab** | 7" min | 7" min | Also must meet VNA floor flatness (see below) |
| **Curb cuts** | 2 min, 4 preferred | 2 min, 4 preferred | Fewer is a deviation that has to be flagged in design review |

### Lower-clear-height fallback
Buildings **under 40' clear** can still work if:
- Rack uprights max out at 402"
- The layout uses 48"-wide order pickers and 60" aisles

In that case K-28 sprinklers aren't required. The site architect and fire protection engineer confirm with WWDE and IDS (Integrated Design System) on a site-specific layout. The 48' max ceiling and 40' clear still can't be **exceeded**, even if a bigger roof span needs more slope.

---

## Operating Program

| Metric | 1M SF | 1.2M SF |
|---|---|---|
| Weekly units IB / OB | 5.7MM | 7.4MM |
| Storage net cube | 5.48M ft³ | 7.0M ft³ |
| Storage bin mix (case / pallet) | 75% / 25% | 75% / 25% |
| IB freight: new vendor / transfer-in | 74% / 26% | 74% / 26% |
| IB fluid / pallet | 67% / 33% | 67% / 33% |
| Cross-dock volume | 40% | 40% |
| Each sort | UIS (universal induction sorter), 50% of OB volume | Same |
| Max OB arcs | 50 | 50 |
| Peak shift HC (PSHC) | 552 | 646 |
| Off-peak shift HC | ~470 | ~550 |
| PIT (powered industrial truck) count | 199 | 245 |
| PIT fuel | Hydrogen or lithium | Hydrogen or lithium |
| Shift break | Single | Single |

- PSHC includes AWD and fixed headcount (110). Source: WWDE, 9/18/2026.
- Hydrogen only goes where H2 infrastructure already exists. Dropping existing H2 requires formal decommissioning with a cost analysis and approval.
- **No hazmat in RDC.**
- **HRV (High Retail Value) inventory is in scope.** It needs badged cages, light curtains, dedicated cameras and structurally reinforced aisle back plates.

### AWD Sandbox (preliminary)
Requirements are pending a leadership decision. A separate AWD guidance doc is coming.
- About 19K SF dedicated inside the footprint, with 11 PSHC
- **Dock door count conflicts in the BRS.** The AWD section says 9 doors. The 1.2M SF dock table lists 10 AWD doors inside the 35 IB (9 fluid / 3 auger & compactor / 3 non-inventory / 10 pallet / 10 AWD).
- No dedicated trailer slips
- Electrical load is **not included** in the baseline power numbers. Treat it as additive and reserve capacity for it.
- An Ergorider needs slab reinforcement

---

## Building Systems — Spec Building Diligence Items

### Floor / Slab
- Floor flatness and levelness have to meet VNA, PIT and pedestrian requirements. **Verify this during site selection.** Budget funds if corrections are needed.
- In VNA aisles the transverse Fmin is **60** for racks up to 402", or **45** for racks up to 300". Verify by profileograph. If the floor fails, it gets ground or the slab is replaced.
- At IB Ergorider locations, the structural engineer of record (SER) checks slab capacity for point loads. Remediation scope is set during diligence.

### Structure / Roof
- **Roof-hung MHE (material handling equipment):** IB and OB dock areas need roof structure that can carry ceiling-hung conveyance. WWDE conditionally requires it, pending leadership approval. Pre-con confirms feasibility and cost per site.
- A concrete PID mezzanine/platform, 190" × 75"
- Rooftop solar is per site-specific design
- Roof access has to comply with OSHA 1910.23. Add a davit crane at each roof hatch.

### Fire Protection
- **ESFR K-28 pendent (Reliable N28T3)** designed for:
  - 48' max ceiling and 40' clear
  - 37' (444") VNA racks
  - 70" aisles for VNA case and 78" for VNA pallet
  - 3" transverse flue
  - 36" min clearance from deflector to top of storage
- Use the existing fire pump room or house

### Electrical — Utility Demand

| | 1M SF | 1.2M SF |
|---|---|---|
| Site & building (excl. MHE, PIT, EV): Li-Ion PIT + gas heat | 2,133 kVA / 2,566 A | 2,560 kVA / 3,079 A |
| Site & building (excl. MHE, PIT, EV): Li-Ion PIT + all-electric | 3,803–5,033 kVA / 4,566–6,056 A | 4,230–5,460 kVA / 5,079–6,579 A |
| PIT charging | 985 kVA / 1,185 A | 1,183 kVA / 1,423 A |
| MHE | 3,281 kVA / 3,947 A | 3,620 kVA / 4,354 A |
| **A. Site + Building total, gas heat** | **6,399 kVA / 7,698 A** | **7,363 kVA / 8,856 A** |
| **A. Site + Building total, all-electric** | **8,069–9,299 kVA / 9,688–11,188 A** | **9,033–10,263 kVA / 10,856–12,356 A** |
| B. Truck yard EV (2 slips) | 120 kVA / 160 A | 120 kVA / 160 A |
| C. Associate parking EV | Per AHJ (local code authority) | Per AHJ |

- Amps are at 480V secondary service. With primary (medium-voltage) service, coordinate the total kVA with the utility instead.
- Diversity factors: 50% for Li-Ion PIT, 40% for MHE.
- Up to 4 main switchboards (480VAC). The site EoR (electrical engineer of record) finalizes the count.
- **If power isn't there at launch:** add a new switchboard with exterior camlock connections for a temporary generator and a future grid tie-in. The temp generator carries the site until permanent utility service is in.
- Larger panels are specified up front to allow for future retrofits.
- An emergency generator (natural gas preferred) covers life safety, IDFs/MDF, the primary guardhouse and telecom. It sits at least 50' from parking lot drains.

### HVAC
- Reuse existing HVAC where possible
- With no existing HVAC or gas, the baseline is **all-electric heat pumps** (cold-climate inverter scroll, or vapor-injection below 0°F). Dual-fuel RTUs are allowed if gas costs less than the electrical upgrade.
- Add HVLS fans in high-occupancy areas, and at docks if ductwork doesn't heat down to the floor
- The BMS is BACnet, integrated to Niagara N4 EBMS. Existing RTUs get checked for compatibility.

### Lighting
- Existing warehouse lighting stays if it meets standard. End-of-life fixtures are replaced with LED rated L70 80K hrs (>45W) and backed by a 7-year warranty.
- Whips older than 10 years get replaced
- Yard: existing lighting is fine for internal conversions. **STS sites must meet the current Amazon yard standard.**

---

## Site / Yard

- **Guardhouses (BTS):** 2 total.
  - Primary IB: 2 lanes, 10 queue
  - Secondary OB: 2 lanes, 5 queue
  - Existing yards with constraints: confirm the lane and guardhouse count with TOM
  - An existing primary guardhouse can be reused if it's at least 9'-3" × 15'-11" (9'-4" × 24'-8" preferred)
  - The guardhouse needs a restroom unless one is within 500'. Porta-potties aren't allowed.
- **RGM is required** on all new launches
- **Converting a two-way yard to one-way** adds an OB guardhouse and RGM infrastructure
- **Trailer stalls:**
  - Dock stalls: 13' centerline, 60' deep in 4,000 PSI concrete
  - Parking stalls: 12' × 55' with a 10' dolly pad
  - "Land-on-blue" applies to all trailer parking stalls
- **Drive aisles:**
  - 70' clear between trailer stalls
  - 40' two-way, or 20' one-way where no trailers move alongside
  - Dead-end aisles need a 100' turnaround circle sized for a WB-67 truck
- **Dock design:**
  - **No dock wells and no sawtooth docks**
  - Aprons slope 1–2% away from the building with no cross-slope. If they don't, a topping slab is base scope.
- **Fence:** 8' chain-link. If the existing fence is 6', upgrade it or get a WWOS exception.
- **Truck EV:** only 2 chargers, run off the warehouse switchboard. No separate transformer.
- **Air quality monitors** (interior and exterior) are required in AZ, CA, CO, ID, NV, OR, UT and WA

---

## Interior / Welfare Program (sizing check for existing office space)

| Item | 1M SF | 1.2M SF |
|---|---|---|
| Main breakroom seats (90% PSHC, single break) | 498 | 582 |
| Lockers (59% PSHC) | 330 | 390 |
| Tandem turnstiles / bypass doors | 2 / 2 | 4 / 4 |
| LP screening module | #30769 (2+1 lanes, 27'-8" min) | Same |
| Large restrooms facing warehouse | 20 fixtures | 24 fixtures |
| Restrooms facing lockers | 6 | 6 |
| Training room | 118 seats | 118 seats |
| Wellness center | Medium | Medium |
| Multifaith | Double | Double |

- **Max 500' travel distance** to:
  - Remote breakrooms (Amazon standard)
  - Remote restrooms (building code)
  - Trucker lounges/cages (min 1 per active dock wall)
  - Water coolers
- Lactation space within a 5-minute walk (about 1,000 ft) of every workstation
- Office: 6 private offices, 8 open desks and a 12-seat conference room
- Use the existing main entrance. If there isn't one, put the office block there.
- Keep any existing recruiting center. Otherwise align with WFS.

---

## Quick Red Flags for a Spec Building

- Clear height **under 40'** (fallback design possible, but costs storage cube) or ceiling **over 48'** (fire protection rework)
- Single-sided dock, or not enough doors on two sides
- Dock door spacing **under 13' O.C.**
- Not enough yard for 266 / 319 slips, which means an offsite yard
- Dock wells, sawtooth docks, or aprons sloping the wrong way
- Floor that won't hit Fmin 60 in VNA aisles, which means grinding or slab replacement
- Roof structure that can't carry roof-hung conveyor at the docks
- Utility capacity well under about 7.5–10 MVA, which means a temp generator and a utility upgrade timeline
- Fewer than 2 curb cuts, or truck and car traffic that can't be separated
