import os
import time
import PyPDF2
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, MAX_RETRIES, CHUNK_SIZE

def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {str(e)}")
        return ""

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks of specified size."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        word_size = len(word) + 1  # +1 for space
        if current_size + word_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_size = word_size
        else:
            current_chunk.append(word)
            current_size += word_size
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def call_groq_api(prompt, max_retries=MAX_RETRIES):
    """Make API call to GROQ with retry logic."""
    client = Groq(api_key=GROQ_API_KEY)
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"API call attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise Exception(f"All {max_retries} API call attempts failed")

def get_pdf_files(folder_path):
    """Get all PDF files from a folder."""
    pdf_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(folder_path, filename))
    return pdf_files

def save_report(content, filename):
    """Save content to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Report saved to {filename}")
    except Exception as e:
        print(f"Error saving report: {str(e)}")

def load_text_file(filepath):
    """Load text content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading file {filepath}: {str(e)}")
        return ""

def extract_discussion_section(paper_text):
    """Extract Discussion/Conclusion section from paper text."""
    import re
    
    # Common section headers to look for
    discussion_patterns = [
        r'\b(DISCUSSION|Discussion)\b',
        r'\b(CONCLUSION|Conclusion|CONCLUSIONS|Conclusions)\b', 
        r'\b(DISCUSSION AND CONCLUSION|Discussion and Conclusion)\b',
        r'\b(IMPLICATIONS|Implications)\b',
        r'\b(THEORETICAL IMPLICATIONS|Theoretical Implications)\b'
    ]
    
    # Split text into sections
    lines = paper_text.split('\n')
    
    discussion_start = -1
    references_start = -1
    
    # Find discussion section start
    for i, line in enumerate(lines):
        line_upper = line.strip().upper()
        for pattern in discussion_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                # Check if this looks like a section header (short line, possibly numbered)
                if len(line.strip()) < 100 and (
                    line_upper.startswith(('DISCUSSION', 'CONCLUSION', 'IMPLICATIONS')) or
                    re.match(r'^\d+\.?\s*(DISCUSSION|CONCLUSION|IMPLICATIONS)', line_upper)
                ):
                    discussion_start = i
                    break
        if discussion_start != -1:
            break
    
    # Find references section start
    for i, line in enumerate(lines):
        line_upper = line.strip().upper()
        if re.match(r'^\s*(REFERENCES|BIBLIOGRAPHY|WORKS CITED)\s*$', line_upper):
            references_start = i
            break
    
    # Extract discussion section
    if discussion_start != -1:
        end_index = references_start if references_start != -1 else len(lines)
        discussion_text = '\n'.join(lines[discussion_start:end_index])
        
        # If discussion section is very short, return the last 30% of the paper instead
        if len(discussion_text.strip()) < 500:
            last_third_start = int(len(lines) * 0.7)
            discussion_text = '\n'.join(lines[last_third_start:end_index])
        
        return discussion_text.strip()
    else:
        # If no discussion section found, return last 30% of paper
        last_third_start = int(len(lines) * 0.7)
        end_index = references_start if references_start != -1 else len(lines)
        return '\n'.join(lines[last_third_start:end_index]).strip()
