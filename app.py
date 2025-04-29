# app.py
# FastAPI application for lab test extraction

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import shutil
import uvicorn
from typing import Dict, Any

# Import your existing functions here
# This assumes your extraction code is in a file named lab_extractor.py
from lab_extractor import process_image_and_extract_tests

app = FastAPI(
    title="Lab Test Extractor API",
    description="API for extracting lab test data from medical report images",
    version="1.0.0"
)

@app.get("/")
async def root():
    """
    Root endpoint that returns basic information about the API
    """
    return {
        "service": "Lab Test Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "/get-lab-tests": "POST endpoint that accepts an image file and returns extracted lab test data"
        }
    }

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract lab tests from an uploaded medical report image
    
    Parameters:
    - file: The image file to process
    
    Returns:
    - JSON with extracted lab test data
    """
    # Check file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in valid_extensions:
        return {
            "is_success": False,
            "error": f"Unsupported file format. Supported formats are: {', '.join(valid_extensions)}"
        }
    
    try:
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp:
            shutil.copyfileobj(file.file, temp)
            temp_path = temp.name
        
        # Process the lab report image
        # Note: Your process_image_and_extract_tests returns (result, original_img, processed_img)
        # We only need the result part for the API response
        result, _, _ = process_image_and_extract_tests(temp_path)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        # Return the results
        return result
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        
        return {
            "is_success": False,
            "error": str(e),
            "details": error_details
        }

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
