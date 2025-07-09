# 🎓 AutoScholar - Academic Research Analysis System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GROQ](https://img.shields.io/badge/AI-GROQ%20API-orange.svg)](https://groq.com)

A CLI-based academic research analysis system that uses AI agents to simulate a **PhD Student**, **Postdoc**, and **Professor** workflow for comprehensive literature review evaluation.

## 🚀 Features

- **🎓 Three-Agent System**: PhD Student → Postdoc → Professor workflow
- **💻 CLI Interface**: Professional command-line interface
- **📚 Review Paper Focus**: Optimized for literature reviews and theoretical synthesis
- **⚡ Scalable**: Handles 150+ reference papers efficiently
- **🤖 AI-Powered**: Advanced language models via GROQ API
- **📊 Production Ready**: Robust error handling and retry logic

## 🎯 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/EngAhmedSelim223/AutoScholar-.git
cd AutoScholar

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
# Edit config.py and add your GROQ API key

# 4. Run analysis
python main.py
```

## 📖 Documentation

- **[📘 Complete Usage Guide](USAGE_GUIDE.md)** - Comprehensive instructions
- **[✅ Project Status](CLIENT_FINAL_STATUS.md)** - Development completion summary

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- GROQ API key (free tier available)

### Installation

```bash
# Install required dependencies
pip install -r requirements.txt
```

## 🎓 How It Works

### Three-Agent Workflow

1. **🎓 PhD Student Agent**

   - Summarizes each reference paper individually
   - Extracts key research questions, methodology, findings
   - Focuses on academic rigor and theoretical contributions

2. **🔬 Postdoc Agent**

   - Reviews and refines PhD student summaries
   - Improves clarity and academic precision
   - Adds missing critical information
   - Enhances theoretical depth

3. **👨‍🏫 Professor Agent**
   - Analyzes all summaries collectively
   - Identifies 5-10 convergent theoretical patterns
   - Highlights 5-10 divergent theoretical conflicts
   - Compares with main paper's theoretical synthesis
   - Generates comprehensive analysis report

### Analysis Focus

✅ **What it analyzes:**

- Theoretical conflicts and convergences
- Substantive intellectual disagreements
- Literature synthesis quality
- Conceptual framework development

❌ **What it ignores:**

- Surface-level methodological differences
- Geographical context variations
- Empirical data consistency (for review papers)

## 📊 Sample Output

```
# REVIEW PAPER ANALYSIS REPORT

## REFERENCE LITERATURE ANALYSIS
### Theoretical Consensus Areas (5-10 patterns)
### Ongoing Theoretical Debates (5-10 conflicts)

## REVIEW PAPER THEORETICAL SYNTHESIS EVALUATION
### Literature Integration Assessment
### Conceptual Contribution Analysis
### Theoretical Positioning Evaluation
```

## 🎮 Usage Examples

### Command Line Interface

```bash
# NOTE: Place main paper in mainPaper/ folder
# NOTE: Place reference papers in subFolder/
python main.py
```

### Quick Demo

```bash
# Test with 3 papers to verify setup
python demo.py
```

### Test Setup

```bash
# Verify all dependencies and configuration
python test_setup.py
```

## ⚙️ Configuration

Edit `config.py` to modify:

- **GROQ API Key**: Add your API credentials
- **Model Settings**: llama-3.3-70b-versatile (default)
- **Chunk Size**: 4000 tokens (adjustable)
- **Retry Logic**: 3 attempts with exponential backoff
- **Output Settings**: File paths and analysis depth

## 📁 Project Structure

```
AutoScholar/
├──  Core Analysis
│   ├── main.py                      # CLI orchestrator
│   ├── phd_student_agent.py         # PhD Student Agent
│   ├── postdoc_agent.py             # Postdoc Agent
│   ├── professor_agent.py           # Professor Agent
│   ├── utils.py                     # Utility functions
│   └── config.py                    # Configuration
├── 🧪 Testing & Demo
│   ├── demo.py                      # Quick demo (3 papers)
│   └── test_setup.py                # Setup verification
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── USAGE_GUIDE.md               # Complete usage guide
│   └── CLIENT_FINAL_STATUS.md       # Project status
├── 📄 Data Folders
│   ├── mainPaper/                   # Main paper PDF location
│   └── subFolder/                   # Reference papers location
└── 📦 Dependencies
    ├── requirements.txt             # Python dependencies
    ├── .env                         # Environment variables
    └── .gitignore                   # Git ignore file
```

## 🎉 Benefits

### For Researchers

- **⏰ Saves hours** of manual literature review
- **🔍 Identifies patterns** across large paper sets
- **📋 Provides comprehensive** theoretical analysis
- **🎓 Professional quality** academic insights

### For Supervisors

- **📊 Evaluates literature review** quality
- **🔍 Identifies research gaps** and opportunities
- **📍 Assesses theoretical positioning**
- **🧭 Guides research direction**

### For Students

- **📚 Learn literature analysis** from AI examples
- **🧠 Understand theoretical debates** in the field
- **✍️ Improve review writing** skills
- **🚀 Accelerate research** progress

## 🔧 API Configuration

Get your free GROQ API key:

1. Visit [console.groq.com](https://console.groq.com)
2. Create account and upgrade (pay-as-you-go)
3. Generate API key
4. Add to `config.py` or set as environment variable in `.env`

```python
# In config.py
GROQ_API_KEY = "your_api_key_here"

# Or in .env file
GROQ_API_KEY=your_api_key_here
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ahmed Selim**

- GitHub: [@EngAhmedSelim223](https://github.com/EngAhmedSelim223)
- Email: [Contact via GitHub](https://github.com/EngAhmedSelim223)

## 🙏 Acknowledgments

- **GROQ** for providing advanced AI models
- **PyPDF2** for PDF text extraction capabilities
- **Academic research community** for inspiration

---

**AutoScholar transforms tedious literature review into intelligent, comprehensive analysis - making academic research more efficient and insightful!** 🎓✨

## 📈 Project Status

- ✅ **Core Analysis System**: Complete
- ✅ **CLI Interface**: Complete
- ✅ **Documentation**: Complete
- ✅ **Testing & Demo**: Complete
- ✅ **Ready for Production**: ✅

**Version**: 2.1.0 | **Status**: Production Ready
