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
    
    # Process only first 10 reference papers for demo
    demo_refs = ref_files[:10]
    print(f"🎯 Demo: Processing {len(demo_refs)} reference papers")

    # Initialize agents
    phd_agent = PhDStudentAgent()
    postdoc_agent = PostdocAgent()
    professor_agent = ProfessorAgent()

    # Step 1: Extract all texts in parallel
    print("\n📚 Extracting text from reference papers (parallel)...")
    import concurrent.futures
    pdf_texts = []
    filenames = [os.path.basename(f) for f in demo_refs]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {executor.submit(extract_text_from_pdf, f): f for f in demo_refs}
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
        return

    # Step 2: Batch summarize with PhD agent
    print("\n🎓 PhD Student Agent: Summarizing papers (batch)...")
    paper_texts = [txt for _, txt in pdf_texts]
    phd_summaries = phd_agent.summarize_paper_batch(paper_texts, [fn for fn, _ in pdf_texts])

    # Step 3: Batch refine with Postdoc agent
    print("\n🔬 Postdoc Agent: Refining summaries (batch)...")
    postdoc_summaries = postdoc_agent.review_and_refine_batch(phd_summaries, [fn for fn, _ in pdf_texts])

    # Build summaries dict
    summaries = {fn: summ for (fn, _), summ in zip(pdf_texts, postdoc_summaries)}
    for fn in summaries:
        print(f"✅ Completed: {fn}")
    
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
