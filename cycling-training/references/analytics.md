# Training Analytics

Guide to training data analysis, metrics, and platforms.

## Table of Contents
1. [Core Metrics](#core-metrics)
2. [Power Duration Curve](#power-duration-curve)
3. [Training Load Management](#training-load-management)
4. [Training Platforms](#training-platforms)
5. [Analysis Workflows](#analysis-workflows)

---

## Key Research Summary

| Topic | Finding | Source |
|-------|---------|--------|
| Impulse-response model | Basis for CTL/ATL/TSB metrics | Banister (book) |
| ACWR and injury | Sweet spot 0.8-1.3 for injury prevention | Hulin et al. 2016 (PMID: 26511006) |
| Training load | High chronic loads are protective | Gabbett 2016 (PMID: 26758673) |
| Training load paradox | High chronic loads protective when built gradually | Gabbett 2020 (PMID: 32728962) |
| ACWR limitations | Rolling averages better than coupled ACWR | Lolli et al. 2019 (PMID: 30480461) |
| W' reconstitution | Models anaerobic reserve recovery | Skiba et al. 2012 (PMID: 22382171) |
| NP/TSS/IF | Power-based training metrics | Coggan & Allen (book) |

---

## Core Metrics

### Power Metrics

**Normalized Power (NP):**
```
Calculation: 30-sec rolling average, raised to 4th power, averaged, then 4th root
Purpose: Estimates metabolic cost of variable power
Use: More accurate than average power for intensity assessment
```

**Intensity Factor (IF):**
```
Formula: IF = NP / FTP
Interpretation:
- IF < 0.75: Recovery/endurance
- IF 0.75-0.85: Tempo
- IF 0.85-0.95: Sweet spot
- IF 0.95-1.05: Threshold
- IF > 1.05: Supra-threshold
```

**Variability Index (VI):**
```
Formula: VI = NP / Average Power
Interpretation:
- VI 1.0-1.02: Steady (TT, trainer)
- VI 1.02-1.06: Moderate variability
- VI 1.06-1.10: Variable (road race)
- VI > 1.10: Very variable (crit)
```

**Training Stress Score (TSS):**
```
Formula: TSS = (Duration × NP × IF) / (FTP × 3600) × 100

Guidelines:
- <150: Low fatigue, recover next day
- 150-300: Medium fatigue, some residual
- 300-450: High fatigue, 2 days to recover
- >450: Very high, several days recovery
```

### Heart Rate Metrics

**Efficiency Factor (EF):**
```
Formula: EF = NP / Average HR
Purpose: Tracks aerobic fitness over time
Trend: Should increase as fitness improves
Use: Compare similar workout types
```

**HR:Power Decoupling:**
```
Formula: (EF first half - EF second half) / EF first half × 100
Interpretation:
- <5%: Good aerobic fitness
- 5-10%: Moderate fitness
- >10%: Poor aerobic fitness or fatigue

Best measured on: 60-90 min steady endurance ride
```

**Heart Rate Variability (HRV):**
```
Metrics: RMSSD most commonly used
Morning measurement: Consistent time, conditions
Trend interpretation:
- Declining: Accumulated fatigue
- Stable/rising: Good recovery
Individual baseline most important
```

---

## Power Duration Curve

### Understanding PDC

**Definition:** Maximum power output for any given duration.

**Key durations:**
| Duration | Represents |
|----------|------------|
| 5 sec | Neuromuscular power |
| 30 sec | Peak anaerobic |
| 1 min | Anaerobic capacity |
| 5 min | VO2max/MAP |
| 20 min | FTP proxy |
| 60 min | True threshold |

### Power Profile Analysis

**Compare to reference:**
- Elite road: 6+ W/kg at 5 min
- Cat 1: 5-6 W/kg at 5 min
- Cat 2-3: 4-5 W/kg at 5 min
- Cat 4-5: 3-4 W/kg at 5 min

**Identify phenotype:**
- Sprinter: High short duration, steep drop
- TTer: Flatter curve, strong sustained
- All-rounder: Balanced profile

### Using PDC for Training

**Find limiters:**
1. Compare your curve to ideal/reference
2. Identify where you fall short
3. Target training to weaknesses

**Track progress:**
1. Overlay PDC from different periods
2. Note improvements at key durations
3. Watch for decay (needs attention)

### Mean Maximal Power (MMP)

**Definition:** Best power for a given duration over selected time period.

**Analysis:**
- Season best: Full season view
- Recent (90 days): Current fitness
- Last 28 days: Recent form

---

## Training Load Management

### Acute Training Load (ATL)

```
Calculation: 7-day exponentially weighted average of TSS
Represents: Fatigue
Typical ranges:
- Recovery: 40-60
- Building: 80-120
- Overreaching: 120-150+
```

### Chronic Training Load (CTL)

```
Calculation: 42-day exponentially weighted average of TSS
Represents: Fitness
Typical ranges by level:
- Recreational: 40-60
- Enthusiast: 60-80
- Competitive: 80-100
- Elite: 100-140+
```

### Training Stress Balance (TSB)

```
Formula: TSB = CTL - ATL
Represents: Form (freshness - fatigue)

Interpretation:
- Very negative (<-30): High fatigue
- Negative (-10 to -30): Building fitness
- Neutral (-10 to +10): Maintenance
- Positive (+10 to +30): Fresh/peaked
- Very positive (>+30): Detraining risk
```

### Acute:Chronic Workload Ratio (ACWR)

```
Formula: ACWR = ATL / CTL

Risk zones:
- <0.8: Underprepared (detraining)
- 0.8-1.3: Optimal loading zone
- 1.3-1.5: Elevated injury risk
- >1.5: High injury/overtraining risk
```

### Ramp Rate

```
Definition: Rate of CTL change
Formula: Weekly CTL gain

Guidelines:
- Conservative: 3-5 pts/week
- Moderate: 5-7 pts/week
- Aggressive: 7-10 pts/week
- Dangerous: >10 pts/week
```

### Performance Management Chart (PMC)

**Components:**
- Blue line: CTL (fitness)
- Pink line: ATL (fatigue)
- Yellow line: TSB (form)

**Using PMC:**
1. Build CTL gradually before key events
2. Watch for excessive negative TSB
3. Time taper to achieve positive TSB for races
4. Monitor ramp rate

---

## Training Platforms

For detailed platform comparison and setup guidance, see [platforms.md](platforms.md).

**Quick reference:**

| Platform | Best For |
|----------|----------|
| TrainerRoad | Structured training, AI adaptation |
| intervals.icu | Budget-conscious, comprehensive analytics |
| WKO5 | Deep analysis, power profiling |
| Strava | Social, segment tracking |

---

## Analysis Workflows

### Weekly Review

```
1. Total volume vs planned
   - Hours achieved
   - TSS achieved
   - Key workouts completed

2. Intensity distribution
   - Time in each zone
   - Compare to target distribution
   - Identify grey zone creep

3. Key workout quality
   - Hit power targets?
   - HR response appropriate?
   - RPE aligned with data?

4. Fatigue indicators
   - TSB trend
   - HRV trend
   - Subjective feel

5. Adjustments needed
   - Next week modifications
   - Recovery needs
```

### Monthly Review

```
1. CTL progression
   - On target?
   - Appropriate ramp rate?

2. Power curve changes
   - Improvements at key durations?
   - Any regressions?

3. Training distribution
   - Aligned with plan?
   - Appropriate for phase?

4. Health/fatigue
   - Any overtraining signs?
   - Illness/injury?

5. Goal tracking
   - On track for season goals?
   - Adjustments needed?
```

### Post-Workout Analysis

```
Endurance ride:
- HR:power decoupling
- Efficiency factor
- Nutrition/hydration success

Interval session:
- Hit power targets?
- Consistency between intervals
- Recovery quality
- Total time at target intensity

Race/hard effort:
- Pacing analysis (VI)
- Power distribution
- Limiters identified
- Tactical execution
```

### Season Analysis

```
1. FTP progression
   - Peak vs start of season
   - Timing of peak

2. Power profile changes
   - Strengths developed
   - Weaknesses addressed

3. Racing performance
   - Results vs training
   - Patterns identified

4. Training load
   - Total volume
   - Distribution
   - Periodization effectiveness

5. Lessons for next season
   - What worked
   - What to change
```

---

## Advanced Metrics

### W' Balance (W'bal)

```
Tracks: Remaining anaerobic capacity
Formula: Complex - accounts for expenditure and recovery
Use: Real-time racing decisions
Platforms: WKO5, Golden Cheetah, some head units
```

### Functional Reserve Capacity (FRC)

```
WKO5 metric
Similar to W' but modeled differently
Represents: Anaerobic work capacity above FTP
Use: Power profiling, workout prescription
```

### Stamina

```
WKO5 metric
Definition: Ability to maintain percentage of peak power
Higher = better fatigue resistance
Training: Long rides, tempo work
```

### Time to Exhaustion (TTE)

```
Definition: How long you can hold FTP
Typical: 30-70 minutes
Training: Threshold intervals, sweet spot
Tracking: Improves with training
```

### Pmax

```
Definition: Maximum instantaneous power
Measured: Very short (<5 sec) maximal effort
Training: Sprints, neuromuscular work
Use: Sprint profiling, race tactics
```

---

## Concrete Analysis Example

### Sample Athlete Data

**Athlete Profile:**
- FTP: 280W
- Current CTL: 72
- Target event: Gran Fondo in 8 weeks

**Last Week's Training:**

| Day | Workout | Duration | TSS | IF | Notes |
|-----|---------|----------|-----|-----|-------|
| Mon | Rest | - | 0 | - | - |
| Tue | Sweet Spot | 75 min | 82 | 0.88 | Indoor, ERG |
| Wed | Recovery | 45 min | 25 | 0.52 | Z1 spin |
| Thu | VO2max | 65 min | 78 | 0.91 | 5×4min @ 310W |
| Fri | Rest | - | 0 | - | - |
| Sat | Group Ride | 3h | 185 | 0.78 | Outdoor, variable |
| Sun | Endurance | 2h | 95 | 0.68 | Steady Z2 |
| **Total** | | **9h 25min** | **465** | | |

### Analysis Walkthrough

**1. Weekly Load Assessment:**
```
Weekly TSS: 465
Target for CTL 72 athlete: 450-550 ✓
ACWR: (465/7) / 72 = 0.92 ✓ (in sweet spot 0.8-1.3)
CTL trend: Will increase ~5-6 points this week
```

**2. Intensity Distribution:**
```
Z1-2 (recovery + endurance): 45 + 95 = 140 TSS (30%)
Z3-4 (tempo + threshold): 82 + 78 = 160 TSS (34%)  ⚠️
Z5+ (VO2max + group ride surges): ~165 TSS (36%)

Issue: Too much time in "grey zone" (Z3-4)
Recommendation: Replace one SS session with pure Z2
```

**3. Indoor vs Outdoor Balance:**
```
Indoor: 75 + 45 + 65 = 185 min (33%)
Outdoor: 3h + 2h = 300 min (67%)

Good balance for someone training primarily outdoors.
If >50% indoor, would recommend indoor FTP test.
```

**4. Progression Check (vs previous weeks):**
```
Week -3: 420 TSS
Week -2: 445 TSS
Week -1: 465 TSS
Week 0: 465 TSS (current)

Trend: Steady progression (+5%/week) ✓
Ready for: 485-500 TSS next week
Deload needed: Week 4 (reduce to 280-300 TSS)
```

**5. Key Workout Review - Thursday VO2max:**
```
Prescription: 5×4min @ 106-110% FTP (298-308W)
Actual: 5×4min @ 310W avg (111% FTP)
IF: 0.91 (target was ~0.90)

Assessment: Slightly over-paced but acceptable
HR response: 175 bpm avg (97% max) - good VO2max stimulus
Recovery intervals: 50% FTP maintained ✓
```

**6. Recommendations for Next Week:**
1. Increase total TSS to 485-500
2. Add 30 min to Sunday endurance ride
3. Consider replacing Tue SS with pure Z2 (polarization)
4. Thursday VO2max: Same prescription, slightly lower target (305W)
