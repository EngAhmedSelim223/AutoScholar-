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
    
    def generate_final_report(self, main_paper_content, fragmentation_analysis, save_details_path=None):
        """
        Generate the complete analysis report.
        
        Args:
            main_paper_content (str): Content of the main paper
            refined_summaries (dict): Refined summaries from all reference papers
            
        Returns:
            str: Complete final report
        """
        print(f"🎓 {self.name}: Synthesizing and comparing with main paper...")
        
        # Extract Discussion/Conclusion section for better comparison
        from utils import extract_discussion_section
        main_paper_discussion = extract_discussion_section(main_paper_content)
        
        # Enhanced prompt with explicit comparison requirements
        prof_prompt = f"""
You are a senior Professor agent. Given the following fragmentation analysis and the main paper content, your task is to:

PART 1: SYNTHESIS (5-10 key convergences/divergences only)
For each major theme from the fragmentation analysis, provide:
   - Concept Match: Does the main paper address this concept? (Yes/No/Partial)
   - Theoretical Lens Match: Does the main paper use the same theoretical lens? (Yes/No/Partial)
   - Suggested Synthesis Novelty: How could the main paper or field integrate or advance this theme?

PART 2: DETAILED COMPARISON WITH MAIN PAPER
Compare the fragmentation analysis findings with the main paper's Discussion/Conclusion sections:
   - What theoretical themes does the main paper emphasize that align with the fragmentation analysis?
   - What gaps exist between the main paper's focus and the broader literature themes?
   - How well does the main paper synthesize the convergent themes identified in the literature?
   - Does the main paper address the divergent fragments found in the literature?
   - What unique theoretical contributions does the main paper make beyond the reference literature?

PART 3: FUTURE RESEARCH AREAS
Based on both the fragmentation analysis and the main paper's limitations/future research suggestions.

Fragmentation Analysis:
{fragmentation_analysis}

Main Paper Discussion/Conclusion Section:
{main_paper_discussion}

IMPORTANT: Make sure to include a detailed comparison section that explicitly contrasts the main paper with the fragmentation analysis findings.
"""
        synthesis_report = call_groq_api(prof_prompt)

        # Save full synthesis if requested
        if save_details_path:
            try:
                with open(save_details_path, 'w', encoding='utf-8') as f:
                    f.write(synthesis_report)
                print(f"📄 Professor synthesis report saved to {save_details_path}")
            except Exception as e:
                print(f"❌ Error saving Professor synthesis: {e}")

        # Step 2: Combine into final report (condensed)
        final_report = f"""
# REVIEW PAPER ANALYSIS REPORT (Condensed)
Generated by AutoScholar System (Condensed v3.0)

## EXECUTIVE SUMMARY
This report presents a condensed analysis of a REVIEW PAPER and its reference literature, focusing on the 5-10 most significant theoretical convergences and divergences, and how the review paper synthesizes these insights.

## SYNTHESIS & COMPARISON
{synthesis_report}

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
