import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
from typing import Dict, List, Any, Tuple
import pandas as pd
import easyocr

def preprocess_image(image):
    """
    Preprocess the image to improve OCR accuracy
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    adaptive_thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    denoised = cv2.fastNlMeansDenoising(adaptive_thresh, h=10)

    return denoised

def display_image(image, title='Image'):
    """
    Display an image using matplotlib
    """
    plt.figure(figsize=(10, 8))
    if len(image.shape) == 3:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    else:
        plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

def extractText(image_path):
    """
    Extract text from an image file using EasyOCR
    Returns the extracted text and images (original and processed)
    """
    reader = easyocr.Reader(['en'])
    
    # Read the image
    original_img = cv2.imread(image_path)
    if original_img is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    # Preprocess image
    processed_img = preprocess_image(original_img)
    
    # Extract text
    results = reader.readtext(processed_img)
    text = " ".join([result[1] for result in results])
    
    return text, original_img, processed_img

def parse_lab_tests(text: str) -> List[Dict[str, Any]]:
    """
    Parse lab test results from extracted text
    """
    lab_tests = []
    patterns = [
        r'([A-Z][A-Za-z\s\(\)]+)[\s:]+(\d+\.?\d*)\s*([a-zA-Z%/]+)[\s\(]+(\d+\.?\d*[-–]\d+\.?\d*)',
        r'([A-Z][A-Za-z\s\(\)]+)\s+(\d+\.?\d*)\s+([a-zA-Z%/]+)\s+(\d+\.?\d*[-–]\d+\.?\d*)'
    ]

    all_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        all_matches.extend(matches)

    for match in all_matches:
        if len(match) >= 4:
            test_name, test_value, test_unit, ref_range = match
            test_name = test_name.strip()
            test_value = test_value.strip()
            test_unit = test_unit.strip()
            ref_range = ref_range.strip().replace('–', '-')
            out_of_range = is_out_of_range(test_value, ref_range)

            lab_test = {
                "test_name": test_name,
                "test_value": test_value,
                "bio_reference_range": ref_range,
                "test_unit": test_unit,
                "lab_test_out_of_range": out_of_range
            }

            lab_tests.append(lab_test)
    
    unique_tests = []
    test_names = set()

    for test in lab_tests:
        if test["test_name"] not in test_names:
            test_names.add(test["test_name"])
            unique_tests.append(test)
    return unique_tests

def is_out_of_range(value, range_str):
    """
    Check if the test value is outside the reference range
    """
    try:
        val = float(value)

        range_parts = range_str.replace('–', '-').split('-')
        min_val = float(range_parts[0])
        max_val = float(range_parts[1])

        return val < min_val or val > max_val
    except (ValueError, IndexError):
        return False

def process_image_and_extract_tests(image_path):
    """
    Process an image and extract lab tests from it
    
    Parameters:
    - image_path: Path to the image file
    
    Returns:
    - result: Dictionary containing extraction results
    - original_img: Original image
    - processed_img: Preprocessed image
    """
    text, original_img, processed_img = extractText(image_path)
    lab_tests = parse_lab_tests(text)
    result = {
        "is_success": len(lab_tests) > 0,
        "data": lab_tests
    }
    
    return result, original_img, processed_img

# For standalone testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        if not os.path.exists(image_path):
            print(f"Error: File {image_path} not found")
            sys.exit(1)
            
        result, original_img, processed_img = process_image_and_extract_tests(image_path)
        
        # Display images
        display_image(original_img, 'Original Image')
        display_image(processed_img, 'Processed Image')
        
        # Print results
        import json
        print("\nJSON Output:")
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python lab_extractor.py <image_path>")
