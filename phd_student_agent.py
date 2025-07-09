from utils import call_groq_api, chunk_text
from config import PHD_STUDENT_PROMPT

class PhDStudentAgent:
    """Agent that simulates a PhD student summarizing academic papers."""
    
    def __init__(self):
        self.name = "PhD Student Agent"
    
    def summarize_paper(self, paper_text, paper_title=""):
        """
        Summarize an academic paper.
        
        Args:
            paper_text (str): The full text of the paper
            paper_title (str): Title of the paper for context
            
        Returns:
            str: Summary of the paper
        """
        print(f"📚 {self.name}: Analyzing paper - {paper_title}")
        
        # Split paper into chunks if it's too long
        chunks = chunk_text(paper_text)
        
        if len(chunks) == 1:
            # Single chunk - summarize directly
            prompt = PHD_STUDENT_PROMPT.format(text=paper_text)
            return call_groq_api(prompt)
        else:
            # Multiple chunks - summarize each and then combine
            chunk_summaries = []
            
            for i, chunk in enumerate(chunks):
                print(f"  Processing chunk {i+1}/{len(chunks)}...")
                prompt = PHD_STUDENT_PROMPT.format(text=chunk)
                chunk_summary = call_groq_api(prompt)
                chunk_summaries.append(chunk_summary)
            
            # Combine chunk summaries into final summary
            combined_text = "\n\n".join(chunk_summaries)
            final_prompt = f"""
            You are a PhD student who has summarized different sections of an academic paper.
            Now combine these section summaries into one coherent overall summary:
            
            Section summaries:
            {combined_text}
            
            Please provide a unified, comprehensive summary:
            """
            
            return call_groq_api(final_prompt)
    
    def process_paper_file(self, paper_path):
        """
        Process a single paper file and return its summary.
        
        Args:
            paper_path (str): Path to the PDF file
            
        Returns:
            tuple: (paper_filename, summary)
        """
        from utils import extract_text_from_pdf
        import os
        
        filename = os.path.basename(paper_path)
        print(f"🔍 Extracting text from: {filename}")
        
        paper_text = extract_text_from_pdf(paper_path)
        
        if not paper_text.strip():
            print(f"⚠️  Warning: No text extracted from {filename}")
            return filename, "No content could be extracted from this PDF."
        
        summary = self.summarize_paper(paper_text, filename)
        return filename, summary
