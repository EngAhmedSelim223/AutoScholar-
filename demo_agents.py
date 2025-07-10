#!/usr/bin/env python3
"""
AutoScholar - Individual Agent Demo

Demonstrates how to run each agent independently as per client requirements.
Each agent saves its output to a separate file for the next agent to use.
"""

import os
import sys
from datetime import datetime

from utils import extract_text_from_pdf, get_pdf_files
from phd_student_agent import PhDStudentAgent
from postdoc_agent import PostdocAgent
from professor_agent import ProfessorAgent
from config import MAIN_PAPER_FOLDER, REFERENCES_FOLDER

def demo_agent_1():
    """Demo: Agent 1 (PhD Student) - Paper Summarization"""
    print("🎓 DEMO: Agent 1 - PhD Student Paper Summarization")
    print("="*60)
    
    # Load a few reference papers for demo
    reference_files = get_pdf_files(REFERENCES_FOLDER)[:5]  # Limit to 5 for demo
    
    if not reference_files:
        print("❌ No reference papers found!")
        return None
    
    print(f"📚 Processing {len(reference_files)} papers...")
    
    # Extract texts
    paper_texts = []
    paper_titles = []
    
    for file_path in reference_files:
        filename = os.path.basename(file_path)
        print(f"  📄 Processing: {filename}")
        
        text = extract_text_from_pdf(file_path)
        if text.strip():
            paper_texts.append(text)
            paper_titles.append(filename)
    
    if not paper_texts:
        print("❌ No valid papers to process!")
        return None
    
    # Run Agent 1
    agent1 = PhDStudentAgent()
    output_file = "demo_agent1_summaries.txt"
    
    summaries = agent1.summarize_paper_batch(
        paper_texts=paper_texts,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 1 Demo Complete!")
    print(f"📄 Output saved to: {output_file}")
    print(f"📊 Summaries generated: {len(summaries)}")
    
    return output_file

def demo_agent_2(agent1_output_file):
    """Demo: Agent 2 (Postdoc) - Fragmentation Analysis"""
    print("\n🔬 DEMO: Agent 2 - Postdoc Fragmentation Analysis")
    print("="*60)
    
    if not agent1_output_file or not os.path.exists(agent1_output_file):
        print("❌ Agent 1 output file not found!")
        return None
    
    # Parse summaries from Agent 1 output
    try:
        with open(agent1_output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple parsing of Agent 1 output
        summaries = []
        paper_titles = []
        
        sections = content.split("## ")
        for section in sections[1:]:  # Skip header
            if section.strip():
                lines = section.strip().split('\n')
                if lines:
                    title = lines[0].strip()
                    summary = '\n'.join(lines[1:]).strip()
                    summary = summary.replace('='*80, '').strip()
                    
                    if summary:
                        paper_titles.append(title)
                        summaries.append(summary)
        
        print(f"📊 Parsed {len(summaries)} summaries from Agent 1")
        
    except Exception as e:
        print(f"❌ Error parsing Agent 1 output: {e}")
        return None
    
    # Run Agent 2
    agent2 = PostdocAgent()
    output_file = "demo_agent2_fragmentation.txt"
    
    fragmentation_analysis = agent2.review_and_refine_batch(
        summaries=summaries,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 2 Demo Complete!")
    print(f"📄 Output saved to: {output_file}")
    print("📊 Fragmentation analysis completed")
    
    return output_file

def demo_agent_3(agent2_output_file):
    """Demo: Agent 3 (Professor) - Final Synthesis"""
    print("\n🎓 DEMO: Agent 3 - Professor Final Synthesis")
    print("="*60)
    
    if not agent2_output_file or not os.path.exists(agent2_output_file):
        print("❌ Agent 2 output file not found!")
        return None
    
    # Load fragmentation analysis from Agent 2
    try:
        with open(agent2_output_file, 'r', encoding='utf-8') as f:
            fragmentation_analysis = f.read()
        print("📊 Loaded fragmentation analysis from Agent 2")
    except Exception as e:
        print(f"❌ Error loading Agent 2 output: {e}")
        return None
    
    # Load main paper
    try:
        main_paper_files = get_pdf_files(MAIN_PAPER_FOLDER)
        if not main_paper_files:
            print("❌ No main paper found!")
            return None
        
        main_paper_content = extract_text_from_pdf(main_paper_files[0])
        main_paper_title = os.path.basename(main_paper_files[0])
        print(f"📖 Loaded main paper: {main_paper_title}")
        
    except Exception as e:
        print(f"❌ Error loading main paper: {e}")
        return None
    
    # Run Agent 3
    agent3 = ProfessorAgent()
    output_file = "demo_agent3_synthesis.txt"
    
    synthesis_report = agent3.generate_final_report(
        main_paper_content=main_paper_content,
        fragmentation_analysis=fragmentation_analysis,
        save_details_path=output_file
    )
    
    print(f"\n✅ Agent 3 Demo Complete!")
    print(f"📄 Output saved to: {output_file}")
    print("📊 Final synthesis completed")
    
    return output_file

def main():
    """Run the complete demo workflow."""
    print("🎯 AUTOSCHOLAR - INDIVIDUAL AGENT DEMO")
    print("="*60)
    print("Demonstrating the three-agent workflow:")
    print("Agent 1 (PhD Student) → Agent 2 (Postdoc) → Agent 3 (Professor)")
    print("Each agent saves its output to a separate file.")
    print("="*60)
    
    try:
        # Step 1: Run Agent 1
        agent1_output = demo_agent_1()
        
        if agent1_output:
            # Step 2: Run Agent 2
            agent2_output = demo_agent_2(agent1_output)
            
            if agent2_output:
                # Step 3: Run Agent 3
                agent3_output = demo_agent_3(agent2_output)
                
                if agent3_output:
                    print("\n🎉 DEMO COMPLETE!")
                    print("="*60)
                    print("📄 Agent 1 Output: demo_agent1_summaries.txt")
                    print("📄 Agent 2 Output: demo_agent2_fragmentation.txt")
                    print("📄 Agent 3 Output: demo_agent3_synthesis.txt")
                    print("="*60)
                    print("✅ Each agent has saved its output to a separate file.")
                    print("✅ Workflow demonstrates independent agent execution.")
                else:
                    print("❌ Agent 3 failed")
            else:
                print("❌ Agent 2 failed")
        else:
            print("❌ Agent 1 failed")
    
    except Exception as e:
        print(f"❌ Demo failed: {e}")

if __name__ == "__main__":
    main()
