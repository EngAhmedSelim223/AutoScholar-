from utils import call_groq_api
from config import PROFESSOR_PROMPT, COMPARISON_PROMPT

class ProfessorAgent:
    """Agent that simulates a Professor analyzing research insights and making comparisons."""
    
    def __init__(self):
        self.name = "Professor Agent"
    
    def analyze_convergent_divergent(self, refined_summaries):
        """
        Analyze refined summaries to identify substantive intellectual disagreements and theoretical tensions.
        
        Args:
            refined_summaries (dict or list): Refined summaries from postdoc agent
            
        Returns:
            str: Analysis focusing on real intellectual conflicts and convergences
        """
        print(f"🎓 {self.name}: Analyzing substantive intellectual agreements and conflicts...")
        
        # Format summaries for analysis
        if isinstance(refined_summaries, dict):
            summaries_text = self._format_summaries_dict(refined_summaries)
        else:
            summaries_text = self._format_summaries_list(refined_summaries)
        
        # Enhanced prompt focusing on intellectual substance
        enhanced_prompt = f"""
        {PROFESSOR_PROMPT.format(summaries=summaries_text)}
        
        CRITICAL INSTRUCTION: Focus on identifying where papers make conflicting claims about:
        - The same phenomena or concepts
        - Causal relationships and mechanisms
        - Theoretical predictions and outcomes
        - Policy recommendations for similar problems
        - Interpretations of similar evidence
        
        Ignore differences in:
        - Research methods (unless they lead to contradictory conclusions)
        - Geographic locations (unless making universal claims)
        - Disciplinary backgrounds (unless addressing the same questions)
        """
        
        # Use batch if summaries are many/long
        if isinstance(refined_summaries, dict) and len(refined_summaries) > 3:
            prompts = [
                f"{PROFESSOR_PROMPT.format(summaries=self._format_summaries_dict({k: v}))}\n\nCRITICAL INSTRUCTION: Focus on identifying where papers make conflicting claims..."
                for k, v in refined_summaries.items()
            ]
            analysis_list = call_groq_api(prompts, batch_mode=True)
            return "\n\n".join(analysis_list)
        else:
            analysis = call_groq_api(enhanced_prompt)
            return analysis
    
    def compare_with_main_paper(self, main_paper_content, reference_insights):
        """
        Compare main paper's Discussion section with aggregated insights focusing on theoretical positioning.
        
        Args:
            main_paper_content (str): Content of the main paper
            reference_insights (str): Aggregated insights from reference papers
            
        Returns:
            str: Detailed comparison report focusing on substantive intellectual contributions
        """
        print(f"🎓 {self.name}: Analyzing theoretical synthesis in Review Paper...")
        
        # Extract Discussion/Conclusion section from main paper
        from utils import extract_discussion_section
        discussion_section = extract_discussion_section(main_paper_content)
        
        # Enhanced comparison focusing on Review Paper's theoretical synthesis
        enhanced_prompt = f"""
        {COMPARISON_PROMPT.format(
            main_paper=discussion_section[:6000],  # Focus on Discussion section
            reference_insights=reference_insights
        )}
        
        REVIEW PAPER ANALYSIS FOCUS:
        Since this is a REVIEW PAPER (not an empirical study), evaluate how the Discussion/Conclusion section:
        - Synthesizes the theoretical landscape of the field
        - Addresses the 5-10 key theoretical consensus areas identified in the literature
        - Engages with the 5-10 main theoretical debates and conflicts
        - Proposes theoretical frameworks or conceptual contributions
        - Identifies future research directions and theoretical gaps
        
        NO EMPIRICAL ANALYSIS REQUIRED - Focus on theoretical synthesis and literature integration.
        - Which of the 5-10 divergent theoretical conflicts does it address or ignore?
        - Does it propose solutions to theoretical fragmentations identified in the literature?
        - How effectively does it position the study within ongoing theoretical debates?
        """
        
        # Use batch if reference_insights is a list
        if isinstance(reference_insights, list) and len(reference_insights) > 3:
            prompts = [
                f"{COMPARISON_PROMPT.format(main_paper=discussion_section[:6000], reference_insights=ri)}\n\nREVIEW PAPER ANALYSIS FOCUS: ..."
                for ri in reference_insights
            ]
            comparison_list = call_groq_api(prompts, batch_mode=True)
            return "\n\n".join(comparison_list)
        else:
            comparison_report = call_groq_api(enhanced_prompt)
            return comparison_report
    
    def generate_final_report(self, main_paper_content, refined_summaries):
        """
        Generate the complete analysis report.
        
        Args:
            main_paper_content (str): Content of the main paper
            refined_summaries (dict): Refined summaries from all reference papers
            
        Returns:
            str: Complete final report
        """
        print(f"🎓 {self.name}: Generating final comprehensive report...")
        
        # Step 1: Analyze convergent/divergent themes
        reference_analysis = self.analyze_convergent_divergent(refined_summaries)
        
        # Step 2: Compare with main paper
        comparison_report = self.compare_with_main_paper(main_paper_content, reference_analysis)
        
        # Step 3: Combine into final report
        final_report = f"""
# REVIEW PAPER ANALYSIS REPORT
Generated by AutoScholar System (Review Paper Analysis v2.1)

## EXECUTIVE SUMMARY
This report presents a comprehensive analysis of a REVIEW PAPER and its reference literature, focusing on theoretical synthesis, literature integration, and conceptual contributions rather than empirical findings.

The analysis evaluates how well the review paper captures and synthesizes the theoretical landscape of the field through a three-stage process simulating PhD Student, Postdoc, and Professor-level review.

## REFERENCE LITERATURE ANALYSIS
### Focus: Theoretical Consensus Areas and Ongoing Theoretical Debates
{reference_analysis}

## REVIEW PAPER THEORETICAL SYNTHESIS EVALUATION
### Focus: Literature Integration and Conceptual Contributions
{comparison_report}

## ANALYSIS SUMMARY
- Total reference papers analyzed: {len(refined_summaries)}
- Analysis focus: Theoretical synthesis and literature integration
- Evaluation method: Convergent/divergent theoretical patterns
- Paper type: Review/Literature Review

---
Report generated by AutoScholar Academic Analysis System @Ahmed Selim"""
        
        return final_report
    
    def _format_summaries_dict(self, summaries_dict):
        """Format dictionary of summaries for API prompt."""
        formatted = []
        for i, (filename, summary) in enumerate(summaries_dict.items(), 1):
            formatted.append(f"Paper {i}: {filename}\n{summary}\n")
        return "\n".join(formatted)
    
    def _format_summaries_list(self, summaries_list):
        """Format list of summaries for API prompt."""
        formatted = []
        for i, (filename, summary) in enumerate(summaries_list, 1):
            formatted.append(f"Paper {i}: {filename}\n{summary}\n")
        return "\n".join(formatted)
