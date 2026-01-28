# Veritas Protocol

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT_Ethical-green)
![Status](https://img.shields.io/badge/status-early_development-orange)
![Build](https://img.shields.io/badge/build-experimental-yellow)

> **A substrate-agnostic framework for enforcing logical determinism in high-entropy information environments**

> ⚠️ **Status:** This project is in **early experimental development**. Accuracy metrics are not yet established. Use for research and testing purposes only.

> 🔬 **Academic Context:** This is a conceptual framework exploring information integrity principles. It is NOT a production-ready tool and requires significant calibration.

---

## 📖 Overview

Veritas Protocol is an **experimental** architecture investigating methods to distinguish signal from noise in information streams. The project explores:

- **Logic Authenticity Check (LAC)** — Prototype algorithms for detecting semantic inconsistencies
- **Entropy Analysis** — Measuring information complexity and chaos indicators
- **Source-Agnostic Validation** — Testing evaluation independent of source credentials

**Development Stage:** Alpha/Experimental  
**Research Paper:** Draft available on [Zenodo](https://zenodo.org/records/18360722)  
**Academic Status:** Conceptual framework, ongoing calibration

---

## ⚠️ Current Limitations

**Please be aware:**

- ❌ **No established accuracy metrics** - System requires extensive testing
- ❌ **False positives common** - Academic papers may flag as "manipulation"
- ❌ **Language limitations** - Currently optimized for Ukrainian/English only
- ❌ **Context-blind** - Cannot distinguish technical writing from propaganda
- ⚠️ **Experimental thresholds** - Entropy boundaries need calibration
- ⚠️ **Limited scraping** - Web extraction works only for simple article structures

**Recommended Use:** Research, experimentation, methodology testing

---

## 🎯 Core Components (Experimental)

### Prototype Architecture

- **LAC (Logic Authenticity Check)** — *Under development*  
  Early-stage filtering of noise markers and chaos indicators

- **ESI (Entropy Stability Index)** — *Conceptual*  
  Theoretical metric for verification/generation divergence  
  Formula: `ESI = τ_verify / τ_inference` (not yet implemented)

- **Shannon Entropy Analysis** — *Functional*  
  Mathematical entropy calculation for text complexity

- **Marker-Based Detection** — *Partially functional*  
  Simple keyword matching for signal/noise/chaos patterns

### Information Classification (Preliminary)

| Type | Description | Status | Known Issues |
|------|-------------|--------|--------------|
| **Type I** | Deterministic Data | Working | May flag academic papers |
| **Type II** | Probabilistic Synthesis | Experimental | High false positive rate |
| **Type III** | Theatrical Rhetoric | Working | Language-dependent |
| **Type IV** | Semantic Noise | Working | Catches conspiracy markers |

---

## 🚀 Installation & Usage

### Prerequisites

```bash
Python 3.9+
pip
```

### Installation

```bash
# Clone repository
git clone https://github.com/Architekt-future/veritas-protocol.git
cd veritas-protocol

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

#### 1. Start Flask Server (Optional)

```bash
cd veritas-news-analyzer/web
python server.py
```

Server runs on `http://localhost:5000`

**Endpoints:**
- `POST /analyze-url` - Analyze news article URL
- `POST /analyze-text` - Analyze text directly
- `GET /health` - Check server status

#### 2. Use React Interface

Open `veritas-live-terminal.jsx` in Claude.ai as artifact or integrate into your frontend.

**Features:**
- ✅ Text analysis (standalone)
- ✅ URL scraping (requires server)
- ✅ Console logging (debug mode)
- ✅ GitHub sync (validation)
- ✅ Batch processing

#### 3. Python CLI (Direct)

```python
from app.analyzer import VeritasAnalyzer
from app.core import VeritasEngine

# Initialize
engine = VeritasEngine()
analyzer = VeritasAnalyzer(config={})

# Analyze text
text = "Your news article text here..."
metrics = analyzer.analyze(text)
score = engine.calculate_veritas_score(metrics)

print(f"Entropy Score: {score}")
print(f"Status: {engine.get_status(score)}")
```

---

## 📊 Known Accuracy Issues

### Current Challenges

1. **Academic Text Problem**
   - Scientific papers flag as "CRITICAL" due to:
     - Repeated technical terms (low vocabulary diversity)
     - Formulas and notation (high Shannon entropy)
     - CAPS acronyms (mistaken for emotional shouting)
   
   **Status:** Needs domain-specific exception handling

2. **Language Limitations**
   - Markers optimized for Ukrainian and English
   - Other languages not supported
   - Cultural context missing

3. **Shout Factor Issues**
   - Short CAPS (AI, DNA, 5G) incorrectly flagged
   - **Partially fixed:** Now ignores CAPS ≤ 5 characters
   - Technical writing still problematic

4. **No Semantic Understanding**
   - Pure keyword matching
   - Cannot understand context or intent
   - "Quantum borsch" triggers sanity check (good) but also flags valid tech+food articles (bad)

### Test Results (Honest Assessment)

```
Scientific Paper (2663 words):
- Expected: TRUSTED/SUCCESS
- Actual: CRITICAL (0.714)
- Issue: False positive due to repetition

BBC News Article:
- Expected: SUCCESS
- Actual: WARNING-SUCCESS (varies)
- Issue: Inconsistent depending on writing style

Conspiracy Content:
- Expected: CRITICAL
- Actual: CRITICAL (0.95+)
- Issue: ✅ Works correctly
```

**Current Accuracy:** Unknown (insufficient testing dataset)

**Target Accuracy:** 85%+ (future goal)

---

## 🔧 Development Roadmap

### Phase 1: Foundation (Current)
- [x] Basic entropy calculation
- [x] Marker-based detection
- [x] Flask API server
- [x] React interface
- [ ] Comprehensive test suite
- [ ] Accuracy benchmarking

### Phase 2: Calibration (Next)
- [ ] Domain detection (news vs academic vs blog)
- [ ] Language-specific tuning
- [ ] Threshold optimization
- [ ] False positive reduction

### Phase 3: Enhancement (Future)
- [ ] Semantic understanding (embeddings)
- [ ] Context awareness
- [ ] Multi-language support
- [ ] Real-time adaptation

### Phase 4: Production (Long-term)
- [ ] 85%+ accuracy achieved
- [ ] Comprehensive documentation
- [ ] API rate limiting
- [ ] Scalability testing

---

## 🛠️ Tools & Components

### Live Terminal Interface

**React-based frontend** for real-time analysis:

- 🌐 GitHub integration (sync with latest code)
- 🖥️ Local server connection (Flask backend)
- 📊 Console logging (detailed debugging)
- 📦 Batch processing (multiple URLs)
- 💾 JSON export (results + logs)

**File:** `veritas-news-analyzer/web/veritas-live-terminal.jsx`

### Scenario Simulator

**Probabilistic exploration tool** for testing assumptions.

**Path:** [`tools/temporal-navigation-engine/`](tools/temporal-navigation-engine/)

**Note:** This is a research demonstrator, not a prediction tool.

---

## 📚 Documentation

### Technical Resources
- [Architecture Overview](docs/architecture.md) *(conceptual)*
- [Ethical Framework](docs/ethics.md)
- [Known Issues](docs/known_issues.md) *(recommended reading)*

### Research Papers
- **Draft Paper:** "The Veritas Protocol: A Substrate-Agnostic Framework..."
- **Status:** Conceptual framework, not peer-reviewed
- **Archive:** [Zenodo DOI 10.5281/zenodo.18360722](https://zenodo.org/records/18360722)

---

## 🤝 Contributing

We **actively welcome** contributions, especially:

- 🐛 Bug reports (with examples)
- 📊 Test cases and benchmarks
- 🔧 Calibration improvements
- 📝 Documentation
- 🌍 Language support

**Critical Needs:**
1. Comprehensive test dataset
2. Domain detection algorithm
3. Academic text exception handling
4. Accuracy benchmarking suite

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## ⚠️ Usage Disclaimer

**This tool is experimental and should NOT be used for:**
- ❌ Production content moderation
- ❌ Automated fact-checking
- ❌ Legal or official decisions
- ❌ High-stakes verification

**Appropriate uses:**
- ✅ Research and experimentation
- ✅ Methodology testing
- ✅ Educational demonstrations
- ✅ Proof-of-concept development

---

## ⚖️ License

Licensed under **MIT License with Ethical Requirements**

**Key Terms:**
- ✅ Free for research, education, ethical applications
- ✅ Attribution required
- ❌ No use for manipulation, surveillance, deception
- ❌ No weaponization or harmful applications

See [LICENSE.md](LICENSE.md) for complete terms.

---

## 👥 Authors & Credits

**Dmytro Kholodniak** (Lead Architect)  
Strategic direction, conceptual framework, real-world testing

**Chimeric Collective** (AI Co-authors)  
- Claude (Anthropic) - Architecture & strategic analysis
- ChatGPT (OpenAI) - Logic synthesis
- Gemini (Google) - Code optimization & calibration

*Authorship reflects contribution regardless of substrate, in accordance with Source-Agnostic principles.*

---

## 🌐 Links & Resources

- **Repository:** [github.com/Architekt-future/veritas-protocol](https://github.com/Architekt-future/veritas-protocol)
- **Research Archive:** [Zenodo DOI 10.5281/zenodo.18360722](https://zenodo.org/records/18360722)
- **Issues & Discussion:** [GitHub Issues](https://github.com/Architekt-future/veritas-protocol/issues)

---

## 📞 Contact & Support

**For research collaboration:** Open an issue on GitHub  
**For bug reports:** Include example text and expected vs actual results  
**For feature requests:** Explain use case and reasoning

---

## 🔬 Experimental Status Notice

```
⚠️ CURRENT STATUS: EARLY ALPHA

This project is actively under development. Expect:
- Frequent breaking changes
- Inconsistent results
- Missing features
- Incomplete documentation

DO NOT use in production environments.
DO use for research, experimentation, and feedback.

Target release: TBD (when 85%+ accuracy achieved)
```

---

## 🎓 Citation

If using Veritas Protocol in academic research:

```bibtex
@software{veritas2026,
  title={Veritas Protocol: Experimental Framework for Information Entropy Analysis},
  author={Kholodniak, Dmytro and Chimeric Collective},
  year={2026},
  note={Experimental software, early development},
  url={https://github.com/Architekt-future/veritas-protocol},
  doi={10.5281/zenodo.18360722}
}
```

**Please note experimental status in any citations.**

---

**Built with cautious optimism by humans and AI working together** 🤝

💠 Veritas Protocol - "Truth is not an instrument. It is a witness."

*Work in progress. Patience appreciated. Contributions welcome.*
