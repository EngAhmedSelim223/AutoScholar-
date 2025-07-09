#!/usr/bin/env python3
"""
AutoScholar - Academic Research Analysis System

Main orchestrator that coordinates the PhD Student, Postdoc, and Professor agents
to analyze academic papers and generate comprehensive research insights.
"""

import os
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
    print("Simulating PhD Student → Postdoc → Professor workflow")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

def load_main_paper():
    """Load and extract text from the main paper."""
    print("\n📖 STEP 1: Loading Main Paper")
    print("-" * 40)
    
    if not os.path.exists(MAIN_PAPER_FOLDER):
        raise FileNotFoundError(f"Main paper folder '{MAIN_PAPER_FOLDER}' not found")
    
    pdf_files = get_pdf_files(MAIN_PAPER_FOLDER)
    
    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in '{MAIN_PAPER_FOLDER}'")
    
    if len(pdf_files) > 1:
        print(f"⚠️  Multiple PDFs found. Using the first one: {os.path.basename(pdf_files[0])}")
    
    main_paper_path = pdf_files[0]
    print(f"📄 Loading: {os.path.basename(main_paper_path)}")
    
    main_paper_content = extract_text_from_pdf(main_paper_path)
    
    if not main_paper_content.strip():
        raise ValueError("Could not extract text from main paper PDF")
    
    print(f"✅ Successfully loaded main paper ({len(main_paper_content)} characters)")
    return main_paper_content, os.path.basename(main_paper_path)

def process_reference_papers():
    """Process all reference papers using PhD Student and Postdoc agents."""
    print("\n📚 STEP 2: Processing Reference Papers")
    print("-" * 40)
    
    if not os.path.exists(REFERENCES_FOLDER):
        raise FileNotFoundError(f"References folder '{REFERENCES_FOLDER}' not found")
    
    reference_files = get_pdf_files(REFERENCES_FOLDER)
    
    if not reference_files:
        raise FileNotFoundError(f"No PDF files found in '{REFERENCES_FOLDER}'")
    
    print(f"📋 Found {len(reference_files)} reference papers to process")
    
    # Initialize agents
    phd_agent = PhDStudentAgent()
    postdoc_agent = PostdocAgent()
    
    # === Parallel & Batch Processing ===
    print(f"\n📚 Extracting text from reference papers (parallel)...")
    import concurrent.futures
    pdf_texts = []
    filenames = [os.path.basename(f) for f in reference_files]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(extract_text_from_pdf, f): f for f in reference_files}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_file), 1):
            file = future_to_file[future]
            filename = os.path.basename(file)
            try:
                text = future.result()
                pdf_texts.append((filename, text))
                print(f"  ✅ Extracted: {filename}")
            except Exception as e:
                pdf_texts.append((filename, ""))
                print(f"  ❌ Error extracting {filename}: {e}")

    # Filter out empty texts
    pdf_texts = [(fn, txt) for fn, txt in pdf_texts if txt.strip()]
    if not pdf_texts:
        print("❌ No valid reference papers to process after extraction.")
        return {}

    # Phase 1: Batch summarize with PhD agent
    print(f"\n🎓 Phase 1: PhD Student Analysis (batch)...")
    paper_texts = [txt for _, txt in pdf_texts]
    phd_summaries = phd_agent.summarize_paper_batch(paper_texts, [fn for fn, _ in pdf_texts])

    # Phase 2: Batch refine with Postdoc agent
    print(f"\n🔬 Phase 2: Postdoc Review & Refinement (batch)...")
    postdoc_summaries = postdoc_agent.review_and_refine_batch(phd_summaries, [fn for fn, _ in pdf_texts])

    # Build refined summaries dict
    refined_summaries = {fn: summ for (fn, _), summ in zip(pdf_texts, postdoc_summaries)}
    print(f"✅ Postdoc completed {len(refined_summaries)} refined summaries")
    return refined_summaries

def generate_final_analysis(main_paper_content, refined_summaries):
    """Generate final analysis using Professor agent."""
    print("\n🎓 STEP 3: Professor-Level Analysis")
    print("-" * 40)
    
    professor_agent = ProfessorAgent()
    
    # Generate comprehensive final report
    final_report = professor_agent.generate_final_report(main_paper_content, refined_summaries)
    
    print("✅ Professor analysis completed")
    return final_report

def main():
    """Main function that orchestrates the entire workflow."""
    try:
        print_header()
        
        # Step 1: Load main paper
        main_paper_content, main_paper_title = load_main_paper()
        
        # Step 2: Process reference papers
        refined_summaries = process_reference_papers()
        
        # Step 3: Generate final analysis
        final_report = generate_final_analysis(main_paper_content, refined_summaries)
        
        # Step 4: Save and display results
        print("\n💾 STEP 4: Saving Results")
        print("-" * 40)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"analysis_report_{timestamp}.txt"
        save_report(final_report, output_filename)
        
        # Display summary
        print(f"\n🎉 ANALYSIS COMPLETE!")
        print("=" * 70)
        print(f"📊 Main Paper: {main_paper_title}")
        print(f"📚 Reference Papers Analyzed: {len(refined_summaries)}")
        print(f"📄 Report Saved: {output_filename}")
        print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Option to display report
        while True:
            display = input("\n📖 Would you like to display the report now? (y/n): ").lower()
            if display in ['y', 'yes']:
                print("\n" + "="*70)
                print("GENERATED REPORT:")
                print("="*70)
                print(final_report)
                break
            elif display in ['n', 'no']:
                print(f"Report saved to {output_filename}")
                break
            else:
                print("Please enter 'y' or 'n'")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    main()
