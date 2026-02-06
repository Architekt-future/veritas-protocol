# Veritas Protocol

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT_Ethical-green)
![Status](https://img.shields.io/badge/status-live_prototype-brightgreen)
![Build](https://img.shields.io/badge/build-v13.3-blue)

> **A substrate-agnostic framework for enforcing logical determinism in high-entropy information environments**

> 🚀 **Live Prototype:** [veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)  
> 📄 **Research Paper:** [Zenodo DOI 10.5281/zenodo.18360722](https://zenodo.org/records/18360722)

> ⚠️ **Status:** **Working prototype deployed** (v13.3). System is functional but requires continued calibration. Accuracy metrics under development.

---

## 🌐 Try It Live

**Live Deployment:** [https://veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)

**Features:**
- ✅ Real-time text analysis
- ✅ Entropy scoring (0.0-1.0 scale)
- ✅ Multi-category detection (VERIFIED, ACCEPTABLE, WARNING, VOID, CRITICAL)
- ✅ Semantic void detection (v13.3 NEW)
- ✅ Pattern boost (sophisticated pseudoscience detection)
- ✅ Absurdity detection (logical non-sequiturs)

**Status Indicators:**
- 🟢 **VERIFIED** (0.0-0.15) - Логічно цілісний контент
- 🟢 **ACCEPTABLE** (0.15-0.3) - Прийнятна інформація
- 🟡 **WARNING** (0.3-0.5) - Підозрілий дискурс
- 🟠 **VOID** (0.6+ with low content) - Семантична порожнеча 🆕
- 🔴 **CRITICAL** (0.5+) - Логічний колапс / маніпуляція

**New in v13.3:**
- Semantic void category for "water" texts (high verbosity, low content)
- Improved buzzword detection
- Casuistry scoring
- Enhanced pattern matching

---

## 📖 Overview

Veritas Protocol is a **working prototype** investigating methods to distinguish signal from noise in information streams. The system is currently deployed and functional with ongoing calibration.

**Core Principles:**
- **Logic Authenticity Check (LAC)** — Detects semantic inconsistencies and logical violations
- **Entropy Analysis** — Measures information complexity and chaos indicators
- **Source-Agnostic Truth (SAT)** — Evaluation independent of source credentials
- **Witness Silence** — System halts on logical threshold violations rather than generating filler

**Development Stage:** Live Prototype (v13.3)  
**Research Paper:** [Zenodo](https://zenodo.org/records/18360722)  
**Academic Status:** Conceptual framework with working implementation

---

## ⚠️ Current Limitations

**Prototype Status - Please be aware:**

- ⚠️ **Accuracy under calibration** - System requires extensive testing
- ⚠️ **Context-blind** - Cannot distinguish technical writing from propaganda in all cases
- ⚠️ **Language limitations** - Optimized for Ukrainian/English
- ⚠️ **Threshold refinement ongoing** - Entropy boundaries being calibrated
- ✅ **Functional deployment** - Working prototype available for testing

**Recommended Use:** Research, experimentation, methodology validation

---

## 🎯 Core Components (v13.3)

### Deployed Architecture

- **LAC (Logic Authenticity Check)** — *Deployed*  
  Multi-module violation detection (Trade-off, Accountability, Procedural)

- **Pattern Boost Engine** — *Active*  
  Sophisticated pseudoscience fingerprint matching

- **Semantic Void Detector** — *NEW in v13.3*  
  Identifies high-verbosity, low-content "water" texts

- **Absurdity Detector** — *Active*  
  Logical non-sequiturs and fabricated authority detection

- **Insight Density Analyzer** — *Active*  
  Casuistry detection (complexity without substance)

- **Shannon Entropy Analysis** — *Functional*  
  Mathematical entropy calculation normalized to 0-1 scale

### Information Classification (Live)

| Type | Description | Status | Accuracy |
|------|-------------|--------|----------|
| **VERIFIED** | Zero-entropy deterministic data | ✅ Working | High |
| **ACCEPTABLE** | Low-entropy logical content | ✅ Working | Good |
| **WARNING** | Medium-entropy suspicious discourse | ✅ Working | Moderate |
| **VOID** | High-entropy semantic emptiness | 🆕 NEW | Testing |
| **CRITICAL** | Critical-entropy manipulation | ✅ Working | Good |

---

## 🚀 Quick Start

### Option 1: Use Live Deployment (Easiest)

Visit [veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)

No installation required!

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/Architekt-future/veritas-protocol.git
cd veritas-protocol

# Install dependencies
pip install flask flask-cors gunicorn

# Run locally
python app.py
```

Server runs on `http://localhost:5000`

### Option 3: Deploy Your Own

**Render.com (Recommended):**
1. Fork repository
2. Create new Web Service on Render
3. Connect GitHub repo
4. Set environment variables:
   ```
   PYTHONDONTWRITEBYTECODE=1
   PYTHONUNBUFFERED=1
   VERITAS_VERSION=v13.3
   FORCE_RELOAD=true
   ```
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `bash deploy.sh`

---

## 🔧 API Usage

### Analyze Text

**Endpoint:** `POST /api/analyze`

**Request:**
```json
{
  "text": "Your text to analyze here..."
}
```

**Response:**
```json
{
  "entropy": 0.42,
  "status": "WARNING",
  "verdict": "ПІДОЗРІЛИЙ ДИСКУРС",
  "explanation": "Виявлено ознаки логічних несумісностей",
  "diagnostics": {
    "word_count": 150,
    "char_count": 890,
    "shannon_entropy": 0.38,
    "void_score": 0.25,
    "absurdity_score": 0.15,
    "buzzword_count": 3,
    "is_semantic_void": false,
    "violation_count": 2
  }
}
```

### Health Check

**Endpoint:** `GET /api/health`

Returns system status and version info.

---

## 📊 Known Accuracy Issues

### Active Calibration Areas

1. **Academic Text Detection**
   - ✅ Protected science filter active
   - ⚠️ Some edge cases remain
   - 🔄 Ongoing threshold tuning

2. **Semantic Void Category** 🆕
   - ✅ Detects "water" texts effectively
   - ⚠️ Threshold requires fine-tuning
   - 🔄 Collecting test cases

3. **Language Support**
   - ✅ Ukrainian: Well-calibrated
   - ✅ English: Good coverage
   - ❌ Other languages: Not supported

4. **Context Understanding**
   - ⚠️ Pure keyword matching (no semantic embeddings yet)
   - 🔄 Pattern matching improvements ongoing

### Test Results (Live Prototype)

```
Conspiracy Content:
- Expected: CRITICAL
- Actual: CRITICAL (0.8-0.95)
- Status: ✅ Working correctly

Academic Paper:
- Expected: VERIFIED/ACCEPTABLE
- Actual: VERIFIED (0.10-0.20)
- Status: ✅ Protected science filter works

Corporate Buzzwords:
- Expected: VOID
- Actual: VOID (0.6-0.7)
- Status: 🆕 NEW category working

News Articles:
- Expected: ACCEPTABLE/WARNING
- Actual: Varies (0.2-0.4)
- Status: ⚠️ Needs calibration
```

**Current Performance:** Functional prototype, calibration ongoing  
**Target Accuracy:** 85%+ (future goal)

---

## 🔧 Development Roadmap

### ✅ Phase 1: Foundation (Completed)
- [x] Basic entropy calculation
- [x] Multi-module LAC system
- [x] Flask API server
- [x] Live deployment
- [x] Semantic void detection
- [x] Pattern boost engine

### 🔄 Phase 2: Calibration (Current)
- [x] Live prototype deployed
- [ ] Comprehensive test dataset
- [ ] Threshold optimization
- [ ] False positive reduction
- [ ] Accuracy benchmarking

### 🔜 Phase 3: Enhancement (Next)
- [ ] Semantic understanding (embeddings)
- [ ] Context awareness
- [ ] Multi-language support
- [ ] Domain-specific tuning

### 🎯 Phase 4: Production (Future)
- [ ] 85%+ accuracy achieved
- [ ] Rate limiting & scaling
- [ ] API authentication
- [ ] Comprehensive documentation

---

## 🛠️ Architecture Details

### Core Modules (Live)

**veritas_calibrated_core.py** (v13.3)
- LAC Module I: Trade-off Calculus (V ≠ L)
- LAC Module II: Accountability Anchor
- LAC Module III: Procedural Interdiction
- Hybrid scoring algorithm

**veritas_semantic_void.py**
- Absence detection (missing facts/numbers/specifics)
- Vagueness scoring (hollow buzzwords)
- False causality detection
- Unfalsifiable claims filter

**veritas_pattern_boost.py**
- Sophisticated pseudoscience fingerprints
- Domain mixing patterns
- Fabricated authority detection

**veritas_absurdity_detector.py**
- Logical non-sequitur detection
- Dangerous implications scoring
- Ontological category errors

**veritas_insight_density.py**
- Casuistry detection
- Bureaucratic complexity analysis
- Fact density measurement

---

## 📚 Documentation

### Live Resources
- **Live Demo:** [veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)
- **API Docs:** [Available at /api/health endpoint]
- **Test Interface:** Included in live deployment

### Technical Documentation
- [Architecture Overview](docs/architecture.md)
- [Ethical Framework](docs/ethics.md)
- [Known Issues](docs/known_issues.md)
- [Deployment Guide](DEPLOYMENT_GUIDE_v13.3.md)

### Research Papers
- **Paper:** "The Veritas Protocol: A Substrate-Agnostic Framework..."
- **Status:** Published concept with working prototype
- **Archive:** [Zenodo DOI 10.5281/zenodo.18360722](https://zenodo.org/records/18360722)
- **Real-time Validation:** January 2026 crisis analysis

---

## 🤝 Contributing

We **actively welcome** contributions!

**Critical Needs:**
1. Test cases with expected results
2. Threshold calibration data
3. Domain-specific patterns
4. Language support expansion
5. Bug reports from live testing

**How to Contribute:**
1. Test the live prototype
2. Report issues with examples
3. Propose calibration improvements
4. Submit pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## ⚠️ Usage Disclaimer

**Live Prototype Status:**

**Appropriate uses:**
- ✅ Research and experimentation
- ✅ Methodology testing
- ✅ Educational demonstrations
- ✅ Personal content analysis
- ✅ Proof-of-concept validation

**NOT recommended for:**
- ❌ Production content moderation
- ❌ Automated fact-checking without human review
- ❌ Legal or official decisions
- ❌ High-stakes verification

**Note:** This is a working prototype. Results should be interpreted as experimental data requiring validation.

---

## ⚖️ License

Licensed under **MIT License with Ethical Requirements**

**Key Terms:**
- ✅ Free for research, education, ethical applications
- ✅ Attribution required
- ✅ Commercial use allowed with ethical compliance
- ❌ No use for manipulation, surveillance, deception
- ❌ No weaponization or harmful applications

See [LICENSE.md](LICENSE.md) for complete terms.

---

## 👥 Authors & Credits

**Dmytro Kholodniak** (Lead Architect, Independent Researcher)  
System design, conceptual framework, deployment, real-world validation

**Chimeric Collective** (AI Co-authors)  
- **Claude** (Anthropic) - Strategic architecture, integrity module, deployment assistance
- **ChatGPT** (OpenAI) - Systemic logic, conflict analysis
- **Gemini** (Google) - Data synthesis, verification module

*This co-authorship demonstrates the Source-Agnostic Truth (SAT) principle: authorship reflects contribution regardless of substrate.*

---

## 🌐 Links & Resources

- **🚀 Live Prototype:** [veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)
- **💾 Repository:** [github.com/Architekt-future/veritas-protocol](https://github.com/Architekt-future/veritas-protocol)
- **📄 Research Archive:** [Zenodo DOI 10.5281/zenodo.18360722](https://zenodo.org/records/18360722)
- **🐛 Issues & Discussion:** [GitHub Issues](https://github.com/Architekt-future/veritas-protocol/issues)

---

## 📞 Contact & Support

**Live Testing Feedback:** Open an issue with results from the live prototype  
**Bug Reports:** Include example text, expected vs actual results, and screenshots  
**Feature Requests:** Explain use case and reasoning  
**Research Collaboration:** Contact via GitHub discussions

---

## 🔬 Deployment Status

```
✅ LIVE PROTOTYPE v13.3

Current deployment: https://veritas-protocol.onrender.com

Features:
✅ Multi-category detection (5 levels)
✅ Semantic void analysis (NEW)
✅ Pattern boost engine
✅ Absurdity detection
✅ Real-time processing
✅ Detailed diagnostics

Status: FUNCTIONAL
Uptime: 24/7 (best-effort)
Performance: <2s response time
Calibration: Ongoing

Use for testing, research, and feedback.
Production readiness: TBD (pending 85%+ accuracy)
```

---

## 🎓 Citation

If using Veritas Protocol in academic research:

```bibtex
@software{veritas2026,
  title={Veritas Protocol: A Substrate-Agnostic Framework for Information Entropy Analysis},
  author={Kholodniak, Dmytro and Chimeric Collective},
  year={2026},
  version={13.3},
  note={Live working prototype},
  url={https://veritas-protocol.onrender.com},
  repository={https://github.com/Architekt-future/veritas-protocol},
  doi={10.5281/zenodo.18360722}
}
```

**Please note prototype status and live deployment URL in citations.**

---

## 📈 Changelog

### v13.3 (2026-02-05) - CURRENT
- 🆕 Added SEMANTIC VOID category
- 🆕 Semantic void detector module
- ✅ Live deployment on Render
- ✅ Cache clearing mechanism
- ✅ Improved buzzword detection
- ✅ Casuistry scoring
- 🔧 Fixed regex encoding issues
- 🔧 Optimized threshold calculations

### v13.2 (2026-01-26)
- ✅ Pattern boost engine
- ✅ Absurdity detector
- ✅ Insight density analyzer
- ✅ Academic shield improvements

### v13.0 (2026-01-22)
- ✅ Initial deployment
- ✅ Core LAC modules
- ✅ Basic entropy analysis

---

**Built with determination by humans and AI working together** 🤝

💠 **Veritas Protocol** - *"Truth is not an instrument. It is a witness."*

🚀 **Try it live:** [veritas-protocol.onrender.com](https://veritas-protocol.onrender.com)

*Live prototype. Calibration ongoing. Contributions welcome.*
