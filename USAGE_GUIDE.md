# AutoScholar Usage Guide

## Quick Start

1. **Run the full analysis:**

   ```bash
   python main.py
   ```

2. **Run a demo with 3 papers:**

   ```bash
   python demo.py
   ```

3. **Test the setup:**
   ```bash
   python test_setup.py
   ```

## Project Structure

```
AutoScholar/
├── main.py                 # Main orchestrator
├── phd_student_agent.py    # Summarizes papers
├── postdoc_agent.py        # Reviews and refines summaries
├── professor_agent.py      # Analyzes insights and compares
├── utils.py                # Utility functions
├── config.py               # Configuration and prompts
├── test_setup.py           # Setup validation
├── demo.py                 # Demo runner (3 papers)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
└── README.md               # Documentation
```

## Workflow Explanation

### Phase 1: PhD Student (Summarization)

- Extracts text from each reference PDF
- Splits large papers into chunks if needed
- Creates comprehensive summaries focusing on:
  - Research questions/objectives
  - Methodology
  - Key findings
  - Theoretical contributions
  - Limitations

### Phase 2: Postdoc (Review & Refinement)

- Reviews each PhD student summary
- Improves clarity and academic precision
- Adds missing critical information
- Corrects any misinterpretations
- Enhances theoretical depth

### Phase 3: Professor (Analysis & Comparison)

- Analyzes all refined summaries collectively
- Identifies convergent themes across papers
- Highlights divergent perspectives
- Spots research gaps
- Compares insights with main paper
- Generates comprehensive final report

## Output

The system generates a detailed report including:

1. Executive summary
2. Reference literature analysis (convergent/divergent themes)
3. Main paper comparison
4. Individual paper summaries
5. Research recommendations

## Configuration

Edit `config.py` to modify:

- Chunk size for large papers
- API retry attempts
- Agent prompts
- Model settings

## API Usage

The system uses GROQ's `llama-3.3-70b-versatile` model with:

- Automatic retry logic (up to 3 attempts)
- Exponential backoff for failed requests
- Rate limiting between requests

## Troubleshooting

**No text extracted from PDF:**

- Some PDFs may be image-based or protected
- Try OCR tools or convert to text first

**API errors:**

- Check your GROQ API key
- Verify internet connection
- Monitor API rate limits

**Memory issues:**

- Reduce CHUNK_SIZE in config.py
- Process fewer papers at once

## Tips for Best Results

1. **Paper Quality:** Ensure PDFs are text-based, not scanned images
2. **Naming:** Use descriptive filenames for reference papers
3. **Organization:** Keep only relevant references in subFolder
4. **API Limits:** Be aware of daily API usage limits
5. **Chunks:** Adjust chunk size based on paper complexity

## Example Commands

```bash
# Full analysis
python main.py

# Quick demo (3 papers)
python demo.py

# Validate setup
python test_setup.py

# Install dependencies
pip install -r requirements.txt
```
