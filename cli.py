#!/usr/bin/env python3
"""
AutoScholar CLI - Command Line Interface

Allows running individual agents from the command line as per client requirements.
Usage:
    python cli.py agent1 [--output filename.txt]
    python cli.py agent2 [--input filename.txt] [--output filename.txt]  
    python cli.py agent3 [--input filename.txt] [--output filename.txt]
    python cli.py full [--timestamp]
"""

import argparse
import sys
import os
from datetime import datetime

from utils import extract_text_from_pdf, get_pdf_files
from phd_student_agent import PhDStudentAgent
from postdoc_agent import PostdocAgent
from professor_agent import ProfessorAgent
from config import MAIN_PAPER_FOLDER, REFERENCES_FOLDER

def run_agent1(output_file=None):
    """Run Agent 1 (PhD Student) - Paper Summarization."""
    print("🎓 Running Agent 1 - PhD Student Paper Summarization")
    print("-" * 50)
    
    # Load reference papers
    reference_files = get_pdf_files(REFERENCES_FOLDER)
    if not reference_files:
        print("❌ No reference papers found in subFolder!")
        return False
    
    print(f"📚 Found {len(reference_files)} reference papers")
    
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
        return False
    
    # Run Agent 1
    agent1 = PhDStudentAgent()
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"agent1_summaries_{timestamp}.txt"
    
    summaries = agent1.summarize_paper_batch(
        paper_texts=paper_texts,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 1 completed successfully!")
    print(f"📄 Output saved to: {output_file}")
    print(f"📊 Papers summarized: {len(summaries)}")
    
    return True

def run_agent2(input_file=None, output_file=None):
    """Run Agent 2 (Postdoc) - Fragmentation Analysis."""
    print("🔬 Running Agent 2 - Postdoc Fragmentation Analysis")
    print("-" * 50)
    
    # Determine input file
    if not input_file:
        # Auto-detect latest Agent 1 output
        import glob
        agent1_files = glob.glob("agent1_summaries_*.txt")
        if not agent1_files:
            print("❌ No Agent 1 output files found!")
            print("💡 Please run Agent 1 first or specify input file with --input")
            return False
        input_file = max(agent1_files, key=os.path.getmtime)
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    print(f"📄 Using input file: {input_file}")
    
    # Parse summaries from Agent 1 output
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
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
        
        print(f"📊 Parsed {len(summaries)} summaries")
        
    except Exception as e:
        print(f"❌ Error parsing input file: {e}")
        return False
    
    # Run Agent 2
    agent2 = PostdocAgent()
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"agent2_fragmentation_{timestamp}.txt"
    
    fragmentation_analysis = agent2.review_and_refine_batch(
        summaries=summaries,
        paper_titles=paper_titles,
        save_path=output_file
    )
    
    print(f"\n✅ Agent 2 completed successfully!")
    print(f"📄 Output saved to: {output_file}")
    
    return True

def run_agent3(input_file=None, output_file=None):
    """Run Agent 3 (Professor) - Final Synthesis."""
    print("🎓 Running Agent 3 - Professor Final Synthesis")
    print("-" * 50)
    
    # Determine input file
    if not input_file:
        # Auto-detect latest Agent 2 output
        import glob
        agent2_files = glob.glob("agent2_fragmentation_*.txt")
        if not agent2_files:
            print("❌ No Agent 2 output files found!")
            print("💡 Please run Agent 2 first or specify input file with --input")
            return False
        input_file = max(agent2_files, key=os.path.getmtime)
    
    if not os.path.exists(input_file):
        print(f"❌ Input file not found: {input_file}")
        return False
    
    print(f"📄 Using input file: {input_file}")
    
    # Load fragmentation analysis
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            fragmentation_analysis = f.read()
        print("📊 Loaded fragmentation analysis")
    except Exception as e:
        print(f"❌ Error loading input file: {e}")
        return False
    
    # Load main paper
    try:
        main_paper_files = get_pdf_files(MAIN_PAPER_FOLDER)
        if not main_paper_files:
            print("❌ No main paper found in mainPaper folder!")
            return False
        
        main_paper_content = extract_text_from_pdf(main_paper_files[0])
        main_paper_title = os.path.basename(main_paper_files[0])
        print(f"📖 Loaded main paper: {main_paper_title}")
        
    except Exception as e:
        print(f"❌ Error loading main paper: {e}")
        return False
    
    # Run Agent 3
    agent3 = ProfessorAgent()
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"agent3_synthesis_{timestamp}.txt"
    
    synthesis_report = agent3.generate_final_report(
        main_paper_content=main_paper_content,
        fragmentation_analysis=fragmentation_analysis,
        save_details_path=output_file
    )
    
    print(f"\n✅ Agent 3 completed successfully!")
    print(f"📄 Output saved to: {output_file}")
    
    return True

def run_full_pipeline(use_timestamp=True):
    """Run the complete three-agent pipeline."""
    print("🔄 Running Full Pipeline - All Three Agents")
    print("-" * 50)
    
    if use_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        agent1_output = f"agent1_summaries_{timestamp}.txt"
        agent2_output = f"agent2_fragmentation_{timestamp}.txt"
        agent3_output = f"agent3_synthesis_{timestamp}.txt"
    else:
        agent1_output = "agent1_summaries.txt"
        agent2_output = "agent2_fragmentation.txt"
        agent3_output = "agent3_synthesis.txt"
    
    # Step 1: Run Agent 1
    print("\n🎓 Step 1: Running Agent 1...")
    if not run_agent1(agent1_output):
        return False
    
    # Step 2: Run Agent 2
    print("\n🔬 Step 2: Running Agent 2...")
    if not run_agent2(agent1_output, agent2_output):
        return False
    
    # Step 3: Run Agent 3
    print("\n🎓 Step 3: Running Agent 3...")
    if not run_agent3(agent2_output, agent3_output):
        return False
    
    print(f"\n🎉 Full Pipeline Completed Successfully!")
    print("="*50)
    print(f"📄 Agent 1 Output: {agent1_output}")
    print(f"📄 Agent 2 Output: {agent2_output}")
    print(f"📄 Agent 3 Output: {agent3_output}")
    print("="*50)
    
    return True

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AutoScholar CLI - Run individual agents or full pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py agent1                    # Run Agent 1 with auto-generated output file
  python cli.py agent1 --output my_summaries.txt  # Run Agent 1 with custom output file
  python cli.py agent2                    # Run Agent 2 using latest Agent 1 output
  python cli.py agent2 --input summaries.txt --output fragmentation.txt
  python cli.py agent3                    # Run Agent 3 using latest Agent 2 output
  python cli.py full                      # Run all three agents in sequence
  python cli.py full --no-timestamp      # Run all agents without timestamp in filenames
        """
    )
    
    parser.add_argument(
        "command",
        choices=["agent1", "agent2", "agent3", "full"],
        help="Which agent or pipeline to run"
    )
    
    parser.add_argument(
        "--input", "-i",
        help="Input file path (for agent2 and agent3)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )
    
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Don't use timestamp in output filenames (for full pipeline)"
    )
    
    args = parser.parse_args()
    
    print("🎯 AUTOSCHOLAR CLI")
    print("="*40)
    
    try:
        if args.command == "agent1":
            success = run_agent1(args.output)
        elif args.command == "agent2":
            success = run_agent2(args.input, args.output)
        elif args.command == "agent3":
            success = run_agent3(args.input, args.output)
        elif args.command == "full":
            success = run_full_pipeline(not args.no_timestamp)
        else:
            print("❌ Invalid command")
            return 1
        
        if success:
            print("\n✅ Operation completed successfully!")
            return 0
        else:
            print("\n❌ Operation failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
