import os
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from google import genai

# --- CONFIGURATION ---
GEMINI_API_KEY = "gen-lang-client-0905822726" # Get this from AI Studio
client = genai.Client(api_key=GEMINI_API_KEY)

def prepare_and_index_file(file_path):
    print(f"🚀 Processing: {file_path}")
    
    # A. Setup Docling with CPU-based OCR (for your Ryzen 5600U)
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True 
    pipeline_options.ocr_options.use_gpu = False # Ryzen-friendly
    
    converter = DocumentConverter(
        format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_options)}
    )
    
    # B. Convert to Markdown
    result = converter.convert(file_path)
    md_content = result.document.export_to_markdown()
    
    # C. Save processed text locally for a moment
    temp_md_path = f"processed_{os.path.basename(file_path)}.md"
    with open(temp_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print("✅ Document turned to Markdown. Now sending to Gemini Search Store...")
    
    # D. Create/Use a Store and Index the file
    # This automatically handles the "Embeddings" in the cloud!
    store_name = "Agent_Knowledge_Base"
    
    # We use upload_to_file_search_store which combines uploading + embedding
    operation = client.file_search_stores.upload_to_file_search_store(
        file=temp_md_path,
        config={'display_name': store_name}
    )
    
    print("⏳ Gemini is now embedding your document. This takes a few seconds...")
    return temp_md_path # We keep the path for querying

# --- SMART QUERY FUNCTION ---
def ask_smart_agent(question, store_id):
    print(f"\n🤔 Querying: {question}")
    
    # We use Gemini 1.5 Pro to "Reason" over the retrieved chunks
    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents=question,
        config={'tools': [{'file_search': {'file_search_store_names': [store_id]}}]}
    )
    
    print("\n🌟 AGENT RESPONSE:")
    print(response.text)

# --- EXECUTION ---
# 1. Process your scanned PDF or DOCX
# my_md_file = prepare_and_index_file("your_document.pdf")

# 2. Ask it anything!
# ask_smart_agent("Extract the summary from the scanned table on page 3", "YOUR_STORE_ID")