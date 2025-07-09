from utils import call_groq_api
from config import POSTDOC_PROMPT

class PostdocAgent:

    def review_and_refine_batch(self, summaries, paper_titles=None):
        """
        Refine a batch of summaries efficiently using batch API.
        Args:
            summaries (list of str): List of summaries to refine
            paper_titles (list of str): Optional list of paper titles for context
        Returns:
            list of str: Refined summaries
        """
        prompts = []
        for i, summary in enumerate(summaries):
            title = paper_titles[i] if paper_titles and i < len(paper_titles) else ""
            prompt = POSTDOC_PROMPT.format(summary=summary)
            if title:
                prompt = f"Paper Title: {title}\n\n" + prompt
            prompts.append(prompt)
        # Use batch API for all
        return call_groq_api(prompts, batch_mode=True)
    """Agent that simulates a Postdoc researcher reviewing and refining summaries."""
    
    def __init__(self):
        self.name = "Postdoc Agent"
    
    def review_and_refine(self, summary, paper_title=""):
        """
        Review and refine a PhD student's summary.
        
        Args:
            summary (str): The original summary to review
            paper_title (str): Title of the paper for context
            
        Returns:
            str: Refined and improved summary
        """
        print(f"🔬 {self.name}: Reviewing summary for - {paper_title}")
        
        prompt = POSTDOC_PROMPT.format(summary=summary)
        # Use batch if summary is a list
        if isinstance(summary, list) and len(summary) > 1:
            prompts = [POSTDOC_PROMPT.format(summary=s) for s in summary]
            refined_list = call_groq_api(prompts, batch_mode=True)
            return refined_list
        else:
            refined_summary = call_groq_api(prompt)
            return refined_summary
    
    def process_summaries(self, summaries_dict):
        """
        Process multiple summaries and return refined versions.
        
        Args:
            summaries_dict (dict): Dictionary with filename as key and summary as value
            
        Returns:
            dict: Dictionary with filename as key and refined summary as value
        """
        refined_summaries = {}
        
        total_papers = len(summaries_dict)
        for i, (filename, summary) in enumerate(summaries_dict.items(), 1):
            print(f"📋 Processing {i}/{total_papers}: {filename}")
            
            refined_summary = self.review_and_refine(summary, filename)
            refined_summaries[filename] = refined_summary
        
        return refined_summaries
    
    def batch_review(self, summaries_list):
        """
        Review a list of summaries in batch.
        
        Args:
            summaries_list (list): List of tuples (filename, summary)
            
        Returns:
            list: List of tuples (filename, refined_summary)
        """
        refined_results = []
        
        for filename, summary in summaries_list:
            refined_summary = self.review_and_refine(summary, filename)
            refined_results.append((filename, refined_summary))
        
        return refined_results
