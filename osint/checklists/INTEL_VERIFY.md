# Checklist: Operational Intelligence Verification
## Veritas Protocol | Procedural Integrity Standard

Use this checklist to evaluate high-impact claims in high-entropy conflict environments.

### 1. Substrate Classification (Evidence Quality)
Identify the primary source of the claim:
- [ ] **Type I (Raw):** Sensor data, unedited satellite imagery, metadata-verified footage.
- [ ] **Type II (Processed):** Aggregated reports, official statements with evidence.
- [ ] **Type III (Interpretative):** Analytical threads, "likely/possibly" claims, expert opinions.
- [ ] **Type IV (Noise):** Anonymous leaks, unverified social media "viral" posts.

**Requirement:** If the source is Type III or IV, it is **interdicted** unless a Type I substrate is attached.

### 2. ESI Assessment (Entropy Stability Index)
Evaluate the information flow speed:
- [ ] **Generation Rate:** Is this narrative spreading faster than it can be physically verified?
- [ ] **Verification Lag:** Is there a technical bottleneck (e.g., waiting for satellite pass, official confirmation)?
- [ ] **Ratio Check:** If $\tau_{verify} / \tau_{inference} > 0.7$, activate **Witness Silence**.

### 3. Logic Authenticity Check (LAC)
Analyze the structural rigor of the conclusion:
- [ ] **Causal Link:** Does the evidence *force* this conclusion, or just *suggest* it?
- [ ] **Trade-off Symmetry ($V \neq L$):** - Value of claim: [Low/High]
    - Cost of error: [Low/High]
    - *Rule:* High Value requires zero-entropy evidence.
- [ ] **Counter-Hypothesis:** Has at least one alternative explanation (e.g., deception, equipment failure) been tested?

### 4. Attribution & Accountability
- [ ] **Accountability Anchor:** Is the claim signed by a persistent identity (analyst/node)?
- [ ] **Confidence Metric:** Is the confidence level (0.0–1.0) explicitly stated?
- [ ] **No-Noise Policy:** All vague attributions ("reports say", "experts believe") are removed.

### 5. Final Action (Decision Matrix)
Select one based on the checks above:
* **[PROCEED]** Conclusion is deterministic. $ESI < 0.3$. High-quality substrate.
* **[FLAG]** Conclusion is probabilistic. Add friction: "Unverified / High Entropy / $ESI$ Warning".
* **[HALT]** Failed $V \neq L$ or LAC check. **Activate Witness Silence.**

---
*Manual interdiction is superior to high-entropy escalation.*
