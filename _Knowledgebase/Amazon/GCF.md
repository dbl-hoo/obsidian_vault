---
tags: [knowledgebase, amazon, gcf]
last_updated: 2026-06-10
---

# GCF — Knowledge Base

## Design Standards

### ARS Gen 14 Building Requirements

| Parameter | Requirement |
|---|---|
| Power | 5x 4,000-amp services |

### 1DC Building Requirements

| Parameter | Requirement |
|---|---|
| Building Size | 1M – 1.2M SF |
| Clear Height | 40' min |
| Dock Doors | 86 (36 IB / 50 OB) |
| Trailer Parking | 431 (517 incl. dock doors) |
| Auto Parking | 413 min / 516 preferred |
| Building Width | 1,736' |
| Building Depth | 588' |
| Power | 10,000 amps |
| Off-peak Weekly HC | 2,103 |
| Distance to Target Zip | 150 miles |

### Dock Spacing

Minimum 13' dock spacing required.

---

## Power / Utility Coordination

### Power Basics: Connected Load vs. Diversified Load, kVA vs. MW vs. Amps

**Connected load vs. diversified (demand) load**

- **Connected load** = sum of the nameplate ratings of every piece of equipment on site, per NEC. A theoretical ceiling — what the building would draw if everything ran at full rated output simultaneously. Always much higher than actual usage.
- **Diversified load** (a.k.a. demand load, coincident peak, or "anticipated peak coincident usage") = the realistic peak draw, accounting for the fact that not everything runs full-out at the same time. This is the number utilities actually plan infrastructure around.
- **Diversity factor** = connected load ÷ diversified load. A factor of 2 means real peak usage is half of the on-paper connected load.
- Why it matters: utilities size lines, transformers, and feeders to the diversified load (often building to ~75% of connected load as "anticipated"). If Amazon's reserved capacity exceeds its diversified load, the excess is **speculative load** — billed upfront (see below).

**kVA vs. kW/MW vs. Amps — units that get used interchangeably on calls**

- **kW / MW (real power)** — power that actually does work (motors, lights, conveyors). What shows up on the utility bill.
- **kVA / MVA (apparent power)** — total power the system must be sized for, including "reactive" power (needed to maintain electrical fields in motors/transformers but doesn't do useful work).
- **Power factor (PF)** = kW ÷ kVA. Industrial sites typically run PF ≈ 0.85–0.95. Utilities may assume their own PF — don't assume it matches Amazon's number without asking.
- **Amps** = current — how services, conductors, and breakers are rated. Converts to kVA via voltage:
  - Three-phase: **kVA = (Volts × Amps × √3) ÷ 1,000**
  - Example: 480V × 12,000A × √3 ÷ 1,000 ≈ 10 MVA — this is where "12,000A = 10MVA" comes from.

**Quick conversions (480V three-phase, PF ≈ 0.9 — typical industrial)**

| Amps | ≈ kVA/MVA | ≈ kW/MW (at PF 0.9) |
|---|---|---|
| 1,800A | 1.5 MVA | ~1.35 MW |
| 4,800A | 4.0 MVA | ~3.6 MW |
| 9,000A | 7.5 MVA | ~6.75 MW |
| 12,000A | 10 MVA | ~9 MW |

Utilities build to 75% of connected load as the "anticipated" level. Building to 100% of connected load is treated as speculative load and costs the difference upfront.

---

## Resources

### Comps Templates
`W:\Shared With Me\Ops RE Transactions\CORE (GCF)\xTemplates\Comps`
