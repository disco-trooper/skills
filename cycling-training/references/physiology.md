# Cycling Physiology

Key physiological concepts for cycling performance based on peer-reviewed research.

## Key Research Summary

| Topic | Finding | Source |
|-------|---------|--------|
| VO2max trainability | Both polarized and threshold training effective | Multiple meta-analyses |
| VO2 kinetics | Trained tau: 15-25s vs untrained 30-45s | Murias et al. 2011 (PMID: 21461928) |
| W' reconstitution | Time constants vary individually | Skiba et al. 2012 (PMID: 22382171) |
| W' sex differences | LBM-normalized W'REC similar in men/women | Bourgois et al. 2023 (PMID: 37369796) |
| CP/W' team pursuit | CP and W' recovery rate differentiate performance | Pugh et al. 2022 (PMID: 36068071) |
| W' model elite cyclists | Bartram adjustment improves W'bal modeling | Bartram et al. 2022 (PMID: 34560664) |
| W' recovery intensity | Below 50% FTP no further W' reconstitution benefit | Chorley et al. 2023 (PMID: 36820074) |
| Fractional utilization | Elite: 80-90%+ of VO2max at threshold | Joyner & Coyle 2008 (PMID: 17901124) |
| Gross efficiency | 18-25%, elite often 22-25% | Hopker et al. 2016 (PMC4893037) |
| HRV-guided training | Improved performance vs traditional | Javaloyes et al. 2019 (PMID: 29809080) |

*Note: Specific percentage improvements vary by study and individual.*

## Table of Contents

### Core Physiology
1. [VO2max](#vo2max) - Definition, values, trainability, testing, kinetics
2. [Lactate Thresholds](#lactate-thresholds) - LT1, LT2, MLSS, fractional utilization
3. [Critical Power Model](#critical-power-model) - CP, W', reconstitution, applications

### Performance Factors
4. [Efficiency and Economy](#efficiency-and-economy) - Gross efficiency, cadence
5. [Fatigue Mechanisms](#fatigue-mechanisms) - Central, peripheral, glycogen, heat
6. [Adaptations to Training](#adaptations-to-training) - Cardiovascular, muscular, detraining

### Analysis Tools
7. [Power Duration Curve](#power-duration-curve) - Phenotype identification, limiters
8. [Heart Rate Variability](#heart-rate-variability) - HRV metrics, monitoring, guided training

**Quick Jump:** [Research Summary](#key-research-summary) | [Related Files](#related-files)

---

## VO2max

### Definition

**VO2max** = Maximum rate of oxygen consumption during maximal exercise.

Units: mL/kg/min (relative) or L/min (absolute)

### Typical Values

| Category | VO2max (mL/kg/min) |
|----------|-------------------|
| Untrained male | 35-45 |
| Recreational cyclist | 45-55 |
| Trained cyclist | 55-65 |
| Competitive amateur | 60-70 |
| Elite amateur | 65-75 |
| Professional | 70-85+ |

**World-class cyclists:** 80-90+ mL/kg/min

### Determinants of VO2max

1. **Cardiac output** (heart rate × stroke volume)
   - Primary limiter in most individuals
   - Stroke volume more trainable than max HR

2. **Oxygen-carrying capacity**
   - Hemoglobin mass
   - Blood volume

3. **Peripheral oxygen extraction**
   - Muscle capillary density
   - Mitochondrial content
   - Oxidative enzyme activity

### Trainability

**Beginner:** +15-25% improvement possible
**Trained:** +5-10% improvement
**Elite:** +1-3% (small margins)

**Time course:**
- Initial gains: 4-8 weeks
- Continued improvement: 6-12 months
- Plateau: Depends on genetic ceiling

### Testing VO2max

**Laboratory:**
- Gold standard: Metabolic cart during ramp test
- Provides: VO2max, VT1, VT2, max HR

**Field estimates:**
- From ramp test: Less accurate but useful
- From race/TT data: Correlates with performance
- WKO5/Xert modeling: Estimates from power data

### VO2max Workouts

See [workouts.md](workouts.md) for specific protocols.

**Effective approaches:**
- Intervals at 90-100% VO2max power
- Duration: 3-8 minutes per interval
- Work:rest typically 1:1
- Total time at VO2max: 15-30 min per session

### VO2 Kinetics

**Definition:** Rate at which oxygen uptake adjusts to metabolic demand.

**Three phases:**
1. **Phase I (cardiodynamic)**: 15-25 sec, reflects pulmonary blood flow
2. **Phase II (primary)**: Exponential rise, muscle oxygen uptake
3. **Phase III**: Steady state or slow component (intensity dependent)

**Time Constant (tau/τ):**
| Training Status | Tau (seconds) |
|-----------------|---------------|
| Untrained | 30-45+ |
| Recreational | 25-35 |
| Trained cyclists | 15-25 |
| Elite | 12-18 |

**Faster kinetics benefits:**
- Earlier oxygen delivery to muscles
- Reduced anaerobic contribution at start
- Better performance in repeated efforts

**Training to improve kinetics:**
- High-intensity interval training
- Priming exercise (moderate warm-up bout)
- Training at intensities accumulating time at VO2max

---

## Lactate Thresholds

### LT1 (First Lactate Threshold / VT1)

**Definition:** Intensity where lactate begins to rise above baseline.

**Characteristics:**
- ~55-75% of VO2max
- Can be sustained for many hours
- "All day" pace
- Corresponds to Z2/Z3 boundary

**Markers:**
- Blood lactate ~2 mmol/L
- First ventilatory threshold (VT1)
- Can still talk comfortably

### LT2 (Second Lactate Threshold / MLSS / VT2)

**Definition:** Maximum intensity where lactate production equals clearance.

**Characteristics:**
- ~75-90% of VO2max
- Sustainable for 30-60 minutes
- "Threshold" effort
- Corresponds to FTP

**Markers:**
- Blood lactate ~4 mmol/L (individual variation 2-8)
- Second ventilatory threshold (VT2)
- Difficult to speak

### MLSS (Maximal Lactate Steady State)

**Definition:** Highest intensity with stable lactate over 30+ min.

**Relationship to FTP:**
- FTP ≈ MLSS power in most athletes
- Some variation: FTP may be slightly above or below true MLSS

**Testing:**
- Multiple 30-min efforts at different powers
- Find power where lactate stabilizes

### Fractional Utilization

**Definition:** % of VO2max at threshold.

**Typical values:**
- Untrained: 50-60%
- Trained: 70-80%
- Elite: 80-90%

**Trainability:**
- Highly trainable (more than VO2max)
- Primary target of threshold training
- Improves with aerobic training

### Improving Lactate Thresholds

**LT1 improvement:**
- High-volume Z2 training
- Long rides
- Takes months/years

**LT2 improvement:**
- Sweet spot training
- Threshold intervals
- Over-unders
- Response in weeks/months

---

## Critical Power Model

### Fundamentals

**Two-component model:**
1. **CP (Critical Power):** Aerobic power ceiling
2. **W' (W-prime):** Anaerobic work capacity (kJ)

### Mathematical Relationship

```
Time to exhaustion = W' / (P - CP)

Work above CP = W'
Once W' depleted = exhaustion
```

### W' Reconstitution

**Recovery of W' during sub-CP efforts:**

```
W'bal = W' - Σ(W' expended) + Σ(W' reconstituted)
```

**Recovery rate factors:**
- Intensity of recovery (lower = faster)
- Individual variation
- Training status
- Fatigue state

### Practical Applications

**Pacing hilly TT:**
- Know your W' budget
- Don't deplete fully on first climb
- Plan efforts to finish with ~0 W'bal

**Racing tactics:**
- Attacks cost W'
- Recovery in peloton rebuilds W'
- Know when you can vs can't respond

**Interval training:**
- Long intervals deplete W'
- Short intervals may not
- Informs workout design

### CP vs FTP

| Metric | Typical Relationship |
|--------|---------------------|
| CP | 100% (reference) |
| FTP (20min × 0.95) | 95-102% of CP |
| 60-min power | 95-100% of CP |

**Note:** CP is typically slightly higher than FTP.

### Testing CP/W'

**3-minute all-out test:**
- After warm-up, go all-out for 3 min
- CP = average power of final 30 sec
- W' = work above CP during entire effort

**Multiple duration tests:**
- 3-min, 10-min, 20-min efforts
- Mathematical fitting to power-duration curve

---

## Efficiency and Economy

### Gross Efficiency (GE)

**Definition:** Work output ÷ energy expenditure

**Formula:**
```
GE = (Power output × 60) / (VO2 × 20.9)
```

**Typical values:**
- Untrained: 18-20%
- Trained: 20-22%
- Elite: 22-25%

**Factors affecting GE:**
- Muscle fiber type (Type I more efficient)
- Cadence (individual optimal)
- Training
- Fatigue (decreases GE)

### Cycling Economy

**Definition:** Oxygen cost to produce a given power output.

**Units:** mL O2/min/watt

**Lower = better economy**

### Trainability

**Factors that improve efficiency:**
- Long-term endurance training
- Technique/pedaling smoothness
- Optimal bike fit
- Appropriate cadence
- Strength training (possibly)

### Cadence Considerations

**Metabolic cost vs neuromuscular cost:**
- Low cadence: Higher muscular stress, lower cardiovascular
- High cadence: Lower muscular stress, higher cardiovascular

**Self-selected cadence:**
- Usually close to optimal for individual
- Typically 80-100 rpm on flat
- May be lower on climbs (60-80)

**Research findings:**
- Highly trained may benefit from higher cadence
- Individual variation significant
- Don't force unnatural cadence

---

## Fatigue Mechanisms

### Central Fatigue

**Location:** Brain and spinal cord

**Mechanisms:**
- Reduced motor unit recruitment
- Decreased neural drive
- Neurotransmitter depletion (serotonin, dopamine)

**Characterized by:**
- Reduced motivation
- Perception of effort
- Sleep-like brain patterns

### Peripheral Fatigue

**Location:** Muscles

**Mechanisms:**
- Glycogen depletion
- Metabolite accumulation (H+, Pi)
- Calcium handling impairment
- Substrate depletion

**Characterized by:**
- Muscle weakness
- Inability to generate force
- Muscle soreness

### Glycogen Depletion

**Effect on performance:**
- Muscle glycogen critical for high-intensity
- Liver glycogen critical for blood glucose
- "Bonking" = severe glycogen depletion

**Prevention:**
- Adequate carb intake
- Fueling during rides
- Train gut to absorb carbs

### Heat and Dehydration

**Effects:**
- Reduced blood volume
- Increased HR for same power
- Reduced muscle blood flow
- Impaired thermoregulation

**Thresholds:**
- >2% dehydration: Performance impairment
- >3-4%: Significant impairment
- >5%: Dangerous

---

## Adaptations to Training

### Cardiovascular Adaptations

| Adaptation | Effect |
|------------|--------|
| ↑ Stroke volume | More blood per beat |
| ↑ Blood volume | Better oxygen delivery |
| ↑ Hemoglobin mass | More oxygen carrying |
| ↓ Resting HR | More efficient heart |
| ↑ Capillary density | Better muscle perfusion |

### Muscular Adaptations

| Adaptation | Effect |
|------------|--------|
| ↑ Mitochondrial density | More aerobic capacity |
| ↑ Oxidative enzymes | Faster aerobic metabolism |
| ↑ Fat oxidation | Spare glycogen |
| ↑ Glycogen storage | More fuel capacity |
| ↑ Lactate clearance | Higher threshold |

### Time Course of Adaptations

| Adaptation | Time to Develop |
|------------|-----------------|
| Neural (coordination) | Days-weeks |
| Blood volume | 1-2 weeks |
| Mitochondrial enzymes | 2-6 weeks |
| Capillary density | 4-8 weeks |
| Cardiac remodeling | Months |
| Hemoglobin mass | Months (or altitude) |

### Detraining

**How quickly fitness is lost:**

| Time Off | Fitness Loss |
|----------|--------------|
| 1 week | Minimal |
| 2 weeks | 5-10% VO2max |
| 4 weeks | 15-20% VO2max |
| 8 weeks | 25-30% VO2max |

**What's lost first:**
1. Blood volume (fast)
2. Muscle enzyme activity
3. Mitochondrial density
4. Capillary density (slower)

**Maintenance:**
- 2-3 sessions/week can maintain fitness
- Intensity more important than volume for maintenance

### Potential Maladaptation at Extreme Volumes

**Research (La Gerche et al. 2012, PMID: 22160404):**
Chronic extreme endurance training may lead to adverse remodeling in some individuals:

| Structure | Change | Clinical Significance |
|-----------|--------|----------------------|
| Right ventricle | Dilation | Substrate for arrhythmias |
| Right atrium | Enlargement | Risk of atrial fibrillation |
| Myocardium | Focal fibrosis | Arrhythmogenic substrate |

**Acute changes after demanding races:**
- Troponin I: May rise 50-100× (normalizes 24-72h)
- T1 relaxation time: Prolongation (possible transient edema)
- Right ventricle: Transient dysfunction (normalizes 7-10 days)

**Key factors:**
- Cumulative "dose" of intensive training over lifetime
- Individual susceptibility (genetics)
- Insufficient recovery between intensive blocks

→ See [injuries.md#cardiovascular-risks-of-endurance-training](injuries.md#cardiovascular-risks-of-endurance-training) for practical recommendations

---

## Power Duration Curve

### Understanding PDC

**Definition:** Maximum power achievable for any given duration.

**Key points:**
- 5 sec: Neuromuscular power (sprint)
- 1 min: Anaerobic capacity
- 5 min: MAP/VO2max power
- 20-60 min: Threshold/FTP
- 60+ min: Aerobic endurance

### Phenotype Identification

**Sprinter profile:**
- Very high 5-15 sec power
- Steep drop-off to FTP
- High W'

**Pursuiter profile:**
- Balanced across durations
- Strong 3-5 min power
- Moderate W'

**Time trialist profile:**
- Relatively flat curve
- Strong sustained power
- Lower W', very high CP

**Climber profile:**
- High W/kg at all durations
- May have lower absolute power
- Excellent efficiency

### Using PDC for Training

**Identify limiters:**
- Compare to reference curves
- Find where you fall off
- Target training to weaknesses

**Track progress:**
- Monitor peak powers over time
- Look for improvements at target durations
- Note decay (needs attention)

---

## Heart Rate Variability (HRV)

### Key Concepts

**Definition:** Variation in time intervals between consecutive heartbeats (R-R intervals).

**What it reflects:**
- Autonomic nervous system balance
- Sympathetic vs parasympathetic activity
- Higher HRV = better recovery/readiness
- Lower HRV = fatigue, stress, illness

### Common HRV Metrics

| Metric | Type | Description |
|--------|------|-------------|
| **RMSSD** | Time domain | Most used; parasympathetic activity |
| **SDNN** | Time domain | Overall variability |
| **HF** | Frequency | 0.15-0.4 Hz; parasympathetic |
| **LF** | Frequency | 0.04-0.15 Hz; mixed |

### Monitoring Protocol

```
When: Immediately upon waking
Position: Supine (lying down)
Duration: 1-5 minutes
Device: Chest strap or validated optical
Consistency: Same conditions daily
```

### HRV-Guided Training (Javaloyes et al. 2019)

**Study results (17 well-trained cyclists, 8 weeks):**
- Peak power output: +5.1%
- Power at VT2: +13.9%
- 40-min time trial: +7.3%
- Traditional group: No significant improvement

### Interpretation Model

| HRV Status | Color | Training Recommendation |
|------------|-------|------------------------|
| Normal/elevated | Green | Ready for high-intensity |
| Slightly below baseline | Yellow | Moderate training OK |
| Significantly suppressed | Red | Recovery day |

### Practical Guidelines

**Establish baseline:**
- 4-8 weeks of consistent measurement
- Calculate rolling 7-day average
- Note individual patterns

**Decision making:**
- Use trends, not single readings
- Combine with RPE, sleep quality
- Multiple factors affect HRV (caffeine, alcohol, stress)

**Limitations:**
- High inter-individual variability
- May not be sensitive in highly trained athletes
- Requires consistent measurement conditions

---

## Related Files

- [zones-and-testing.md](zones-and-testing.md) - Practical application of physiological concepts to zones and testing
- [periodization.md](periodization.md) - How to structure training for physiological adaptations
- [workouts.md](workouts.md) - Specific protocols targeting physiological systems
- [nutrition-recovery.md](nutrition-recovery.md) - Nutrition and recovery supporting physiological adaptations
