import os
from dotenv import load_dotenv

load_dotenv()

# GROQ API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Default to llama-3.3-70b-versatile if not set

# Processing Configuration
CHUNK_SIZE = 4000  # Maximum tokens per chunk
MAX_RETRIES = 3    # Maximum API retry attempts

# File Paths
MAIN_PAPER_FOLDER = "mainPaper"
REFERENCES_FOLDER = "subFolder"
OUTPUT_FILE = "analysis_report.txt"

# Agent Prompts
PHD_STUDENT_PROMPT = """
You are a PhD student tasked with summarizing an academic paper. 
Read the following text carefully and provide a comprehensive summary that includes:
1. Main research question/objective
2. Key methodology used
3. Primary findings
4. Theoretical contributions
5. Limitations mentioned

Be thorough but concise. Focus on the academic rigor and scientific content.

Text to summarize:
{text}
"""

POSTDOC_PROMPT = """
You are a Postdoc researcher reviewing a PhD student's summary of an academic paper.
Your task is to refine and improve the summary by:
1. Ensuring all key points are captured accurately
2. Adding any missing critical information
3. Improving clarity and academic precision
4. Correcting any misinterpretations
5. Enhancing the theoretical depth

Original summary:
{summary}

Please provide a refined and improved version:
"""

PROFESSOR_PROMPT = """
You are a senior Professor conducting a meta-analysis of academic literature that will be compared with a REVIEW PAPER. When analyzing 150+ reference papers, your goal is to identify the most significant theoretical convergences and divergences that a comprehensive review should address.

**CONVERGENT THEORETICAL PATTERNS (Aim for 5-10 key established consensus areas):**
- Theoretical propositions that have achieved strong consensus across multiple studies
- Consistent theoretical frameworks and conceptual models widely accepted in the field
- Well-established theoretical relationships that most scholars agree upon
- Common theoretical foundations that underpin the field
- Shared conceptual definitions and theoretical constructs
- Theoretical principles that have been consistently validated across different contexts

**DIVERGENT THEORETICAL DEBATES (Aim for 5-10 key ongoing conflicts):**
- Papers using the SAME theoretical framework but reaching OPPOSITE theoretical conclusions
- Direct contradictions in theoretical interpretations of key concepts or phenomena
- Competing theoretical models or frameworks for explaining the same phenomena
- Unresolved theoretical disputes about fundamental mechanisms or processes
- Studies that explicitly challenge or refute established theoretical positions
- Ongoing theoretical tensions where different schools of thought offer conflicting explanations

**ANALYSIS CRITERIA FOR REVIEW PAPER EVALUATION:**
✅ FOCUS ON: Theoretical agreements and disagreements, conceptual consensus vs. debates, competing theoretical frameworks
❌ IGNORE: Methodological differences, geographical contexts, or empirical approaches (unless they represent fundamental theoretical disagreements)

**SCALING CONSIDERATION:**
With 150+ papers, you should identify the major theoretical fault lines and consensus areas that any comprehensive review paper should acknowledge and address.

**REVIEW PAPER CONTEXT:**
Remember that your analysis will be used to evaluate how well a review paper captures and synthesizes the theoretical landscape of the field.

Here are the refined summaries to analyze:
{summaries}

Provide a focused analysis identifying the key theoretical consensus areas and ongoing theoretical debates that a review paper should address:
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
