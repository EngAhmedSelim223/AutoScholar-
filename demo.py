#!/usr/bin/env python3
"""
Demo runner for AutoScholar - processes a smaller subset for testing
"""

import os
from datetime import datetime
from utils import extract_text_from_pdf, get_pdf_files
from phd_student_agent import PhDStudentAgent
from postdoc_agent import PostdocAgent
from professor_agent import ProfessorAgent

def demo_run():
    """Run a demo with limited papers for testing."""
    print("🧪 AUTOSCHOLAR DEMO RUN")
    print("=" * 50)
    
    # Check if we have the required folders
    main_folder = "mainPaper"
    ref_folder = "subFolder"
    
    if not os.path.exists(main_folder):
        print(f"❌ Main paper folder '{main_folder}' not found")
        return
    
    if not os.path.exists(ref_folder):
        print(f"❌ References folder '{ref_folder}' not found")
        return
    
    # Get files
    main_files = get_pdf_files(main_folder)
    ref_files = get_pdf_files(ref_folder)
    
    print(f"📄 Main papers found: {len(main_files)}")
    print(f"📚 Reference papers found: {len(ref_files)}")
    
    if not main_files:
        print("❌ No main paper found")
        return
    
    if not ref_files:
        print("❌ No reference papers found")
        return
    
    # Process only first 3 reference papers for demo
    demo_refs = ref_files[:3]
    print(f"🎯 Demo: Processing {len(demo_refs)} reference papers")
    
    # Initialize agents
    phd_agent = PhDStudentAgent()
    postdoc_agent = PostdocAgent()
    professor_agent = ProfessorAgent()
    
    # Process references
    print("\n📚 Processing Reference Papers...")
    summaries = {}
    
    for i, ref_file in enumerate(demo_refs, 1):
        filename = os.path.basename(ref_file)
        print(f"\n--- Paper {i}/{len(demo_refs)}: {filename} ---")
        
        try:
            # PhD Student summarize
            _, summary = phd_agent.process_paper_file(ref_file)
            
            # Postdoc refine
            refined = postdoc_agent.review_and_refine(summary, filename)
            
            summaries[filename] = refined
            print(f"✅ Completed: {filename}")
            
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    # Load main paper
    print(f"\n📖 Loading Main Paper...")
    main_paper = extract_text_from_pdf(main_files[0])
    main_title = os.path.basename(main_files[0])
    
    if summaries:
        # Professor analysis
        print(f"\n🎓 Professor Analysis...")
        final_report = professor_agent.generate_final_report(main_paper, summaries)
        
        # Save demo report
        demo_output = f"demo_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(demo_output, 'w', encoding='utf-8') as f:
            f.write(final_report)
        
        print(f"\n🎉 Demo completed!")
        print(f"📄 Report saved: {demo_output}")
        print(f"📊 Processed {len(summaries)} reference papers")
        
        # Show brief summary
        print(f"\n📋 DEMO SUMMARY:")
        print(f"Main Paper: {main_title}")
        for filename in summaries.keys():
            print(f"  ✅ {filename}")
    
    else:
        print("❌ No papers were successfully processed")

if __name__ == "__main__":
    demo_run()
