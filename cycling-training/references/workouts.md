# Workout Library

Comprehensive collection of evidence-based cycling workouts organized by training goal.
Based on current sports science research.

## Quick Search Patterns

For efficient navigation in this large file, use these grep patterns:

| Looking for | Pattern |
|-------------|---------|
| Endurance workouts | `grep -n "^### .*Endurance" workouts.md` |
| VO2max intervals | `grep -n "VO2max\|Norwegian 4x4\|30-30" workouts.md` |
| Sweet spot | `grep -n "Sweet Spot\|88-94%" workouts.md` |
| Threshold | `grep -n "^### .*Threshold\|95-105%" workouts.md` |
| Sprint/Power | `grep -n "Sprint\|Neuromuscular\|Max" workouts.md` |
| Research sources | `grep -n "PMID\|PMC\|Source:" workouts.md` |
| TSS estimates | `grep -n "TSS:" workouts.md` |

---

## Table of Contents

### Aerobic Development
1. [Endurance Workouts](#endurance-workouts) - Z2, cadence work, decoupling test
2. [Tempo & Sweet Spot](#tempo--sweet-spot) - Sweet spot, over-unders, tempo cruise

### Threshold & VO2max
3. [Threshold Workouts](#threshold-workouts) - Classic, progression, bursts
4. [VO2max Intervals](#vo2max-intervals) - 30-30s, 5×4min, Norwegian 4×4, 10-20-30

### High Intensity
5. [Anaerobic Capacity](#anaerobic-capacity) - AC intervals, Tabata, race winners
6. [Sprint & Neuromuscular](#sprint--neuromuscular) - Max sprints, repeatability

### Specialty
7. [Cadence Training](#cadence-training) - High cadence, low cadence force
8. [Race-Specific Workouts](#race-specific-workouts) - TT, criterium, hill repeats
9. [Recovery Workouts](#recovery-workouts) - Active recovery, openers

**Quick Jump:** [Research Summary](#key-research-findings) | [Selection Guide](#workout-selection-guide) | [TSS Estimates](#tss-estimates-by-workout-type)

---

## Key Research Findings

**Optimal VO2max Interval Parameters:**
*Source: Yang et al. 2025, BMC Sports Sci Med Rehabil (PMC12218014, PMID: 40605061), n=1,261 athletes*
- Work duration: **140 seconds** (inverted U-shaped relationship)
- Work:Recovery ratio: **0.85** (~140s work : 165s recovery)
- Frequency: 3 sessions/week
- Duration: 3-6 weeks for significant adaptations
- RST > HIIT > SIT > CT in effectiveness ranking (no significant difference among interval methods)

**Training Intensity Distribution:**
*Source: Yu et al. 2025, Front Physiol (PMC12568352, DOI: 10.3389/fphys.2025.1657892)*
- Polarized and pyramidal distributions yield comparable improvements
- Most important factors: workout frequency > time in zones > distribution
- TID should be periodized across training phases (general prep, specific prep, competition)

---

## Endurance Workouts

### Z2 Endurance Ride
**Purpose:** Aerobic base, fat oxidation, mitochondrial development
**Target:** 55-75% FTP, HR Zone 2
**Duration:** 1.5-6+ hours

```
Workout: Standard Endurance
Total: 2-4 hours
Structure: Steady Zone 2 throughout
Power: 55-75% FTP
Cadence: Self-selected (80-95 typical)
RPE: 2-3/10
Notes: Should be conversational pace
```

### Endurance with Cadence Work
**Purpose:** Aerobic base + pedaling efficiency
**Duration:** 2-3 hours

```
Workout: Cadence Pyramids
10 min warm-up
Main set (repeat 3-4x):
  - 5 min @ 60 rpm, 70% FTP
  - 5 min @ 80 rpm, 65% FTP
  - 5 min @ 100 rpm, 60% FTP
  - 5 min @ 80 rpm, 65% FTP
10 min cool-down
```

### Aerobic Decoupling Test
**Purpose:** Assess aerobic fitness
**Duration:** 2 hours

```
Workout: Decoupling Test
20 min warm-up
60 min steady @ 70-75% FTP
Record: Average power and HR for first and second 30 min
Cool-down
Target: <5% HR drift = good aerobic fitness
```

---

## Tempo & Sweet Spot

### Sweet Spot Intervals
**Purpose:** Time-efficient threshold development
**Target:** 84-97% FTP
**Scientific basis:** Maximum training stimulus with manageable fatigue

```
Workout: Sweet Spot 3x15
15 min warm-up
3 × 15 min @ 88-93% FTP
  - 5 min recovery between intervals
15 min cool-down
Total: 90 min, TSS ~85

Workout: Sweet Spot 2x20
15 min warm-up
2 × 20 min @ 88-93% FTP
  - 5 min recovery
15 min cool-down
Total: 75 min, TSS ~75

Workout: Sweet Spot Continuous
15 min warm-up
45-60 min @ 84-88% FTP
10 min cool-down
Total: 70-85 min, TSS ~80-95
```

### Over-Under Intervals
**Purpose:** Lactate clearance, threshold tolerance
**Target:** Alternate above/below FTP
**Scientific basis:** Lactate shuttle theory (Dr. George Brooks, UC Berkeley)
- MCT-4 transports lactate from fast-twitch fibers
- MCT-1 uptakes lactate into slow-twitch for oxidation
- Training above/below threshold maximizes transporter adaptation

```
Workout: Over-Unders 3x12
15 min warm-up
3 × 12 min as:
  - 2 min @ 95% FTP (under)
  - 1 min @ 105% FTP (over)
  - Repeat 4x within each interval
8 min recovery between sets
15 min cool-down
Total: 80 min, TSS ~90

Workout: Criss-Cross
15 min warm-up
3 × 10 min as:
  - 30 sec @ 110% FTP
  - 30 sec @ 90% FTP
  - Continuous alternating
6 min recovery between sets
15 min cool-down
Total: 65 min, TSS ~75
```

### Tempo Cruise Intervals
**Purpose:** Muscular endurance, fatigue resistance
**Target:** 76-90% FTP

```
Workout: Tempo 3x20
15 min warm-up
3 × 20 min @ 80-85% FTP
  - 5 min recovery
10 min cool-down
Total: 95 min, TSS ~85

Workout: Long Tempo
15 min warm-up
45-60 min continuous @ 76-83% FTP
10 min cool-down
Total: 70-85 min, TSS ~70-85
```

---

## Threshold Workouts

### Classic Threshold Intervals
**Purpose:** Increase FTP, lactate tolerance
**Target:** 95-105% FTP

```
Workout: 2x20 @ Threshold
20 min warm-up
2 × 20 min @ 95-100% FTP
  - 10 min recovery
15 min cool-down
Total: 85 min, TSS ~95
Notes: Gold standard threshold workout

Workout: 3x15 @ Threshold
15 min warm-up
3 × 15 min @ 95-100% FTP
  - 8 min recovery
15 min cool-down
Total: 90 min, TSS ~95

Workout: 4x10 @ Threshold
15 min warm-up
4 × 10 min @ 100-105% FTP
  - 5 min recovery
15 min cool-down
Total: 85 min, TSS ~90
```

### Threshold Progression
**Purpose:** Build threshold duration capacity

```
Week 1: 2 × 15 min @ 95% FTP
Week 2: 2 × 18 min @ 95% FTP
Week 3: 2 × 20 min @ 95% FTP
Week 4: Deload - 2 × 12 min @ 90% FTP
Week 5: 2 × 20 min @ 97% FTP
Week 6: 1 × 30 min @ 95% FTP
```

### Threshold Bursts
**Purpose:** Handle accelerations at threshold

```
Workout: Threshold with Bursts
15 min warm-up
4 × 8 min @ 95% FTP with:
  - 15 sec burst @ 130% FTP at 2 min and 5 min
  - 5 min recovery between intervals
15 min cool-down
Total: 75 min, TSS ~85
```

---

## VO2max Intervals

### Scientific Basis (2025 Research)
- Target: Accumulate time at >90% VO2max
- Optimal work duration: 140 seconds (2min 20s)
- Optimal work:rest ratio: 0.85
- Long intervals (4×3min) produce more time at >90% VO2max than short intervals (21×30s) at same intensity

### Classic VO2max
**Purpose:** Increase VO2max, aerobic power
**Target:** 106-120% FTP, achieve >90% VO2max
**Work:Rest:** Typically 1:1 to 2:1

```
Workout: Billat 30-30s (Optimized)
15 min warm-up
3 sets of:
  - 8+ min continuous (8×30s ON / 30s OFF minimum per set)
  - ON: 130-140% FTP, OFF: 50-60% FTP (NOT passive rest)
  - 5 min recovery between sets
15 min cool-down
Total: 65 min, TSS ~75
Research: Rønnestad et al. 2020 - 4.7% 20min power improvement vs 1.7% reduction with 4×5min

Workout: 5x4min @ VO2max
15 min warm-up
5 × 4 min @ 108-112% FTP
  - 4 min recovery @ 50% FTP
15 min cool-down
Total: 70 min, TSS ~80

Workout: 4x5min @ VO2max
15 min warm-up
4 × 5 min @ 106-110% FTP
  - 5 min recovery
15 min cool-down
Total: 70 min, TSS ~80
```

### Long VO2max Intervals
**Purpose:** Sustained aerobic power, race simulation

```
Workout: 3x8min @ VO2max
20 min warm-up
3 × 8 min @ 105-108% FTP
  - 8 min recovery
15 min cool-down
Total: 85 min, TSS ~90
Notes: For well-trained athletes, demanding workout
```

### Norwegian 4x4 (Gold Standard)
**Purpose:** VO2max development (200+ peer-reviewed studies)
**Research:** Developed by Professors Jan Hoff and Jan Helgerud

```
Workout: Norwegian 4x4
15 min warm-up
4 × 4 min @ 108-115% FTP (target 90-95% HRmax)
  - 3 min active recovery @ 60-70% HRmax
15 min cool-down
Total: 58 min, TSS ~65

Research findings:
- Hearts "20 years younger" after 2-year 1×weekly intervention (50yo study)
- 13% VO2max improvement over 8 weeks with 3 sessions/week
- Considered gold standard for VO2max development
```

### 10-20-30 Training (New Protocol)
**Purpose:** VO2max with high adherence, variable intensity
**Research:** PMC11295100 (2024) - 6.4% VO2max improvement, >80% adherence

```
Workout: 10-20-30
15 min warm-up
3-4 blocks of 5 minutes:
  - 30 sec @ 50-60% FTP (low)
  - 20 sec @ 75-85% FTP (moderate)
  - 10 sec @ near maximal (high)
  - Repeat 5× = 5 min block
3 min recovery between blocks
15 min cool-down
Total: 50-60 min, TSS ~55

Benefits: Also reduces blood pressure in hypertensive patients
```

### Micro-Intervals (40-20s)
**Purpose:** Accumulate VO2max time with lower perceptual strain

```
Workout: 40-20s VO2max
15 min warm-up
3 sets of:
  - 8 × (40 sec @ 125-130% FTP / 20 sec @ 50% FTP)
  - 5 min between sets
15 min cool-down
Total: 65 min, TSS ~70
```

---

## Anaerobic Capacity

### AC Intervals
**Purpose:** Increase anaerobic capacity, W' development
**Target:** 121-150% FTP

```
Workout: 30-30s Anaerobic
15 min warm-up
3 sets of:
  - 8 × (30 sec @ 140-150% FTP / 30 sec easy)
  - 5 min between sets
15 min cool-down
Total: 55 min, TSS ~55

Workout: Tabata Protocol
15 min warm-up
4-8 × (20 sec @ 170%+ FTP / 10 sec rest)
10 min recovery
Repeat 1-2 more sets
15 min cool-down
Total: 45-60 min, TSS ~50-65
Notes: True Tabata requires maximal effort
```

### Race Winners
**Purpose:** Simulate race-winning attacks

```
Workout: Attack Simulation
20 min warm-up
Main set (repeat 3-4x):
  - 20 sec @ 180% FTP (attack)
  - 2 min @ 95% FTP (chase/hold)
  - 5 min recovery
15 min cool-down
Total: 65-75 min, TSS ~65-75
```

---

## Sprint & Neuromuscular

### Max Sprints
**Purpose:** Peak power, neuromuscular recruitment
**Target:** Maximum effort

```
Workout: Standing Starts
15 min warm-up
6-8 × 10 sec standing start sprints
  - Start from near-standstill
  - Maximum effort
  - 5 min full recovery between
15 min cool-down
Total: 60 min, TSS ~40
Notes: Full recovery essential for quality

Workout: Flying Sprints
15 min warm-up
6-8 × 15 sec sprints from 30 km/h
  - 5 min recovery
15 min cool-down
Total: 60 min, TSS ~40
```

### Sprint Repeatability
**Purpose:** Maintain sprint power when fatigued

```
Workout: Sprint Clusters
15 min warm-up
4 sets of:
  - 3 × 15 sec sprint (90 sec recovery between)
  - 5 min between sets
15 min cool-down
Total: 60 min, TSS ~50

Workout: Sprint-Threshold Combo
15 min warm-up
3 × 8 min @ 90% FTP with:
  - 10 sec sprint at 3 min and 6 min
  - 6 min recovery between sets
15 min cool-down
Total: 65 min, TSS ~70
```

---

## Cadence Training

### Scientific Basis (Ludyga et al. 2016, Whitty et al. 2016, Paton et al. 2009)

**High Cadence (100-120+ RPM):**
- Shifts load from muscular to cardiovascular system
- Improved pedaling smoothness and neural efficiency
- Reduced EEG spectral power (more efficient brain activity)

**Low Cadence (50-70 RPM):**
- Greater muscular strength development
- 97% testosterone increase vs 62% for high cadence (Paton 2009)
- 2.5% greater 60s power improvement
- Superior 15min TT performance in trained cyclists

### High Cadence Work

```
Workout: High Cadence Endurance
60 min @ 65% FTP maintaining 100-110 RPM
Focus: Smooth pedaling circles, no bouncing
Benefits: Improved neural efficiency

Workout: Spin-Ups
15 min warm-up
6 × 30 sec progressive cadence increase:
  - Start 90 RPM, finish 130+ RPM
  - Maintain smooth form
  - 2 min recovery
15 min cool-down
```

### Low Cadence Force Intervals

```
Workout: Force Repeats
15 min warm-up
6 × 5 min @ 85% FTP, 50-60 RPM (seated, big gear)
  - 3 min recovery @ self-selected cadence
15 min cool-down
Total: 70 min, TSS ~70
Notes: Builds muscular strength, testosterone response

Workout: Cadence Pyramid
15 min warm-up
Repeat 2-3×:
  - 5 min @ 70 RPM / 5 min @ 85 RPM / 5 min @ 100 RPM / 5 min @ 115 RPM
  - All at same power (75% FTP)
15 min cool-down
```

---

## Race-Specific Workouts

### Time Trial Simulation
**Purpose:** TT pacing, race preparation

```
Workout: 20km TT Simulation
20 min warm-up
25-35 min @ 95-102% FTP (simulate TT effort)
15 min cool-down
Total: 60-70 min, TSS ~75-90
Notes: Practice pacing strategy

Workout: Split TT Efforts
15 min warm-up
4 × 5 min @ 100-105% FTP (simulate pacing)
  - 2 min recovery
15 min cool-down
Total: 60 min, TSS ~70
```

### Criterium Simulation
**Purpose:** Repeated surges, race-specific fitness

```
Workout: Crit Simulation
20 min warm-up
30 min as:
  - 1 min @ 120% FTP
  - 2 min @ 85% FTP
  - Continuous rotation
15 min cool-down
Total: 65 min, TSS ~85

Workout: Corner Accelerations
15 min warm-up
20-30 × (20 sec @ 150% FTP / 40 sec @ 75% FTP)
15 min cool-down
Total: 50-60 min, TSS ~70
```

### Hill Repeat Simulation
**Purpose:** Climbing fitness, threshold at low cadence

```
Workout: Climbing Repeats
15 min warm-up
5 × 6 min @ 100% FTP, 60-70 rpm
  - 4 min recovery @ high cadence
15 min cool-down
Total: 75 min, TSS ~80
Notes: Simulate climbing cadence

Workout: Seated/Standing Mix
15 min warm-up
4 × 8 min as:
  - 2 min seated @ 95% FTP
  - 1 min standing @ 100% FTP
  - Repeat
  - 6 min recovery
15 min cool-down
Total: 75 min, TSS ~80
```

---

## Recovery Workouts

### Active Recovery
**Purpose:** Promote blood flow, minimal stress
**Target:** <55% FTP

```
Workout: Easy Spin
30-60 min @ 40-55% FTP
Cadence: Self-selected, comfortable
No intervals, no hard efforts
Goal: Feel better after than before
```

### Openers (Pre-Race)
**Purpose:** Activate systems before race/hard effort

```
Workout: Race Day Openers
15 min Zone 2
3 × 1 min build to Zone 4
5 min easy
3 × 30 sec @ 110% FTP (2 min recovery)
5 min easy
2 × 15 sec sprint (3 min recovery)
10 min cool-down
Total: 45 min, TSS ~30
Timing: 24-48 hours before race

Workout: Quick Openers (Race Morning)
10 min easy spinning
2 × 30 sec @ 105% FTP
5 min easy
1 × 10 sec sprint
5 min easy
Total: 25-30 min, TSS ~15
```

---

## Workout Selection Guide

| Goal | Primary Workouts | Frequency |
|------|-----------------|-----------|
| Build base | Z2 Endurance, Tempo | 3-5x/week |
| Raise FTP | Sweet Spot, Threshold | 2-3x/week |
| Improve VO2max | VO2max intervals | 2x/week |
| Peak for event | Race-specific, Openers | 1-2x/week |
| Maintain fitness | Mixed, reduced volume | 2-3x/week |

## TSS Estimates by Workout Type

| Workout Type | Duration | Approximate TSS |
|--------------|----------|-----------------|
| Recovery | 45-60 min | 25-35 |
| Endurance | 2-4 hours | 80-200 |
| Sweet Spot | 60-90 min | 70-95 |
| Threshold | 60-90 min | 80-100 |
| VO2max | 60-75 min | 70-90 |
| Sprints | 45-60 min | 35-50 |

---

## Key Research References

| Source | Year | Key Finding |
|--------|------|-------------|
| Yang et al. (PMID: 40605061) | 2025 | Network meta-analysis: optimal VO2max interval = 140s work, 0.85 ratio |
| Yu et al. (PMC12568352) | 2025 | TID review: polarized and pyramidal comparable for trained athletes |
| PMC11295100 | 2024 | 10-20-30 protocol: 6.4% VO2max, >80% adherence |
| Rønnestad et al. | 2020 | 30/15 intervals superior to 4×5min in elite cyclists |
| Tabata et al. | 1996 | Original Tabata: 28% anaerobic + 7 ml/kg/min VO2max |
| Ludyga et al. | 2016 | High cadence training improves neural efficiency |
| Whitty et al. | 2016 | Low cadence: superior 15min TT performance |
| Paton et al. | 2009 | Low cadence: 97% testosterone increase |
| Brooks (UC Berkeley) | - | Lactate shuttle theory for over-under intervals |
| Hoff & Helgerud | - | Norwegian 4×4 protocol development |

---

## Related Files

- [periodization.md](periodization.md) - How to fit workouts into training plan
- [zones-and-testing.md](zones-and-testing.md) - Power zones for setting workout intensity
- [physiology.md](physiology.md) - Physiological goals of different workout types
- [indoor-training.md](indoor-training.md) - Indoor trainer workout specifics
- [nutrition-recovery.md](nutrition-recovery.md) - Nutrition before/during/after workouts
