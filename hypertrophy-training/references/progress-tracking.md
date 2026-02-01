# Progress Tracking for Hypertrophy

## Table of Contents
1. [What to Track](#what-to-track)
2. [Measurement Methods](#measurement-methods)
3. [Training Log](#training-log)
4. [Apps and Tools](#apps-and-tools)
5. [Photo Documentation](#photo-documentation)
6. [Data Interpretation](#data-interpretation)

---

## What to Track

### Primary Metrics

| Metric | Frequency | Priority |
|--------|-----------|----------|
| Training progression (weights, reps) | Every workout | Critical |
| Body weight | Daily (weekly average) | High |
| Body measurements | 2-4 weeks | Medium |
| Photos | 4-8 weeks | Medium |
| Subjective assessment | Daily | Medium |

### Secondary Metrics

- Sleep quality
- Energy levels
- Soreness level
- Appetite

---

## Measurement Methods

### Body Weight

**Protocol:**
1. Morning, after waking
2. After bathroom, before food/drink
3. In underwear or naked
4. Same scale, same location

**Interpretation:** Weekly average, not daily fluctuations

### Body Measurements

**Standard measurements:**

| Location | How to Measure |
|----------|----------------|
| Chest | Across nipples, normal exhale |
| Biceps | Relaxed, mid-upper arm |
| Biceps (flexed) | Contracted, peak |
| Waist | At navel, relaxed |
| Hips | Widest point |
| Thigh | 15cm above knee |
| Calf | Widest point |

**Tips:**
- Always measure same side
- Don't pull tape tight
- Morning, before training

### Strength / Performance

**1RM Tracking:**
- Direct testing (every 8-12 weeks)
- Estimation from submax (every workout)

**Formulas for 1RM estimate:**
```
1RM = Weight × (1 + Reps/30)  [Epley]
1RM = Weight × (36 / (37 - Reps))  [Brzycki]
```

---

## Training Log

### What to Record

```
Date: 2026-01-31
Workout: Push A
Weight: 82.3 kg
Sleep: 7.5h (quality 8/10)
Energy: 7/10

Exercises:
1. Bench Press
   - Warm-up: 60×10, 80×5, 90×3
   - 100kg × 8, 8, 7 (RIR: 2, 2, 1)
   - Note: Left triceps fatigued

2. Incline DB Press
   - 32kg × 10, 10, 9 (RIR: 2, 2, 1)

[...]

Overall rating: 8/10
Notes: Good pump, solid form
```

### Volume Tracking

Count weekly sets per muscle group:

| Muscle | Mon | Tue | Wed | Thu | Fri | Sat | Weekly |
|--------|-----|-----|-----|-----|-----|-----|--------|
| Chest | 9 | - | - | 6 | - | - | 15 |
| Back | - | 12 | - | - | 10 | - | 22 |
| ... |

---

## Apps and Tools

### Recommended Apps

| App | Platform | Specialty | Price |
|-----|----------|-----------|-------|
| Strong | iOS/Android | Tracking workouts | Free/Premium |
| Hevy | iOS/Android | Social + tracking | Free/Premium |
| JEFIT | iOS/Android | Exercise library | Free/Premium |
| Google Sheets | Web | Custom tracking | Free |
| Notion | Web/App | Comprehensive notes | Free |

### Excel/Sheets Template

Basic columns:
- Date
- Exercise
- Weight
- Reps
- RIR/RPE
- Volume (weight × reps)
- Notes

### Automatic Calculations

```
=SUMIF(exercise_range, "Bench Press", volume_range)  // Weekly volume for exercise
=AVERAGE(weight_week)  // Average weight
```

---

## Photo Documentation

### Standardization

**Positions:**
1. Front (relaxed)
2. Front (double biceps)
3. Side
4. Back (relaxed)
5. Back (lat spread)

**Conditions:**
- Same lighting
- Same time of day (ideally morning)
- Same distance from mirror/camera
- Neutral background

**Frequency:** Every 4-8 weeks

---

## Data Interpretation

### Barbell Weight Progression

| Situation | Interpretation | Action |
|-----------|----------------|--------|
| +Reps every week | Excellent progress | Continue |
| Stagnation 1-2 weeks | Normal | Monitor |
| Stagnation 3+ weeks | Plateau | Change stimulus |
| Performance drop | Fatigue/regression | Deload |

### Body Weight

**Bulking:**
- Goal: +0.25-0.5% BW/week
- Faster = more fat
- Slower = possibly not enough food

**Cutting:**
- Goal: -0.5-1% BW/week
- Faster = risk of muscle loss
- Slower = longer in deficit

### Red Flags

- Performance drops during bulk
- Strength loss >10% during cut
- Weight stagnates 3+ weeks (both phases)
- Fatigue doesn't decrease after deload

---

## See Also

- **Volume landmarks:** See SKILL.md Section 1.2 for MEV/MAV/MRV
- **Periodization tracking:** See `periodization.md` for mesocycle structure
- **Body composition:** See `nutrition.md` for bulk/cut strategies
