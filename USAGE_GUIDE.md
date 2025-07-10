# AutoScholar - Complete Usage Guide

## Overview

AutoScholar is a three-agent academic analysis system that processes research papers through a structured workflow:

1. **Agent 1 (PhD Student)**: Summarizes papers with structured information
2. **Agent 2 (Postdoc)**: Identifies theoretical fragmentation and themes
3. **Agent 3 (Professor)**: Synthesizes insights and compares with main paper

## Setup Instructions

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd AutoScholar

# Install dependencies
pip install -r requirements.txt

# Create environment file
# Create .env file with:
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 2. Data Preparation

- Place your main paper (PDF) in `mainPaper/` folder
- Place reference papers (PDFs) in `subFolder/` folder
- Ensure PDFs are text-extractable (not scanned images)

## Usage Methods

### Method 1: Interactive Menu (Recommended)

```bash
python main.py
```

**Menu Options:**

1. **Run Agent 1 Only**: PhD Student paper summarization
2. **Run Agent 2 Only**: Postdoc fragmentation analysis (requires Agent 1 output)
3. **Run Agent 3 Only**: Professor synthesis (requires Agent 2 output)
4. **Run Full Pipeline**: All three agents in sequence
5. **Exit**

### Method 2: Command Line Interface

```bash
# Individual agents
python cli.py agent1                    # Run PhD Student
python cli.py agent2                    # Run Postdoc (uses latest Agent 1 output)
python cli.py agent3                    # Run Professor (uses latest Agent 2 output)

# With specific input/output files
python cli.py agent1 --output my_summaries.txt
python cli.py agent2 --input summaries.txt --output fragmentation.txt
python cli.py agent3 --input fragmentation.txt --output synthesis.txt

# Full pipeline
python cli.py full                      # Run all agents with timestamps
python cli.py full --no-timestamp      # Run all agents without timestamps
```

### Method 3: Demo Script

```bash
python demo_agents.py
```

This runs a limited demo with 5 papers to demonstrate the workflow.

## Agent Details

### Agent 1 (PhD Student) - Paper Summarization

**Purpose**: Extract and structure key information from academic papers

**Input**: PDF files from `subFolder/`
**Output**: Text file with structured summaries

**Summary Structure**:

1. **Full citation** (authors, year, title, journal)
2. **Research question(s)**
3. **Theoretical frameworks or lenses used**
4. **Core theoretical constructs & definitions**
5. **Key methods and data sources**
6. **Main findings and conclusions**
7. **Any stated limitations or boundary conditions**

**Example Output File**: `agent1_summaries_20250710_143022.txt`

### Agent 2 (Postdoc) - Fragmentation Analysis

**Purpose**: Identify theoretical patterns and fragmentation across papers

**Input**: Agent 1 summaries
**Output**: Analysis of convergent/divergent themes

**Analysis Sections**:

- **Convergent themes**: Concepts appearing in 3+ papers with explanations
- **Divergent fragments**: Topics treated in isolation with divergence details
- **Suggested integrative links**: Bullet points of synthesis opportunities

**Key Rule**: Only themes appearing in 3+ papers are classified as major themes; others are minor fragments.

**Example Output File**: `agent2_fragmentation_20250710_143045.txt`

### Agent 3 (Professor) - Final Synthesis

**Purpose**: Synthesize landscape and compare with main paper

**Input**: Agent 2 fragmentation analysis + main paper from `mainPaper/`
**Output**: Comprehensive synthesis report

**Synthesis Components**:

1. **Theoretical Landscape**: 5-10 key convergences/divergences
2. **For each major theme**:
   - **Concept Match**: Does main paper address this? (Yes/No/Partial)
   - **Theoretical Lens Match**: Same theoretical lens? (Yes/No/Partial)
   - **Suggested Synthesis Novelty**: How to integrate/advance the theme
3. **Future Research Areas**: Based on fragmentation analysis
4. **Comparison**: With main paper's Discussion/Conclusion sections

**Example Output File**: `agent3_synthesis_20250710_143112.txt`

## Workflow Examples

### Example 1: Full Pipeline

```bash
# Run complete workflow
python main.py
# Select option 4 (Run Full Pipeline)

# Results:
# agent1_summaries_20250710_143022.txt
# agent2_fragmentation_20250710_143045.txt
# agent3_synthesis_20250710_143112.txt
```

### Example 2: Individual Agent Execution

```bash
# Step 1: Run PhD Student
python cli.py agent1 --output phd_summaries.txt

# Step 2: Run Postdoc
python cli.py agent2 --input phd_summaries.txt --output postdoc_analysis.txt

# Step 3: Run Professor
python cli.py agent3 --input postdoc_analysis.txt --output professor_synthesis.txt
```

### Example 3: Re-run Individual Agents

```bash
# If you want to re-run Agent 2 with different parameters:
python cli.py agent2 --input agent1_summaries_20250710_143022.txt --output new_fragmentation.txt

# Then run Agent 3 with the new fragmentation analysis:
python cli.py agent3 --input new_fragmentation.txt --output new_synthesis.txt
```

## File Management

### Input Files

- **Main Paper**: Place in `mainPaper/` folder (only one PDF file)
- **Reference Papers**: Place in `subFolder/` folder (multiple PDF files)

### Output Files

- **Agent 1**: `agent1_summaries_[timestamp].txt`
- **Agent 2**: `agent2_fragmentation_[timestamp].txt`
- **Agent 3**: `agent3_synthesis_[timestamp].txt`

### File Naming Convention

- Timestamp format: `YYYYMMDD_HHMMSS`
- Files are automatically named unless specified otherwise
- CLI allows custom file names with `--output` parameter

## Configuration

### API Configuration

Edit `config.py`:

```python
GROQ_API_KEY = "your_api_key_here"
GROQ_MODEL = "llama-3.3-70b-versatile"
CHUNK_SIZE = 4000
MAX_RETRIES = 3
```

### Folder Configuration

```python
MAIN_PAPER_FOLDER = "mainPaper"
REFERENCES_FOLDER = "subFolder"
```

### Agent Prompts

All agent prompts are defined in `config.py` and can be customized:

- `PHD_STUDENT_PROMPT`: Instructions for paper summarization
- `POSTDOC_PROMPT`: Instructions for fragmentation analysis
- `PROFESSOR_PROMPT`: Instructions for synthesis and comparison

## Troubleshooting

### Common Issues

1. **No papers found**

   - Ensure PDF files are in correct folders
   - Check file permissions
   - Verify PDF files are not corrupted

2. **API errors**

   - Check GROQ API key validity
   - Verify internet connection
   - Check API rate limits

3. **Text extraction fails**

   - Ensure PDFs contain extractable text (not scanned images)
   - Try converting scanned PDFs to text-searchable PDFs

4. **Agent 2/3 can't find input files**
   - Check that previous agent completed successfully
   - Verify output file names and locations
   - Use CLI with explicit `--input` parameter

### Performance Tips

1. **Large document sets**

   - Process in smaller batches if needed
   - Monitor API usage and limits
   - Consider using the demo script first

2. **Processing time**

   - Larger papers take longer to process
   - Batch processing is optimized for efficiency
   - Network speed affects API calls

3. **Memory usage**
   - Large PDFs consume more memory
   - Close other applications if needed
   - Consider processing fewer papers at once

## Advanced Usage

### Custom Workflows

You can create custom workflows by importing the agent classes:

```python
from phd_student_agent import PhDStudentAgent
from postdoc_agent import PostdocAgent
from professor_agent import ProfessorAgent

# Create custom workflow
agent1 = PhDStudentAgent()
agent2 = PostdocAgent()
agent3 = ProfessorAgent()

# Process with custom parameters
summaries = agent1.summarize_paper_batch(papers, titles, "custom_output.txt")
fragmentation = agent2.review_and_refine_batch(summaries, titles, "custom_frag.txt")
synthesis = agent3.generate_final_report(main_paper, fragmentation, "custom_synth.txt")
```

### Batch Processing

The system supports batch processing for efficiency:

- Multiple papers processed simultaneously
- Optimized API calls
- Parallel text extraction
- Progress tracking

## Support

For issues or questions:

1. Check this usage guide
2. Review error messages in console
3. Verify file permissions and API configuration
4. Check the project repository for updates

## Best Practices

1. **Data Preparation**

   - Use high-quality, text-extractable PDFs
   - Organize papers logically
   - Remove corrupted or duplicate files

2. **Workflow Management**

   - Start with the demo script to test setup
   - Use individual agents for iterative refinement
   - Save intermediate outputs for reprocessing

3. **Output Review**

   - Review each agent's output before proceeding
   - Check for any extraction or analysis errors
   - Verify that themes meet the 3+ paper threshold

4. **Resource Management**
   - Monitor API usage and costs
   - Process in reasonable batches
   - Keep backups of important outputs
