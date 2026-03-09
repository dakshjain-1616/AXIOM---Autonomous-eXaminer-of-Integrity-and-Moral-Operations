# 🔍 AXIOM - Autonomous eXaminer of Integrity and Moral Operations

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: PEP 8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

> An autonomous ethics auditing agent that scans code for privacy, bias, surveillance, and dark-pattern issues — then debates, resolves, measures carbon impact, and generates legal documentation.

> **Built autonomously by [NEO](https://heyneo.so/) — Your Autonomous AI Agent.**

## 🎯 Overview

AXIOM executes a comprehensive five-phase autonomous pipeline to identify, analyze, and resolve ethical concerns in software code:

```
┌─────────────────────────────────────────────────────────────────┐
│                    AXIOM ETHICS PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│  Phase 1: DETECT  → Scan for tracking, bias, surveillance      │
│  Phase 2: DEBATE  → Adversarial reasoning (DEVIL vs ANGEL)     │
│  Phase 3: RESOLVE → Generate privacy-compliant alternatives    │
│  Phase 4: IMPACT  → Estimate carbon footprint delta (CO2e)     │
│  Phase 5: LEGALIZE→ Produce GDPR/CCPA legal documentation      │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### 🔍 Phase 1: Detection
- **Tracking Detection**: Identifies cookie-based tracking, fingerprinting, analytics collection
- **Bias Detection**: Flags demographic data usage, protected class handling, discriminatory logic
- **Surveillance Detection**: Spots employee monitoring, keystroke logging, screen recording
- **Dark Pattern Detection**: Finds confirm shaming, roach motel patterns, hidden costs

### ⚖️ Phase 2: Debate
- **DEVIL Persona**: Advocates for utility, profit, and business value
- **ANGEL Persona**: Champions privacy, rights, and ethical considerations
- **Balanced Synthesis**: Generates recommendations weighing both perspectives

### 🛠️ Phase 3: Resolution
- Generates privacy-compliant code alternatives
- Provides side-by-side trade-off annotations
- Estimates compliance gains and functionality losses

### 🌱 Phase 4: Impact
- Estimates carbon footprint delta (CO2e)
- Uses baseline: 0.233 kg CO2/kWh
- Analyzes computational complexity
- Provides optimization recommendations

### 📜 Phase 5: Legalize
- **GDPR Compliance**: Articles 5, 6, 7, 17, 22
- **CCPA Disclosures**: Sections 1798.100-1798.125
- **Terms of Service**: Custom clauses based on detected issues
- **Audit Trail**: Timestamped compliance documentation

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/axiom.git
cd axiom

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Command Line Interface

```bash
# Basic usage
python src/axiom_main.py path/to/your/code.py

# With custom output directories
python src/axiom_main.py path/to/your/code.py \
    --output ./my_output \
    --legal-dir ./my_legal_docs \
    --alternatives-dir ./my_alternatives

# Run with sample test data
python src/run_axiom.py
```

### Programmatic API

```python
from src.axiom_config import AXIOMConfig
from src.axiom_pipeline import AXIOMPipeline

# Configure
config = AXIOMConfig(
    output_dir="./output",
    legal_docs_dir="./legal_docs",
    alternatives_dir="./alternatives"
)

# Load code
with open("my_code.py", "r") as f:
    code = f.read()

# Run pipeline
pipeline = AXIOMPipeline(config)
results = pipeline.run(code, "my_code.py")

# Access results
print(f"Issues found: {results['detection']['issues_count']}")
print(f"Risk level: {results['detection']['overall_risk']}")
```

## 📁 Project Structure

```
axiom-ethics-agent/
├── src/                          # Source code
│   ├── axiom_main.py            # CLI entry point
│   ├── axiom_pipeline.py        # Pipeline orchestrator
│   ├── axiom_config.py          # Configuration settings
│   ├── axiom_detection.py       # Phase 1: Detection
│   ├── axiom_debate.py          # Phase 2: Debate
│   ├── axiom_resolve.py         # Phase 3: Resolution
│   ├── axiom_impact.py          # Phase 4: Impact
│   ├── axiom_legalize.py        # Phase 5: Legalize
│   └── run_axiom.py             # Test runner
├── data/                         # Sample data
│   └── sample_code_with_issues.py
├── output/                       # Generated reports
├── legal_docs/                   # Legal documentation
├── alternatives/                 # Code alternatives
├── README.md                     # This file
├── requirements.txt              # Dependencies
├── .gitignore                    # Git ignore rules
└── LICENSE                       # MIT License
```

## 🧪 Testing

```bash
# Run the test suite with sample code
python src/run_axiom.py

# The pipeline will:
# 1. Load sample code with ethical issues
# 2. Run all 5 phases
# 3. Generate reports in output/, legal_docs/, and alternatives/
```

## 📊 Example Output

After running AXIOM, you'll find:

### Master Report (`output/AXIOM_ETHICS_REPORT.md`)
```markdown
# AXIOM ETHICS REPORT
**Generated**: 2026-03-09T10:30:00
**Target**: sample_code_with_issues.py

## Executive Summary
- **Total Issues Detected**: 5
- **Overall Risk Level**: HIGH
- **Debates Conducted**: 3
- **Alternatives Generated**: 5
...
```

### Legal Documents
- `GDPR_Compliance_*.md` - GDPR compliance assessment
- `CCPA_Disclosure_*.md` - CCPA privacy disclosure
- `Terms_of_Service_*.md` - Custom ToS clauses
- `Audit_Trail_*.md` - Timestamped audit log

### Code Alternatives
- `alt_*.py` - Privacy-compliant code alternatives with trade-off annotations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by ethical AI research and privacy-by-design principles
- GDPR and CCPA compliance frameworks

## 📞 Support

For questions, issues, or feature requests, open an issue on GitHub.

---

<p align="center">
  <strong>AXIOM</strong> - Auditing code for a more ethical digital future 🔍✨
</p>

<p align="center">
  Autonomously built by <a href="https://heyneo.so/"><strong>NEO</strong></a> — Your Autonomous AI Agent.
</p>
