#!/usr/bin/env python3
"""
AutoScholar - Academic Research Analysis System

Main orchestrator that coordinates the PhD Student, Postdoc, and Professor agents
to analyze academic papers and generate comprehensive research insights.

Updated to match client requirements:
- Agent 1 (PhD Student): Summarizes papers, saves to file
- Agent 2 (Postdoc): Analyzes fragmentation, saves to file
- Agent 3 (Professor): Synthesizes and compares, saves to file
"""

import os
import sys
import time
from datetime import datetime

from utils import extract_text_from_pdf, get_pdf_files, save_report
from phd_student_agent import PhDStudentAgent
from postdoc_agent import PostdocAgent
from professor_agent import ProfessorAgent
from config import MAIN_PAPER_FOLDER, REFERENCES_FOLDER, OUTPUT_FILE

def print_header():
    """Print the application header."""
    print("="*70)
    print("🎓 AUTOSCHOLAR - ACADEMIC RESEARCH ANALYSIS SYSTEM")
    print("="*70)
    print("Three-Agent Academic Analysis Pipeline:")
    print("Agent 1 (PhD Student) → Agent 2 (Postdoc) → Agent 3 (Professor)")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def run_agent_1_only():
    """Run only Agent 1 (PhD Student) - Paper Summarization."""
    print("\n� AGENT 1 ONLY: PhD Student Paper Summarization")
    print("-" * 50)
    
    # Load reference papers
    reference_files = get_pdf_files(REFERENCES_FOLDER)
    if not reference_files:
        print("❌ No reference papers found!")
        return
    
    print(f"📋 Found {len(reference_files)} reference papers to summarize")
    
    # Extract texts
    print("📖 Extracting text from papers...")
    paper_texts = []
    paper_titles = []
    
    for i, file_path in enumerate(reference_files, 1):
        filename = os.path.basename(file_path)
        print(f"  Processing {i}/{len(reference_files)}: {filename}")
        
        text = extract_text_from_pdf(file_path)
        if text.strip():
            paper_texts.append(text)
            paper_titles.append(filename)
        else:
            print(f"    ⚠️  Warning: No text extracted from {filename}")
    
    if not paper_texts:
        print("❌ No valid papers to process!")
        return
    
    # Run Agent 1
    agent1 = PhDStudentAgent()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"agent1_summaries_{timestamp}.txt"
    
    summaries = agent1.summarize_paper_batch(
        paper_texts=paper_texts,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 1 completed! Summaries saved to: {output_file}")
    print(f"📊 Total papers summarized: {len(summaries)}")

def run_agent_2_only():
    """Run only Agent 2 (Postdoc) - Fragmentation Analysis."""
    print("\n� AGENT 2 ONLY: Postdoc Fragmentation Analysis")
    print("-" * 50)
    
    # Check if Agent 1 output exists
    import glob
    agent1_files = glob.glob("agent1_summaries_*.txt")
    
    if not agent1_files:
        print("❌ No Agent 1 output files found!")
        print("� Please run Agent 1 first or provide summaries manually.")
        return
    
    # Use the most recent Agent 1 output
    latest_file = max(agent1_files, key=os.path.getmtime)
    print(f"📄 Using Agent 1 output: {latest_file}")
    
    # Parse summaries from Agent 1 output
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract summaries (simple parsing)
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
        
        print(f"📊 Parsed {len(summaries)} summaries from Agent 1 output")
        
    except Exception as e:
        print(f"❌ Error parsing Agent 1 output: {e}")
        return
    
    # Run Agent 2
    agent2 = PostdocAgent()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"agent2_fragmentation_{timestamp}.txt"
    
    fragmentation_analysis = agent2.review_and_refine_batch(
        summaries=summaries,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 2 completed! Fragmentation analysis saved to: {output_file}")

def run_agent_3_only():
    """Run only Agent 3 (Professor) - Final Synthesis."""
    print("\n🎓 AGENT 3 ONLY: Professor Final Synthesis")
    print("-" * 50)
    
    # Check if Agent 2 output exists
    import glob
    agent2_files = glob.glob("agent2_fragmentation_*.txt")
    
    if not agent2_files:
        print("❌ No Agent 2 output files found!")
        print("💡 Please run Agent 2 first or provide fragmentation analysis manually.")
        return
    
    # Use the most recent Agent 2 output
    latest_file = max(agent2_files, key=os.path.getmtime)
    print(f"📄 Using Agent 2 output: {latest_file}")
    
    # Load fragmentation analysis
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            fragmentation_analysis = f.read()
        print("📊 Loaded fragmentation analysis from Agent 2")
    except Exception as e:
        print(f"❌ Error loading Agent 2 output: {e}")
        return
    
    # Load main paper
    try:
        main_paper_files = get_pdf_files(MAIN_PAPER_FOLDER)
        if not main_paper_files:
            print("❌ No main paper found!")
            return
        
        main_paper_content = extract_text_from_pdf(main_paper_files[0])
        main_paper_title = os.path.basename(main_paper_files[0])
        print(f"📖 Loaded main paper: {main_paper_title}")
        
    except Exception as e:
        print(f"❌ Error loading main paper: {e}")
        return
    
    # Run Agent 3
    agent3 = ProfessorAgent()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"agent3_synthesis_{timestamp}.txt"
    
    synthesis_report = agent3.generate_final_report(
        main_paper_content=main_paper_content,
        fragmentation_analysis=fragmentation_analysis,
        save_details_path=output_file
    )
    
    print(f"\n✅ Agent 3 completed! Final synthesis saved to: {output_file}")

def run_full_pipeline():
    """Run the complete three-agent pipeline."""
    print("\n🔄 FULL PIPELINE: Running All Three Agents")
    print("-" * 50)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Load reference papers
    print("\n📚 STEP 1: Loading Reference Papers")
    reference_files = get_pdf_files(REFERENCES_FOLDER)
    if not reference_files:
        print("❌ No reference papers found!")
        return
    
    print(f"📋 Found {len(reference_files)} reference papers")
    
    # Extract texts
    paper_texts = []
    paper_titles = []
    
    for i, file_path in enumerate(reference_files, 1):
        filename = os.path.basename(file_path)
        print(f"  Processing {i}/{len(reference_files)}: {filename}")
        
        text = extract_text_from_pdf(file_path)
        if text.strip():
            paper_texts.append(text)
            paper_titles.append(filename)
    
    if not paper_texts:
        print("❌ No valid papers to process!")
        return
    
    # Step 2: Run Agent 1 (PhD Student)
    print("\n🎓 STEP 2: Agent 1 - PhD Student Summarization")
    agent1 = PhDStudentAgent()
    agent1_output = f"agent1_summaries_{timestamp}.txt"
    
    summaries = agent1.summarize_paper_batch(
        paper_texts=paper_texts,
        paper_titles=paper_titles,
        save_path=agent1_output
    )
    
    print(f"✅ Agent 1 completed: {len(summaries)} summaries")
    
    # Step 3: Run Agent 2 (Postdoc)
    print("\n🔬 STEP 3: Agent 2 - Postdoc Fragmentation Analysis")
    agent2 = PostdocAgent()
    agent2_output = f"agent2_fragmentation_{timestamp}.txt"
    
    fragmentation_analysis = agent2.review_and_refine_batch(
        summaries=summaries,
        paper_titles=paper_titles,
        save_path=agent2_output
    )
    
    print("✅ Agent 2 completed: Fragmentation analysis ready")
    
    # Step 4: Load main paper
    print("\n� STEP 4: Loading Main Paper")
    main_paper_files = get_pdf_files(MAIN_PAPER_FOLDER)
    if not main_paper_files:
        print("❌ No main paper found!")
        return
    
    main_paper_content = extract_text_from_pdf(main_paper_files[0])
    main_paper_title = os.path.basename(main_paper_files[0])
    print(f"📄 Main paper loaded: {main_paper_title}")
    
    # Step 5: Run Agent 3 (Professor)
    print("\n🎓 STEP 5: Agent 3 - Professor Final Synthesis")
    agent3 = ProfessorAgent()
    agent3_output = f"agent3_synthesis_{timestamp}.txt"
    
    synthesis_report = agent3.generate_final_report(
        main_paper_content=main_paper_content,
        fragmentation_analysis=fragmentation_analysis,
        save_details_path=agent3_output
    )
    
    print("✅ Agent 3 completed: Final synthesis ready")
    
    # Final summary
    print(f"\n🎉 PIPELINE COMPLETED!")
    print("="*70)
    print(f"📊 Reference Papers Processed: {len(paper_texts)}")
    print(f"� Agent 1 Output: {agent1_output}")
    print(f"📄 Agent 2 Output: {agent2_output}")
    print(f"📄 Agent 3 Output: {agent3_output}")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def main():
    """Main function with menu for different execution modes."""
    print_header()
    
    while True:
        print("\n🔧 EXECUTION MODE SELECTION")
        print("-" * 30)
        print("1. Run Agent 1 Only (PhD Student - Paper Summarization)")
        print("2. Run Agent 2 Only (Postdoc - Fragmentation Analysis)")
        print("3. Run Agent 3 Only (Professor - Final Synthesis)")
        print("4. Run Full Pipeline (All Three Agents)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        try:
            if choice == '1':
                run_agent_1_only()
            elif choice == '2':
                run_agent_2_only()
            elif choice == '3':
                run_agent_3_only()
            elif choice == '4':
                run_full_pipeline()
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation interrupted by user")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
