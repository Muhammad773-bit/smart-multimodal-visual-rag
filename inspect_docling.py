from docling.datamodel.pipeline_options import PdfPipelineOptions
import json

options = PdfPipelineOptions()
print("PdfPipelineOptions attributes:", dir(options))
if hasattr(options, 'ocr_options'):
    print("OcrOptions fields:")
    # Instead of dir, let's look at the fields if it's a pydantic model
    try:
        if hasattr(options.ocr_options, 'model_fields'):
            for field in options.ocr_options.model_fields:
                print(f"- {field}")
        else:
            print(vars(options.ocr_options))
    except Exception as e:
        print("Error inspecting fields:", e)
        print(dir(options.ocr_options))
else:
    print("No ocr_options found in PdfPipelineOptions")

