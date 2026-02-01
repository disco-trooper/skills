# Training Platforms

Overview and comparison of cycling training platforms.

## Table of Contents
1. [Platform Comparison Matrix](#platform-comparison-matrix)
2. [TrainerRoad](#trainerroad)
3. [TrainingPeaks](#trainingpeaks)
4. [WKO5](#wko5)
5. [intervals.icu](#intervalsicu)
6. [Golden Cheetah](#golden-cheetah)
7. [Strava](#strava)
8. [Xert](#xert)
9. [SYSTM (Wahoo)](#systm-wahoo)
10. [Platform Integration Strategy](#platform-integration-strategy)

---

## Platform Comparison Matrix

| Platform | FTP Method | Adaptivity | Best For | Price |
|----------|------------|------------|----------|-------|
| TrainerRoad | AI FTP Detection | Real-time AI | Structured training | $22/mo |
| Zwift | Ramp Test | None | Motivation, racing | $20/mo |
| SYSTM | 4DP (4 metrics) | Moderate | Holistic training | $15/mo |
| Xert | Breakthrough | Real-time MPA | Data-driven athletes | $10/mo |
| intervals.icu | eFTP auto | None | Self-coached, analytics | Free/$4 |
| Golden Cheetah | CP/W' manual | N/A | Power users | Free |
| JOIN | eFTP auto | Real-time | Schedule flexibility | $15/mo |

---

## TrainerRoad

**Unique features:**
- AI FTP Detection (250M+ activities ML model)
- Progression Levels (1-10 per zone)
- Adaptive Training (adjusts based on completed workouts)
- 27% improvement in workout appropriateness (2025)

**Strengths:**
- Most sophisticated AI adaptation
- Extensive workout library
- Integrates with Zwift
- Eliminates FTP testing

**Best for:** Athletes wanting structured, adaptive training with minimal decision-making

---

## TrainingPeaks

**Strengths:**
- Industry standard PMC
- Coach/athlete sharing
- Calendar integration
- Workout library

**Key features:**
- TSS, IF, NP calculations
- PMC tracking
- Season planning
- Annual Training Plan (ATP)

**Best for:** Athletes working with coaches, long-term planning

---

## WKO5

**Strengths:**
- Advanced analytics
- Individual modeling
- Power profiling

**Key features:**
- iLevels (individualized zones)
- mFTP (modeled FTP)
- Power-Duration modeling
- Phenotype identification
- TTE (time to exhaustion) curves

**Best for:** Data-driven athletes wanting deep analysis

---

## intervals.icu

**Strengths:**
- Free
- Comprehensive analytics
- Active development
- Community

**Key features:**
- All standard metrics
- PMC
- Calendar
- Power curves
- Custom charts
- Fitness/freshness modeling

**Best for:** Budget-conscious athletes, excellent value

---

## Golden Cheetah

**Strengths:**
- Free, open source
- Highly customizable
- Advanced metrics

**Key features:**
- CP/W' modeling
- Custom charts
- Batch analysis
- Scientific rigor

**Best for:** Technical users, researchers

---

## Strava

**Strengths:**
- Social features
- Segment tracking
- Wide adoption

**Limitations:**
- Basic analytics
- Relative effort (not TSS)
- Limited training load tracking

**Best for:** Social, segment hunting (use with dedicated platform)

---

## Xert

**Unique approach:**
- Fitness Signature: TP (threshold), HIE (W'), PP (peak)
- MPA (Maximum Power Available) - real-time fatigue tracking
- Breakthrough detection - no formal testing needed
- XSS replaces TSS with energy system breakdown

**Key concepts:**
- MPA drops when above threshold, recovers below
- Smart Intervals scale to exact athlete signature
- XATA advisor for personalized recommendations

**Best for:** Data-driven athletes wanting sophisticated fatigue modeling

---

## SYSTM (Wahoo)

**4DP system (Four-Dimensional Power):**
1. NM (Neuromuscular) - 5-15s sprint
2. AC (Anaerobic Capacity) - 1min attack
3. MAP (Maximal Aerobic) - 3-8min VO2max
4. FTP (Threshold) - 1hr sustainable

**Rider Types:** Sprinter, Attacker, Pursuiter, Rouleur, Climber, TTer

**Best for:** Athletes wanting holistic training (cycling + strength + mental)

---

## Platform Integration Strategy

**Recommended approach:**
1. Primary data: Wahoo/Garmin (device)
2. Analysis: intervals.icu or WKO5
3. Planning: TrainingPeaks or intervals.icu
4. Social: Strava (auto-sync)

**Typical setups:**

| Athlete Type | Devices | Analysis | Training |
|--------------|---------|----------|----------|
| Budget-conscious | Garmin/Wahoo | intervals.icu | intervals.icu |
| Data-driven | Smart trainer | WKO5 + intervals.icu | TrainerRoad |
| Coach-led | Any | TrainingPeaks | Coach-prescribed |
| Casual/Social | Any | Strava | Zwift |

---

## Related Files

- [analytics.md](analytics.md) - Training metrics and analysis workflows
- [zones-and-testing.md](zones-and-testing.md) - FTP testing protocols
- [indoor-training.md](indoor-training.md) - Indoor trainer setup
