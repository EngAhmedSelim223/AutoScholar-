from utils import call_groq_api, chunk_text
from config import PHD_STUDENT_PROMPT

class PhDStudentAgent:

    def summarize_paper_batch(self, paper_texts, paper_titles=None):
        """
        Summarize a batch of academic papers efficiently using batch API.
        Args:
            paper_texts (list of str): List of full texts of papers
            paper_titles (list of str): Optional list of paper titles for context
        Returns:
            list of str: Summaries for each paper
        """
        prompts = []
        for i, text in enumerate(paper_texts):
            title = paper_titles[i] if paper_titles and i < len(paper_titles) else ""
            prompt = PHD_STUDENT_PROMPT.format(text=text)
            if title:
                prompt = f"Paper Title: {title}\n\n" + prompt
            prompts.append(prompt)
        # Use batch API for all
        return call_groq_api(prompts, batch_mode=True)
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
            # Multiple chunks - summarize each in batch
            prompts = [PHD_STUDENT_PROMPT.format(text=chunk) for chunk in chunks]
            chunk_summaries = call_groq_api(prompts, batch_mode=True)
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
