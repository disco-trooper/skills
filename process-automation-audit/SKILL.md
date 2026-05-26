---
name: process-automation-audit
description: Scope, sell, run, and package paid audits for manual business process automation. Use when Codex needs to help with discovery, scoping, pricing, stakeholder questions, process maps, audit deliverables, pilot proposals, or negotiation boundaries for automating operational workflows such as invoices, price lists, ERP/SAP handoffs, warehouse/inventory, approvals, spreadsheets, OCR, AI-assisted document handling, or other repetitive administrative processes. Also use when deciding what is free discovery versus paid audit work.
---

# Process Automation Audit

Use this skill to turn broad automation interest into a bounded paid engagement. It combines business analysis, pricing discipline, and negotiation boundaries.

## Core Rule

Free work helps the client decide whether to continue. Paid work explains exactly how to continue.

## Engagement Ladder

1. **Intro discovery** - free or relationship-led. Understand context, pain, people, systems, and candidate processes.
2. **Scoping call** - usually free, tightly limited. Review provided materials enough to prepare questions and decide the paid next step.
3. **Paid audit** - map the process, quantify pain, identify options, define pilot scope, risks, assumptions, and rough implementation path.
4. **Paid pilot** - build or simulate a narrow workflow on real or anonymized data.
5. **Implementation** - production system, integrations, rollout, support.

Never let step 2 silently become step 3.

## Free vs Paid Boundary

Free is acceptable:

- read materials at a skim level,
- identify missing information,
- prepare questions,
- hold one bounded scoping call,
- recommend whether the next paid step should be an audit, roadmap, or pilot.

Paid audit begins when asked to produce:

- documented process map or analysis deliverable,
- detailed current-state analysis,
- target-state workflow,
- technology approach,
- business case,
- implementation estimate,
- pilot specification,
- vendor/SAP/ERP recommendation,
- written report with actionable recommendations.

Use this line when needed:

```text
The next useful step is no longer just understanding the topic. It is analyzing the process and producing a recommendation. I would treat that as a separate paid audit.
```

## Choose The Right Offer

- **Quick scan**: client is small, trust is early, or the goal is a light directional memo without detailed process mapping.
- **Single-process audit**: one process is likely first, but details are unclear. Example: received invoices, supplier price lists, warehouse inventory.
- **Digitalization roadmap**: client has many competing areas and leadership needs prioritization. Example: invoices + price lists + warehouse + CRM + portal.
- **Pilot**: process is already clear, data exists, owner is assigned, and success criteria are known.

Default to audit when uncertain. Do not sell a pilot before the process is understood.

## Discovery Checklist

For each candidate process, identify:

- owner,
- users,
- trigger/input,
- current steps,
- systems and files,
- manual handoffs,
- decision rules,
- exceptions,
- volume/frequency,
- time cost,
- error/rework cost,
- compliance/security constraints,
- desired output,
- success metric.

If any of owner, data, current steps, or success metric is missing, recommend audit before pilot.

## Pricing Heuristic

Use value-based fixed pricing for audit packages; do not price only by hourly effort.

Indicative Czech SMB/mid-market ranges:

- quick scan: low tens of thousands CZK,
- single-process audit: roughly 35-75k CZK,
- broader roadmap: roughly 60-120k CZK,
- pilot: usually higher tens to low hundreds of thousands CZK, depending on integrations and data.

Treat these ranges as directional, not timeless. If the user asks for market validation, current rates, competitor pricing, or "am I outside the market?", browse current sources and cite them.

Adjust upward for SAP/ERP complexity, many stakeholders, multiple locations, sensitive data, or board-level deliverables. Adjust downward only by reducing scope, not by discounting the same output.

Never use a client's internal investment estimates as your anchor unless they mention them first.

## Deliverable Standards

A paid audit should produce:

- executive summary,
- current-state process map,
- pain points and waste,
- data/input inventory,
- roles and ownership,
- rules and exceptions,
- automation opportunities,
- recommended first pilot,
- out-of-scope items,
- assumptions and risks,
- rough next-step estimate or pricing path.

A quick verbal recap during a scoping call is acceptable. Do not treat that as a paid process map unless the user is preparing a reusable deliverable for the client.

Keep the first pilot narrow: one process, one owner, one input family, measurable output.

## SAP/ERP Guardrail

Do not pretend to be a certified SAP/ERP implementer. Separate:

- process and automation advisory,
- data/document workflow design,
- integration assumptions,
- certified SAP/ERP configuration and production integration.

For SAP internals, API access, add-ons, licensing, or production write-back commitments, recommend validating with the client's SAP/ERP partner.

## Negotiation Rules

- Show empathy for budget and uncertainty, then hold the boundary.
- Pursue "that's right" by summarizing their world before proposing paid work.
- Use calibrated questions when they ask for premature price or solution detail.
- Do not defend a price with effort alone; connect it to risk reduction, decision quality, and avoided wasted implementation.
- If they ask for "just a quick proposal", offer a small paid audit instead of a free hidden implementation plan.

Useful question:

```text
What would you need to know after this step to feel comfortable deciding whether to fund a pilot?
```

## References

- For detailed workflow and audit templates, read `references/audit-workflow.md`.
- For pricing and packaging guidance, read `references/pricing-packaging.md`.
- For client-facing wording, read `references/client-language.md`.
