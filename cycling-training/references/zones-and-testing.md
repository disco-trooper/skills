# Power Zones & FTP Testing

## Table of Contents
1. [Zone Models](#zone-models)
2. [FTP Testing Protocols](#ftp-testing-protocols)
3. [Critical Power Model](#critical-power-model)
4. [Zone Setup Guidelines](#zone-setup-guidelines)
5. [Interpreting Test Results](#interpreting-test-results)

---

## Key Research Summary

| Topic | Finding | Source |
|-------|---------|--------|
| FTP 20-min test validity | 95% of 20-min power sustainable for 60 min in trained athletes | Morgan et al. 2019 (PMID: 30387374) |
| Critical Power concept | CP represents highest sustainable oxidative ATP rate; W' depleted at exhaustion | Jones et al. 2010 (PMID: 20195180) |
| 3-min all-out test | Valid CP estimation; end-test power correlates r=0.99 with conventional CP | Vanhatalo et al. 2007 (PMID: 17473782) |
| W'bal model | Accurately predicts exhaustion during intermittent cycling (ROC=0.914) | Skiba et al. 2014 (PMID: 24509723) |
| Polarized training zones | ~80% below VT1, ~20% above VT2 optimal for endurance | Seiler 2010 (PMID: 20861519) |
| Threshold determination | CP/CS best delineates heavy-severe boundary; LT1/VT valid for moderate-heavy | Jamnick et al. 2020 (PMID: 32729096) |

---

## Zone Models

### Coggan 7-Zone Model (Classic)

The most widely used model, based on percentage of FTP (Functional Threshold Power).

| Zone | Name | % FTP | HR % LTHR | RPE | Physiological Basis |
|------|------|-------|-----------|-----|---------------------|
| 1 | Active Recovery | <55% | <68% | 1-2 | Recovery, minimal stress |
| 2 | Endurance | 55-75% | 69-83% | 2-3 | Fat oxidation, aerobic base |
| 3 | Tempo | 76-90% | 84-94% | 3-5 | Aerobic/anaerobic transition |
| 4 | Threshold | 91-105% | 95-105% | 5-7 | MLSS, lactate clearance |
| 5 | VO2max | 106-120% | >106% | 7-8 | Maximal oxygen uptake |
| 6 | Anaerobic | 121-150% | N/A | 9 | Anaerobic glycolysis |
| 7 | Neuromuscular | Max | N/A | 10 | Neuromuscular power |

**When to use:** General training, most athletes, TrainerRoad/Zwift compatibility.

### Seiler 3-Zone Model (Polarized)

Based on ventilatory/lactate thresholds, emphasizes polarized training.

| Zone | Physiological Marker | % FTP (approx) | Description |
|------|---------------------|----------------|-------------|
| Zone 1 | Below VT1/LT1 | <75-80% | Comfortable, conversational |
| Zone 2 | VT1-VT2 (LT1-LT2) | 80-95% | "Grey zone" - hard but not hard enough |
| Zone 3 | Above VT2/LT2 | >95% | Unsustainable, race pace+ |

**When to use:** Polarized training approach, well-trained athletes.

### Coggan iLevels (WKO5)

Individualized zones based on power duration curve modeling.

| Level | Name | Description |
|-------|------|-------------|
| iLevel 1 | Recovery | Very light |
| iLevel 2 | Endurance | Aerobic base |
| iLevel 3 | Tempo | Moderate aerobic |
| iLevel 4 | FTP | Threshold power |
| iLevel 5 | FRC | Functional Reserve Capacity |
| iLevel 6 | Pmax | Peak power |

**Calculation:** Uses mFTP (modeled FTP) and individual power duration curve.
**When to use:** WKO5 users, advanced athletes with extensive power data.

### Polarized Index Calculation

To assess training distribution:
```
Polarized Training Index (PTI) = (% Zone 1 + % Zone 3) / % Zone 2
```
- PTI > 2.0 = Well polarized
- PTI 1.5-2.0 = Moderately polarized
- PTI < 1.5 = Threshold-focused

### Zone Model Comparison

| Model | Zones | Based On | Best For |
|-------|-------|----------|----------|
| Coggan | 7 | FTP | Structured training, TSS |
| Seiler | 3 | Lactate thresholds | Polarized training |
| SYSTM/4DP | 4 targets | NM, AC, MAP, FTP | Multi-dimensional |
| Xert | Continuous | MPA, fitness signature | Real-time tracking |
| ISM | 5 | % FTP | Simplified approach |

### When to Use Which Model

**Coggan 7-zone:**
- Most platforms (TrainerRoad, TrainingPeaks)
- Detailed workout prescription
- TSS-based load management

**Seiler 3-zone:**
- Polarized training focus
- Simplifies intensity decisions
- Research-backed distribution

**Individual considerations:**
- High FTP variability → Regular retesting
- Poor repeatability → Use RPE alongside power
- Indoor/outdoor difference → Consider separate FTPs

---

## FTP Testing Protocols

### 20-Minute Test (Classic Coggan)

**Protocol:**
1. Warm-up: 20 min progressive
2. 3 × 1 min high cadence (100+ rpm)
3. 5 min easy recovery
4. **20 min all-out effort**
5. 10-15 min cool-down

**FTP Calculation:** 20-min average power × 0.95

**Pros:** Well-validated, simple
**Cons:** Requires pacing skill, mentally demanding

**Pacing Strategy:**
- Start at estimated FTP
- First 5 min: Settle in, don't go too hard
- Middle 10 min: Steady state, stay focused
- Last 5 min: Push if you have anything left
- Target: Negative split or even pacing

### 8-Minute Test (Sufferfest/SYSTM)

**Protocol:**
1. Warm-up: 15 min
2. **5 min all-out effort** (for MAP estimation)
3. 10 min recovery
4. **20 min FTP effort** OR **2 × 8 min efforts** with 10 min recovery

**FTP Calculation:**
- From 2×8min: Average of both × 0.90
- Combined with 5-min for 4DP profile

### Ramp Test

**Protocol:**
1. Warm-up: 5-10 min easy
2. Start at low power (100W typical)
3. Increase 20W every minute until failure
4. Continue until you cannot maintain target

**FTP Calculation:** 75% of best 1-minute power achieved

**Pros:** Short, less pacing required, repeatable
**Cons:** Favors anaerobic athletes, may underestimate FTP for diesel types

**Who it suits:**
- Athletes with good anaerobic capacity: May overestimate FTP
- "Diesel" athletes (strong aerobically): May underestimate FTP
- Best for: Tracking relative changes over time

### 60-Minute Test (Gold Standard)

**Protocol:**
1. Warm-up: 20 min
2. **60 min maximal sustainable effort**
3. Cool-down

**FTP = 60-min average power**

**Pros:** Most accurate by definition
**Cons:** Extremely demanding, rarely done, requires significant motivation

### Critical Power Test

**Protocol (3-test method):**
1. 3-minute all-out effort
2. 10-minute all-out effort
3. 20-minute all-out effort

**Calculation:** Mathematical modeling yields CP (critical power) and W' (anaerobic work capacity)

**Alternative (Ramp + 3-min):**
1. Ramp test to exhaustion
2. Recovery (20-30 min)
3. 3-minute all-out test

---

## Critical Power Model

### Fundamentals

**Critical Power (CP):** The highest power output that can theoretically be maintained indefinitely without fatigue accumulation. In practice, ~40-70 minutes.

**W' (W-prime):** The fixed amount of work (in kJ) that can be done above CP before exhaustion.

### Mathematical Model

```
t = W' / (P - CP)

Where:
t = time to exhaustion
P = power output
CP = critical power
W' = anaerobic work capacity
```

### Typical Values

| Athlete Level | W' (kJ) | CP (W) | CP as % FTP |
|---------------|---------|--------|-------------|
| Recreational | 10-15 | 150-220 | 95-98% |
| Trained | 15-20 | 220-300 | 96-99% |
| Elite | 20-30 | 300-400+ | 97-100% |

### CP vs FTP

- CP is typically 3-8% higher than traditional FTP
- CP represents true physiological threshold
- FTP (0.95 × 20min) is a practical approximation
- For pacing: Use CP for efforts >30 min

### W' Reconstitution

W' recovers during sub-CP efforts:
- Fast component: ~30% recovery in first 2 min
- Slow component: Full recovery takes 15-30 min
- Recovery rate depends on intensity below CP

**Practical Application:**
- Know your W' for race tactics
- Managing efforts in crits/road races
- Pacing hilly time trials

---

## Zone Setup Guidelines

### Using FTP Test Results

1. **Calculate FTP** from test result
2. **Set zones** as percentage of FTP
3. **Validate** with training feel over 2-3 weeks
4. **Adjust** if necessary (±2-5W)

### Zone Calculation Example

FTP = 250W

| Zone | % FTP | Power Range |
|------|-------|-------------|
| 1 | <55% | <138W |
| 2 | 55-75% | 138-188W |
| 3 | 76-90% | 189-225W |
| 4 | 91-105% | 226-263W |
| 5 | 106-120% | 264-300W |
| 6 | 121-150% | 301-375W |
| 7 | Max | >375W |

### Heart Rate Zones (from LTHR)

If you have LTHR (lactate threshold heart rate):

| Zone | % LTHR |
|------|--------|
| 1 | <68% |
| 2 | 69-83% |
| 3 | 84-94% |
| 4 | 95-105% |
| 5a | 106%+ |

**Finding LTHR:** Average HR of last 20 min of 30-min FTP test.

### Platform-Specific Setup

**TrainerRoad:**
- Uses FTP directly
- Zones auto-calculated
- Ramp test integrated

**Zwift:**
- Set FTP in settings
- Zones displayed during rides
- FTP test workouts available

**Wahoo SYSTM:**
- Uses 4DP (4 power metrics)
- More individualized zones
- Full Frontal test required

**intervals.icu:**
- Customizable zone models
- Can use CP or FTP
- Import from other platforms

---

## Interpreting Test Results

### Signs of Good Test

- Even or negative split pacing
- RPE 9-10 at finish
- HR reaches expected max zone
- Unable to continue at test power
- No significant power drop in final minutes

### Signs of Poor Test

- Started too hard (positive split)
- Significant power fade (>10%)
- Didn't reach expected RPE
- Could have gone harder at end
- External interruptions

### FTP Trends

**Expected progression:**
- Beginner: +10-20W per month possible
- Intermediate: +5-10W per month
- Advanced: +2-5W per month
- Elite: +1-3W per year

**FTP decline indicators:**
- Time off (loses ~5-7% per week of inactivity)
- Illness
- Overtraining
- Seasonal variation (normal)

### Red Flags in Testing

- **HR very low:** May indicate fatigue or illness
- **HR very high:** May indicate stress or dehydration
- **Power much lower than expected:** Rest and retest
- **Power much higher than expected:** Verify calibration, may need to validate with training

### When Test Results Don't Match Training

If prescribed workouts feel wrong:
1. **Too hard:** FTP may be set too high
2. **Too easy:** FTP may be set too low
3. **Threshold feels ok but VO2max is too hard:** May have tested poorly on anaerobic component
4. **Good at short efforts, struggle with long:** May have overestimated due to anaerobic contribution

**Solution:** Trust training feel, adjust zones ±3-5%, retest after 4-6 weeks.

---

## Test Frequency Recommendations

| Phase | Test Frequency |
|-------|----------------|
| Base building | Every 6-8 weeks |
| Build phase | Every 4-6 weeks |
| Race season | Every 6-8 weeks or as needed |
| Off-season | Beginning and end |

**Avoid testing when:**
- Fatigued (TSB < -10)
- Ill or recovering from illness
- Within 1 week of hard race
- Not properly fueled/hydrated

---

## Related Files

- [workouts.md](workouts.md) - Workouts structured by power zones
- [analytics.md](analytics.md) - Analysis of test and training data
- [physiology.md](physiology.md) - Physiological basis of zone models
- [periodization.md](periodization.md) - When and how to test within the season
