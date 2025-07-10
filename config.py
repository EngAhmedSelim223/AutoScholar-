import os
from dotenv import load_dotenv

load_dotenv()

# GROQ API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "meta-llama/llama-4-maverick-17b-128e-instruct")  # Default to llama-4-scout (fastest & most cost-effective Llama 4 model for academic analysis)

# Processing Configuration
CHUNK_SIZE = 4000  # Maximum tokens per chunk
MAX_RETRIES = 3    # Maximum API retry attempts

# File Paths
MAIN_PAPER_FOLDER = "mainPaper"
REFERENCES_FOLDER = "subFolder"
OUTPUT_FILE = "analysis_report.txt"

# Agent Prompts
PHD_STUDENT_PROMPT = """
You are a scholarly literature summarization assistant. Your task is to read academic articles and distill their essential information in a consistent, structured format:

1. Full citation (authors, year, title, journal)
2. Research question(s)
3. Theoretical frameworks or lenses used
4. Core theoretical constructs & definitions
5. Key methods and data sources
6. Main findings and conclusions
7. Any stated limitations or boundary conditions

Please provide a clear, structured summary with numbered sections for each field above.

Text to summarize:
{text}
"""

POSTDOC_PROMPT = """
You are an analytical agent specialized in mapping theory landscapes. Given a set of paper summaries, your task is to:

1. Identify concepts or themes that appear under multiple names (convergent)
2. Flag topics treated in isolation across sub-fields (divergent)
3. Highlight overlaps, gaps, and potential points of synthesis

IMPORTANT RULE: Only list a theme if it appears in at least 3 of the papers; otherwise classify as 'minor fragment'

Output your findings in three sections:
- Convergent themes (list + brief explanation)
- Divergent fragments (list + how they diverge)
- Suggested integrative links (short bullet ideas)

Paper summaries:
{summaries}
"""

PROFESSOR_PROMPT = """
You are a senior Professor agent responsible for final synthesis and comparison. Given the fragmentation analysis from Agent 2, your task is to:

PART 1: SYNTHESIS (focus on 5-10 key convergences/divergences only)
For each major theme, evaluate:
   - Concept Match: Does the main paper address this concept? (Yes/No/Partial)
   - Theoretical Lens Match: Does the main paper use the same theoretical lens? (Yes/No/Partial)
   - Suggested Synthesis Novelty: How could the main paper or field integrate or advance this theme?

PART 2: DETAILED COMPARISON WITH MAIN PAPER
Compare the fragmentation analysis findings with the main paper's Discussion/Conclusion:
   - What theoretical themes does the main paper emphasize that align with the literature?
   - What gaps exist between the main paper's focus and the broader literature themes?
   - How well does the main paper synthesize the convergent themes?
   - Does the main paper address the divergent fragments found in the literature?
   - What unique theoretical contributions does the main paper make?

PART 3: FUTURE RESEARCH AREAS
Based on fragmentation analysis and main paper limitations.

Fragmentation Analysis:
{fragmentation_analysis}

Main Paper Content:
{main_paper}

IMPORTANT: Include a detailed comparison section that explicitly contrasts the main paper with the fragmentation analysis findings.
"""

COMPARISON_PROMPT = """
You are a senior Professor comparing a REVIEW PAPER with established theoretical convergences and divergences from its reference literature.

**IMPORTANT:** This is a REVIEW/THEORETICAL PAPER, not an empirical study, so focus on theoretical synthesis and literature integration rather than empirical findings.

**ANALYSIS FOCUS:**
Compare how the review paper synthesizes, positions, and contributes to the theoretical landscape revealed by the reference analysis.

**THEORETICAL SYNTHESIS EVALUATION:**
- How comprehensively does the review capture the 5-10 established theoretical convergences?
- Does it adequately represent and discuss the 5-10 key theoretical divergences in the field?
- Are there important theoretical debates, conflicts, or consensus areas that the review overlooks?

**LITERATURE INTEGRATION ASSESSMENT:**
- How well does the review integrate conflicting theoretical perspectives?
- Does it provide balanced representation of competing theoretical positions?
- How effectively does it synthesize diverse theoretical frameworks?

**THEORETICAL POSITIONING:**
- What stance does the review take on existing theoretical debates and conflicts?
- Does it propose resolutions to theoretical fragmentations identified in the literature?
- How does it position itself relative to dominant vs. minority theoretical perspectives?

**CONCEPTUAL CONTRIBUTION:**
- Does the review develop new theoretical frameworks or conceptual models?
- What unique theoretical insights does it contribute beyond summarizing existing work?
- How does it advance theoretical understanding in the field?

**CRITICAL EVALUATION:**
- Strengths: How effectively does the review synthesize and advance theoretical knowledge?
- Weaknesses: What important theoretical perspectives, debates, or developments does it miss?
- Gaps: Which theoretical tensions or research directions does it fail to address?

**REVIEW QUALITY ASSESSMENT:**
- Does it provide a balanced and comprehensive view of the theoretical landscape?
- How well does it handle contradictory theoretical positions in the literature?
- Does it identify areas of theoretical consensus vs. ongoing debates?

Focus on theoretical contributions, literature synthesis, and conceptual development rather than empirical analysis.

MAIN PAPER CONTENT (focus on Discussion/Conclusion sections if identifiable):
{main_paper}

REFERENCE LITERATURE ANALYSIS (Convergences and Divergences):
{reference_insights}

Provide a focused comparison emphasizing theoretical synthesis and review quality:
"""
