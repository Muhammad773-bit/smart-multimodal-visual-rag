import os
import time
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from google import genai
from google.genai import types

# 1. Setup API Client
# Replace with your actual key from https://aistudio.google.com/
API_KEY = "gen-lang-client-0905822726"
client = genai.Client(api_key=API_KEY)

def run_agent_pipeline(file_path, user_question):
    print(f"--- 🛠️ STEP 1: Processing {file_path} with Docling ---")
    
    # Configure Docling for your Ryzen CPU (OCR enabled for scans)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True 
    pipeline_options.ocr_options.use_gpu = False 
    
    converter = DocumentConverter(
        format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_options)}
    )
    
    # Convert PDF/DOCX to Markdown
    result = converter.convert(file_path)
    markdown_content = result.document.export_to_markdown()
    
    # Save a temporary markdown file for Gemini to index
    temp_md_name = f"temp_{int(time.time())}.md"
    with open(temp_md_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"--- 🧠 STEP 2: Creating Cloud Search Store & Embedding ---")
    # Create the store (The 'Memory' in the cloud)
    store = client.file_search_stores.create(config={'display_name': 'Agent_Memory'})
    
    # Upload and let Gemini handle the 'Embeddings' automatically
    operation = client.file_search_stores.upload_to_file_search_store(
        file=temp_md_name,
        file_search_store_name=store.name
    )
    
    # Wait for the cloud brain to finish indexing
    while not operation.done:
        print("Waiting for Gemini to index...")
        time.sleep(3)
        operation = client.operations.get(operation.name)

    print(f"--- 🌟 STEP 3: Smart Response from Gemini ---")
    response = client.models.generate_content(
        model="gemini-2.5-flash", # Fast and smart for 2026
        contents=user_question,
        config=types.GenerateContentConfig(
            tools=[types.Tool(file_search=types.FileSearch(file_search_store_names=[store.name]))]
        )
    )

    print("\nAGENT ANSWER:", response.text)
    
    # Cleanup local temp file
    os.remove(temp_md_name)

# --- ACTION ---
# Put your file in the same folder and run!
my_file = "attention-is-all-you-need.pdf" # Or "report.docx"
my_question = "what is the Transformer model architecture flow"

if os.path.exists(my_file):
    run_agent_pipeline(my_file, my_question)
else:
    print(f"File {my_file} not found! Please add it to the folder.")